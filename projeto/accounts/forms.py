from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
 
from projeto.core.utils import generate_hash_key
from projeto.core.mail import send_mail_template

from .models import PasswordReset

User  = get_user_model() # Utilizar usuário padrão declarado na settings

# Opções de produtos para escolha
TIPO_CHOICES = (
        (1, 'Clipping - Diário'),
        (2, 'Epidemiológico - Quinzenal'),
        (3, 'Monitoramento - Semanal'),
    )

# Resetar a senha - Opção esqueci minha senha 
class PasswordResetForm(forms.Form):
	email = forms.EmailField(label='Email')

	def clean_email(self):
		email = self.cleaned_data['email'] # Realiza validação do email
		# Verifica se existe usuário com o email
		if User.objects.filter(email=email).exists():
			return email
		else: # Caso não exista informa erro
			raise forms.ValidationError(
				'Nenhum usuário encontrado com este email'
			)

	def save(self):
		# Busca usuário do email informado
		user = User.objects.get(email=self.cleaned_data['email'])
		key = generate_hash_key(user.username) # Geração de senha aleatória
		reset = PasswordReset(key=key,user=user) # Gera objeto de resetar senha
		reset.save() # Salva objeto no bando de dados
		template_name = 'accounts/password_reset_mail.html'
		# Montando email
		subject = 'Criar nova senha no GGS Controle - Sala de Situação - FS - UnB'
		context = {
			'reset': reset
		}
		# Envia email
		send_mail_template(subject, template_name, context, [user.email])		

class RegisterForm (forms.ModelForm):

	name = forms.CharField(label='Nome')
	email = forms.EmailField(label='Email') # Criação do campo de email no formulário
	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput) # Senha com tamanho padrão
	password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)
	pais = forms.CharField(label='País')
	estado = forms.CharField(label='Estado')
	cidade = forms.CharField(label='Cidade')
	formacao = forms.CharField(label='Formação Acadêmica')
	tipo_produto = forms.MultipleChoiceField(
		choices=TIPO_CHOICES, label='Tipo de Produto', 
		widget=forms.CheckboxSelectMultiple, required=False
		)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		# Verifica se a senha e a confirmação foram preenchidas e se são diferentes
		if password1 and password2 and password1 != password2:
			# Erro
			raise forms.ValidationError ('A confirmação não está correta')

		return password2


	# Método save sobrepõe o método de UserCreationForm
	def save (self, commit=True):
		# Válida informações do usuário e retorno para user. Não salva no banco de dados.
		user = super(RegisterForm, self).save(commit=False) 
		user.set_password(self.cleaned_data['password1']) # Seta senha realizando a criptográfia
		if commit:
			user.save() # Salva no banco de dados.
		return user

	class Meta:
		model = User # Aproveita model do usuário
		fields = ['name', 'email', 'pais', 'estado', 'cidade', 'formacao', 'tipo_produto', 'username'] # Lista de campos para registro

class EditAccountForm(forms.ModelForm):
	# Declara campo de tipo de produto definindo o choice utilizado 
	tipo_produto = forms.MultipleChoiceField(
		choices=TIPO_CHOICES, label='Tipo de Produto', 
		widget=forms.CheckboxSelectMultiple(), required=False
	)

	class Meta:
		model = User # Aproveita model do usuário 
		fields = ['username', 'email', 'name', 'tipo_produto', 'pais', 'estado', 'cidade', 'formacao'] # Lista de campos do usuário padrão