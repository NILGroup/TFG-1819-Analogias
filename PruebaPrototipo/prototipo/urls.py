from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('version1', views.version1, name='version1'),
    path('version2', views.version2, name='version2'),
    path ('prueba', views.prueba, name='prueba'),
    path('imagen/<str:offset>', views.getImagen, name='getImagen'),
    path('imagenByPalabra/<str:palabra>', views.getImagenPalabra, name='getImagenPalabra'),
    path('json/word=<str:word>&level=<str:level>', views.getJsonResults, name='getJsonResults')

   # path('resultadoSinonimosRAE', views.sinonimosPalabrasRAE, name='sinonimosPalabrasRAE'),
]