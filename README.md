# Projeto GGS Controle

## Comandos para subir aplicação em produção

Clone o repositório:

'''
https://github.com/gabrieldeoliveiraestevam/projeto.git
'''

Levantar o ambiente:

'''
docker-compose up
'''

Execute o comando de criação do super usuário (funcionário do Centeias):

'''
docker-compose run web python manage.py createsuperuser
'''

Criar usuário com os seguintes dados:

Usuário: saladesituacao
Email: saladesituacaofs@gmail.com
Senha: 12345678

Lembrando que a aplicação permiti a alteração de senha, sendo assim, a senha informada acima é somente provisória.
