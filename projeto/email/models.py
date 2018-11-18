from django.db import models 
# Declaração das classes da aplicação email

class Mensagem(models.Model):
	tipo_produto = models.IntegerField('Tipo de Produto', blank=True, default=0)
	texto = models.TextField('Mensagem', blank=True)
	created_at = models.DateTimeField('Enviada em', auto_now_add=True) 
		
	class Meta:
		verbose_name = 'Mensagem'
		verbose_name_plural = 'Mensagens'
	
class Transacao(models.Model):
	mensagem = models.ForeignKey(Mensagem, verbose_name='Mensagem', on_delete=models.CASCADE)
	email = models.EmailField('Email')

	class Meta:
		verbose_name = 'Transação'
		verbose_name_plural = 'Transações'

class Demanda(models.Model):
	tipo_produto = models.IntegerField('Tipo de Produto', blank=True, default=0)	
	id_cliente = models.IntegerField('Id do Cliente')	
	email_cliente = models.EmailField('Email do Cliente')
	created_at = models.DateTimeField('Incluido em', auto_now_add=True) 
	
	class Meta:
		verbose_name = 'Demanda'
		verbose_name_plural = 'Demandas'
