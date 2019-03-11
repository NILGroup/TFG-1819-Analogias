from django import forms

from .models import WeiSpa30Variant


#Formulario para coger la palabra introducida en la vista
class PostFormWordSearch(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostFormWordSearch, self).__init__(*args, **kwargs)
       # self.fields['palabra'].required = False
        self.fields['word'].required = False

    class Meta:
        model = WeiSpa30Variant
        fields = ('word',)

       # def __str__(self):
       #     return self.palabra

        def __str__(self):
             return self.word
