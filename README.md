# Projeto GGS Controle

## Comandos para subir aplicação em produção

Clone o repositório:

```
https://github.com/gabrieldeoliveiraestevam/projeto.git
```

Levantar o ambiente:

```
docker-compose up
```

Execute o comando de criação do super usuário (funcionário da Sala de Situação do Centeias):

```
docker-compose run web python manage.py createsuperuser
```

Criar usuário com os seguintes dados:

```
Nome de Usuário: saladesituacao
E-mail: saladesituacaofs@gmail.com
Password: centeias1734
Password (again): centeias1734
```

Lembrando que a aplicação permiti a alteração de senha, sendo assim, a senha informada acima é somente provisória.
