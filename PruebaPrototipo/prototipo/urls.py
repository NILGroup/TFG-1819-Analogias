from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prototipo/form', views.resultado, name='resultado'),

]