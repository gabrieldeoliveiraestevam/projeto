# Projeto GGS Controle

## Comandos para subir aplicação em produção

Clone o repositório:

...
https://github.com/gabrieldeoliveiraestevam/projeto.git
...

Levantar o ambiente:

...
docker-compose up
...

Execute o comando de criação do super usuário (funcionário do Centeias):

...
docker-compose run web python manage.py createsuperuser
...
