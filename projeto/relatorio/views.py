from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SelecaoRelatorio
from projeto.email.models import Transacao, Mensagem 

@login_required
def relatorio(request):
	template_name = 'relatorio/relatorio.html' # Define o template que será utilizado
	context = {}
	
	if request.method == 'POST': # Caso o método seja POST
		form = SelecaoRelatorio(request.POST) # Alimenta formulário

		if form.is_valid(): # Verifica se dados estão validos
			# Busca mensagens do ano e mes escolhido
			mensagens = Mensagem.objects.filter(
				created_at__year=form.cleaned_data['ano'], 
				created_at__month=form.cleaned_data['mes']
				)
			
			qtdTipo1 = 0
			qtdTipo2 = 0
			qtdTipo3 = 0
			for mensagem in mensagens:
				# Busca a quantidade de emails disparados para a mensagem encontradas
				quantidade = Transacao.objects.filter(mensagem=mensagem).count()
				
				# Separa a quantidade de mensagens por tipo de produto
				if mensagem.tipo_produto == 1:
					qtdTipo1 = qtdTipo1 + quantidade 
				elif mensagem.tipo_produto == 2:
					qtdTipo2 = qtdTipo2 + quantidade
				elif mensagem.tipo_produto == 3:
					qtdTipo3 = qtdTipo3 + quantidade
			# Compõe o dicionário 
			context = {
				'tipo1': qtdTipo1,
				'tipo2': qtdTipo2,
				'tipo3': qtdTipo3,
				'ano': form.cleaned_data['ano'],
				'mes': form.cleaned_data['mes'],	
			}
			template_name = 'relatorio/resultado_relatorio.html' # Define o template de resultado
	else:
		form = SelecaoRelatorio() 
	
	context['form'] = form
	return render(request,template_name,context) # Renderiza template 