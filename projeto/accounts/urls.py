from django.urls import path
from django.contrib.auth.views import login, logout # Importa login padrão do Django
from projeto.accounts.views import register, dashboard, edit, edit_password, password_reset, password_reset_confirm, delete
app_name = 'accounts'

urlpatterns = [
	path("", dashboard, name='dashboard'), # controle de perfil do usuário
	path("entrar/", login, {'template_name': 'accounts/login.html'}, name='login'), # controle de login
	path("sair/", logout, {'next_page': 'core:home'}, name='logout'), # controle de logout
	path("cadastre-se/", register, name='register'),  # controle de cadastro de usuário
	path("nova-senha/", password_reset, name='password_reset'),  # controle de solicitação de nova senha
	path("confirmar-nova-senha/<key>/", password_reset_confirm, 
	 name='password_reset_confirm'),  # controle de confirmação de nova senha
	path("editar/", edit, name='edit'),  # controle de alteração de dados do usuário
	path("editar-senha/", edit_password, name='edit_password'),  # controle de alteração de senha
	path("deletar/", delete, name='delete'),  # controle para deletar usuário
]