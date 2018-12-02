from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Transacao, Mensagem, Demanda 
from .forms  import Email

@login_required
def enviar_email(request):
	context = {}
	if request.method == 'POST': # Verifica se o método é POST
		form = Email(request.POST, request.FILES) 
		if form.is_valid(): # Valida formulário
			tipo_produto = form.cleaned_data['tipo_produto']
			# Decide qual é o tipo de produto para realizar a pesquisa
			if tipo_produto == '1':
				subject = 'Clipping de Notícias de Eventos de Interesse à Saúde Pública'				
			elif tipo_produto == '2':
				subject = 'Boletim Epidemiológico '
			elif tipo_produto == '3':
				subject = 'Boletim de Monitoramento de Eventos de Interesse a Saúde'
			
			subject = subject + " " + form.cleaned_data['complemento_assunto']

			# Seleciona clientes cadastrados para receberem o produto escolhido
			emails = Demanda.objects.filter(tipo_produto=tipo_produto)

			lista_email=[""]*emails.count() # Inicializa lista de emails

			if emails.count() != 0: # Caso tenham emails cadastrados para receberem o produto escolhido
				# Salva mensagem
				mensagem = Mensagem(tipo_produto=form.cleaned_data['tipo_produto'], 
									texto=form.cleaned_data['mensage'])
				mensagem.save() 
				i = 0
				for email in emails:
					# Salva no banco de dados cada email enviado
					transacao = Transacao(mensagem=mensagem, email = email.email_cliente)
					transacao.save()
					lista_email[i] = email.email_cliente # Criação da lista de emails
					i = i + 1

				form.send_mail(lista_email,subject,tipo_produto) # Envia email
				form = Email() # Iniciliza formulário de envio de email
				messages.success(request, 'Email enviado com sucesso!') 
			else:
				messages.info(request, 'Nenhum email está cadastrado para o produto escolhido!')
	else: # caso contrário preenche formulário em branco
		form = Email()

	context['form'] = form
 	
	template_name = 'email/email.html' # Define template que será utilizado
	return render(request, template_name, context)# Renderização do template 