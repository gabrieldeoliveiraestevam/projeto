from django.urls import path
from projeto.email.views import enviar_email # Importando a view
app_name = 'email'

urlpatterns = [
	path("", enviar_email, name='enviar_email'),
]