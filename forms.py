from django import forms
from django.forms import Form

class EmailForm(Form):
    assunto = forms.CharField()
    conteudo = forms.TextField()