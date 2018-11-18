import re # Regex
from django.db import models
from django.core import validators # Importa lista de validação
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)
from django.conf import settings
from multiselectfield import MultiSelectField

# Opções de produtos para escolha
TIPO_CHOICES = (
        (1, 'Clipping - Diário'),
        (2, 'Epidemiológico - Quinzenal'),
        (3, 'Monitoramento - Semanal'),
    )

class User(AbstractBaseUser, PermissionsMixin):

    # nome do usuário realiza validação utilizando regex informado no validators
    username = models.CharField('Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
            'O nome do usuário só pode conter letras, digitos ou os' 
            ' caracteres ( @ / . / + / - / _ )','invalid')])

    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Ativo', blank=True, default=True)
    is_staff = models.BooleanField('Funcionario', blank=True, default=False)
    data_inscricao = models.DateTimeField('Data de Inscrição', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)
    formacao = models.CharField('Formação', max_length=30, blank=True)
    pais = models.CharField('País', max_length=30, blank=True)
    estado = models.CharField('Estado', max_length=30, blank=True)
    cidade = models.CharField('Cidade', max_length=30, blank=True)
    tipo_produto = MultiSelectField('Tipo de Produto', choices=TIPO_CHOICES, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'  # ====> Acrescente essa linha
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)
    
    def get_email(self):
        return self.email

    def get_id(self):
        return self.id 

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

class PasswordReset (models.Model):

    # Relacionamento de chave estrangeira, quer dizer que um usuário pode ter vários pedidos de resetar a senha.
    # Relaciona com usuário custom.
    # Atributo reset criado para alterar senha do usuário utilizando o relacionamento.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário', 
        on_delete=models.CASCADE, related_name='reset'
    )

    key = models.CharField('Chave', max_length=100, unique=True) # Chave única
    created_at = models.DateTimeField('Criado em', auto_now_add=True) # O registro é incluido com o timestamp
    confirmed = models.BooleanField('Confirmado', default=False, blank=True) # Identifica se o usuário confirmou o reset da senha
    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at'] # Ordenar por data de criação de forma decrescente