from django import forms # Importando biblioteca forms

# Classe herdando de Form
class SelecaoRelatorio(forms.Form):
	ano = forms.IntegerField(label='Ano', min_value=1)
	mes = forms.IntegerField(label='Mês', min_value=1, max_value=12)

