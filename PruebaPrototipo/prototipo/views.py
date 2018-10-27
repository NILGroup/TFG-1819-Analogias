from django.shortcuts import render

from .forms import PostForm
from django.shortcuts import redirect
from .models import Formulario
from django.http import HttpResponseRedirect
# Create your views here.


def resultado(request, palabra):

    return render(request, 'prototipo/index.html', {})



def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'prototipo/index.html', {'form': form})
    else:
        form = PostForm()
        formularios = Formulario.objects.all()
        args = {'form': form, 'formularios': formularios}
        return render(request, 'prototipo/formulario.html', args)


