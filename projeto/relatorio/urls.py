from django.urls import path
from projeto.relatorio.views import relatorio # Importando a view
app_name = 'relatorio'

urlpatterns = [
	path("", relatorio, name='relatorio'),
]