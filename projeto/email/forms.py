from django import forms # Importando biblioteca forms
from django.core.mail import send_mail # Importa a função para envio de email
from django.conf import settings
from projeto.core.mail import send_mail_template

# Opções de produtos para escolha
TIPO_CHOICES = (
    	(1, 'Clipping - Diário'),
    	(2, 'Epidemiológico - Quinzenal'),
    	(3, 'Monitoramento - Semanal'),
    )

# Classe herdando de Form
class Email(forms.Form):

	# requerid = true/false -> Define se o campo é ou não é obrigatório
	tipo_produto = forms.ChoiceField(
		choices=TIPO_CHOICES, label='Produto', widget=forms.Select(), required=True
	)
	mensage = forms.CharField(label='Mensagem', widget=forms.Textarea, required=False) # Campo texto de área
	file = forms.FileField(label='Arquivo', required=True)

	# Função para envio de email
	def send_mail(self, lista_email, subject, tipo_produto):
		#	 Montam informações do email
		context = {
			'mensage': self.cleaned_data['mensage'],
			'tipo_produto': tipo_produto
		}

		# Chama função do import django.core.mail
		template_name = 'email/corpo_email.html' # Template de email

		# Aciona função para envio do email
		send_mail_template(
			subject, 
			template_name, 
			context, 
			lista_email, 
			fail_silently=False, 
			files=self.cleaned_data['file']
			)