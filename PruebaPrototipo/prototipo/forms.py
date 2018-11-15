from django import forms

from .models import Formulario, FormularioTerminos, FormularioFinal

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['campoPalabra'].required = False

    class Meta:
        model = Formulario
        fields = ('campoPalabra',)

        def __str__(self):
            return self.campoPalabra



class PostFormTerminos(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostFormTerminos, self).__init__(*args, **kwargs)
        self.fields['Palabra'].required = False

    class Meta:
        model = FormularioTerminos
        fields = ('Palabra',)

        def __str__(self):
            return self.Palabra


class PostFormFinal(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostFormFinal, self).__init__(*args, **kwargs)
        self.fields['Word'].required = False


    class Meta:
        model = FormularioFinal
        fields = ('Word', 'Depth',)

        def __str__(self):
            return self.Word