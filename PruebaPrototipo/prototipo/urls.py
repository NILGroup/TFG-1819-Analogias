from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('word=<str:word>&level=<str:level>', views.principal, name='principal'),
    path('image_offset/<str:offset>', views.getImagen, name='getImagen'),
    path('image_word/<str:palabra>', views.getImagenPalabra, name='getImagenPalabra'),
    path('easysynonym/json/word=<str:word>&level=<str:level>', views.getSynonymsJsonResults, name='getSynonymsJsonResults'),
    path('easyhyponym/json/word=<str:word>&level=<str:level>', views.getHyponymsJsonResults, name='getHyponymsJsonResults'),
    path('easyhyperonym/json/word=<str:word>&level=<str:level>', views.getHyperonymsJsonResults, name='getHyperonymsJsonResults'),
    path('metaphor/json/word=<str:word>&level=<str:level>', views.getMetaphor, name='getMetaphor'),
    path('simil/json/word=<str:word>&level=<str:level>', views.getSimil, name='getSimil'),
    path('def_example/json/word=<str:word>&level=<str:level>', views.getDefAndExample, name='getDefAndExample'),



   # path('resultadoSinonimosRAE', views.sinonimosPalabrasRAE, name='sinonimosPalabrasRAE'),
]