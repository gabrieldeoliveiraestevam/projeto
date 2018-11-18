from django.urls import path
from projeto.core.views import home # Importando a view
app_name = 'core'

urlpatterns = [
	path("", home, name="home"), # Informando o local e a view da url
]