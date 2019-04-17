from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('version1', views.version1, name='version1'),
    path('version2', views.version2, name='version2'),
    path ('prueba', views.prueba, name='prueba'),

   # path('resultadoSinonimosRAE', views.sinonimosPalabrasRAE, name='sinonimosPalabrasRAE'),
]