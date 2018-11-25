from django import forms # Importando biblioteca forms

# Classe herdando de Form
class SelecaoRelatorio(forms.Form):
	ano = forms.IntegerField(label='Ano', min_value=1, required=True)
	mes = forms.IntegerField(label='Mês', min_value=1, max_value=12, required=False)
	dia = forms.IntegerField(label='Dia', min_value=1, max_value=31, required=False)

	# Realiza a validação de data campo a campo (ano, mês e dia)
	def valida_data(self):
		
		mensagem = ""
		# Verifica se ultrapassou o ĺimite de dias de meses que possuem 30 dias
		if ( self.cleaned_data['mes'] in ( 4, 6, 9, 11) ) and ( self.cleaned_data['dia'] > 30 ):
			mensagem = "O mês %d possui 30 dias!" % self.cleaned_data['mes']
		# Verifica se ultrapassou o limite de dias de fevereiro
		if ( self.cleaned_data['mes'] == 2 ):
			
			if ( self.cleaned_data['dia'] > 29 ):
				mensagem = "O mês %d possui 29 dias!" % self.cleaned_data['mes']
			else:
				# Caso o dia escolhido seja 29, verificar se o ano é bissexto
				bissexto = 0
				if ( self.cleaned_data['ano'] % 4 == 0 ):
					if ( self.cleaned_data['ano'] % 100 != 0 ):
						bissexto = 1
					else: 
						if ( self.cleaned_data['ano'] % 400 == 0 ):
							bissexto = 1						
				
				if bissexto == 0:
					mensagem = "O ano %d não é bissexto, então o mês %d possui 28 dias!" % (self.cleaned_data['ano'],self.cleaned_data['mes'])	
				
		return mensagem

		


