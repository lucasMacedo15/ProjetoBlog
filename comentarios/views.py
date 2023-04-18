from django.shortcuts import render, HttpResponse
from django.db import models
from django.contrib.auth.models import User
from .models import Comentario
from posts.models import Post
from posts.views import gera_titulo, cria_conteudo
from random import randint
from django.utils import timezone
# Create your views here.


#  nome_comentario = models.CharField(max_length=50)
#     email_comentario = models.EmailField(blank=False)
#     comentario = models.TextField(blank=False)
#     # QUANDO UM POST FOR DELETADO, DELETE TODOS OS COMENTÁRIOS QUE O POST TIVER
#     post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE)
#     # AO DELETAR UM USUÁRIO O QUAL FEZ O COMENTÁRIO, O COMENTÁRIO PERMANECE
#     usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     data_comentario = models.DateTimeField(default=timezone.now)
#     publicado_comentario = models.BooleanField(default=False)

def gera_id_post():
    id_categorias = []
    for categoria in Post.objects.all():
        id_categorias.append(categoria.id)
    num_post = id_categorias[randint(0, len(id_categorias)-1)]
    nome_post = Post.objects.get(id=num_post)
    return num_post


def cria_comentarios(request):
    for e in range(100):
        comentario = Comentario()
        comentario.nome_comentario = gera_titulo(
            'modelos_titulos_comentarios.txt')
        comentario.email_comentario = gera_titulo('modelos_emails.txt')
        comentario.comentario = cria_conteudo()
        comentario.post_comentario = Post.objects.get(id=gera_id_post())
        comentario.usuario_comentario = User.objects.get(
            id=randint(1, len(User.objects.all())))
        comentario.data_comentario = timezone.now()
        comentario.publicado_comentario = True
        comentario.save()

    return HttpResponse(Comentario.objects.all())
