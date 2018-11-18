from django.contrib import admin
admin.autodiscover()

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static 

app_name = 'accounts'

urlpatterns = [
    path("", include('projeto.core.urls',namespace='core')), # Inicio da cadeia de urls
    path("conta/", include('projeto.accounts.urls',namespace='accounts')), 
    path("email/", include('projeto.email.urls',namespace='email')), 
    path("relatorio/", include('projeto.relatorio.urls',namespace='relatorio')), 
    path('admin/', admin.site.urls),
]

if settings.DEBUG: # se estiver em ambiente de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)