from django import forms

from .models import Formulario

class PostForm(forms.ModelForm):

    class Meta:
        model = Formulario
        fields = ('campoPalabra',)