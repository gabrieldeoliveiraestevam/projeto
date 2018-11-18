from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import ( UserCreationForm, PasswordChangeForm,
	SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from projeto.core.utils import generate_hash_key

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from projeto.email.models import Demanda

User = get_user_model() # Utilizar usuário padrão declarado na settings

# Verifica se o usuário está logado para permitir a execução do método dashboard.
@login_required
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	context = {}
	return render(request, template_name, context) # Renderiza template.

def register(request):
	template_name = 'accounts/register.html' # Define o template que será utilizado.
	# Verifica se o método é um POST.
	if request.method == 'POST':
		form = RegisterForm(request.POST) # Inclui dados do POST do form.
		if form.is_valid(): # Verifica se o form está correto.
			user = form.save()     # Salva o form.

			lista_produtos = form.cleaned_data['tipo_produto']
			# Registra os produtos escolhidos pelo usuário
			for produto in lista_produtos:
				Demanda(tipo_produto=produto, 
						id_cliente=user.id,
						email_cliente=form.cleaned_data['email']).save()

			# Realiza a autenticação do login.
			user = authenticate(username=user.username, password=form.cleaned_data['password1'])
			login(request,user) # Realiza login
			return redirect('core:home') # Redireciona para o endereço do home.
	else:
		form = RegisterForm() # Caso o método seja GET iniciliza o form.

	# Cria o discionário conténdo as variáveis do template.
	context = {
		'form': form
	}
	return render(request, template_name, context) # Renderiza template.

def password_reset (request):
	template_name = 'accounts/passwordreset.html' # Define o template que será utilizado
	context = {}
	form = PasswordResetForm(request.POST or None) # Caso o POST esteja vazio envia o formulário vazio
	# Verifica se os dados informados no formulário estão correto
	if form.is_valid():
		form.save()
		context['sucess'] = True # Senha resetada com sucesso

	context['form'] = form # Insere formulário no dicionário
	return render(request, template_name, context) # Renderiza template

def password_reset_confirm(request, key):
	template_name = 'accounts/password_reset_confirm.html' # Define o template que será utilizado
	context = {}
	# Busca o registro no banco de dados, caso não encontre informa erro 404.
	reset = get_object_or_404(PasswordReset, key=key) 
	form = SetPasswordForm(user=reset.user, data=request.POST or None)
	# Verifica se a nova senha é correta
	if form.is_valid():
		form.save() # Salva nova senha
		context['success'] = True
	context['form'] = form # Adiciona o formulário ao dicionário
	return render(request, template_name, context) # Renderiza template

# Verifica se o usuário está logado para permitir a execução do método dashboard.
@login_required
def edit(request):
	template_name = 'accounts/edit.html' # Define o template que será utilizado.
	context = {}
	# Verifica se o método é um POST.
	
	if request.method == 'POST':
		form = EditAccountForm(request.POST, instance=request.user) # Cria formulário de edição.
		if form.is_valid(): # Verifica se o form está correto.	
			# Deleta produtos da tabela de demanda
			Demanda.objects.filter(id_cliente=request.user.get_id()).delete()
			form.save() # Salva alteração no banco de dados.
			lista_produtos = form.cleaned_data['tipo_produto']
			# Inclui os novos produtos escolhidos
			for produto in lista_produtos:
				Demanda(tipo_produto=produto, 
					 	id_cliente=request.user.get_id(),
					    email_cliente=request.user.get_email()).save()

			messages.success(request, 'Os seus dados foram alterados com sucesso!')
			return redirect('accounts:dashboard') # Redireciona para o painel do usuário
	else:
		form = EditAccountForm(instance=request.user) # Cria o formulário em branco.

	context['form'] = form
	return render(request, template_name, context) # Renderiza template.

# Verifica se o usuário está logado para permitir a execução do método dashboard.
@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html' # Define o template que será utilizado.
	context = {}
	# Verifica se o método é um POST.
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user) # Informa dados e usuário
		if form.is_valid(): # Verifica se o form está correto
			user = form.save()	# Salva alteração de senha no banco de dados
			messages.success(request, 'A sua senha foi alterada com sucesso!')
			# Realiza o login com a nova senha 
			user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
			login(request,user)
			return redirect('accounts:dashboard') # Redireciona para o painel do usuário
	else:
		form = PasswordChangeForm(user=request.user)
	context['form'] = form
	return render(request, template_name, context) # Renderiza template

# Verifica se o usuário está logado para permitir a execução do método dashboard.
@login_required
def delete(request):
	context = {}
	template_name = 'accounts/delete.html'
	
	# Verifica se o método é POST
	if request.method == 'POST':
		Demanda.objects.filter(id_cliente=request.user.get_id()).delete() # Deleta solicitacões do usuário 
		request.user.delete() # Deletar usuário
		messages.success(request, 'Usuário deletado com sucesso!')
		return redirect('accounts:login') # Redireciona para a página de login

	return render(request, template_name, context) # Renderiza template