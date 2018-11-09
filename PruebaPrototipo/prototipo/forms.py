from django import forms

from .models import Formulario, FormularioTerminos

class PostForm(forms.ModelForm):

    class Meta:
        model = Formulario
        fields = ('campoPalabra',)

        def __str__(self):
            return self.campoPalabra



class PostFormTerminos(forms.ModelForm):

    class Meta:
        model = FormularioTerminos
        fields = ('Palabra',)

        def __str__(self):
            return self.Palabra