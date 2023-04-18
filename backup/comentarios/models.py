from django.db import models
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=50)
    email_comentario = models.EmailField(blank=False)
    comentario = models.TextField(blank=False)
    # QUANDO UM POST FOR DELETADO, DELETE TODOS OS COMENTÁRIOS QUE O POST TIVER
    post_comentario = models.ForeignKey(Post, on_delete=models.CASCADE)
    # AO DELETAR UM USUÁRIO O QUAL FEZ O COMENTÁRIO, O COMENTÁRIO PERMANECE
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data_comentario = models.DateTimeField(default=timezone.now)
    publicado_comentario = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome_comentario
