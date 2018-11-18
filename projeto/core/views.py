from django.shortcuts import render  # Atalho para renderizar um template

def home(request):
    return render(request, 'home.html') #Função de rederização recebe request, template e dicionário.
