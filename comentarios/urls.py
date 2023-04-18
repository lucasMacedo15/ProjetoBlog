from django.urls import path
from . import views

urlpatterns = [
    path('cria_comentarios/', views.cria_comentarios, name='cria_comentarios')
]
