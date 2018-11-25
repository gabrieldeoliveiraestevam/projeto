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
		# Realiza validação do forms
		is_valid = form.is_valid()
		# Caso o dia tenha sido informado, valida a toda a data
		erro = ""
		if form.cleaned_data['dia'] != None:
			# Verifica se a data informada está correta
			erro = form.valida_data()
				
		if form.is_valid() and erro == "": # Verifica se dados estão validos
			# Busca mensagens do ano, mes e dia escolhido
			# Verifica a pesquisa que será realizada
			if form.cleaned_data['mes'] == None or form.cleaned_data['dia'] == None:
				if form.cleaned_data['mes'] == None:
					mensagens = Mensagem.objects.filter(
						created_at__year=form.cleaned_data['ano'], 	
					)
					tipo_pesquisa = "1"
				else:
					mensagens = Mensagem.objects.filter(
						created_at__year=form.cleaned_data['ano'], 
						created_at__month=form.cleaned_data['mes'],
						)
					tipo_pesquisa = "2"
			else:
				mensagens = Mensagem.objects.filter(
						created_at__year=form.cleaned_data['ano'], 
						created_at__month=form.cleaned_data['mes'],
						created_at__day=form.cleaned_data['dia']				
						)
				tipo_pesquisa = "3"

			
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
				'dia': form.cleaned_data['dia'],
				'tipo_pesquisa': tipo_pesquisa,
			}
			template_name = 'relatorio/resultado_relatorio.html' # Define o template de resultado	
		else:
			context['erro'] = erro
	else:
		context['erro'] = ""
		form = SelecaoRelatorio() 
	
	context['form'] = form
	return render(request,template_name,context) # Renderiza template 