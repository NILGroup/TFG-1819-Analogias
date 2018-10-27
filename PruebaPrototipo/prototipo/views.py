from django.shortcuts import render

from .forms import PostForm
from django.shortcuts import redirect
from .models import Formulario
from django.http import HttpResponseRedirect
# Create your views here.


def resultado(request):

    return render(request, 'prototipo/index.html', {})



def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            palabra  = form.save()

            palabra.save()
            return redirect('resultado', palabra)
    else:
            form = PostForm()
    return render(request, 'prototipo/formulario.html', {'form': form})


