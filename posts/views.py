from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from .models import Post, Categoria
from comentarios.models import Comentario
from django.utils import timezone
from django.db import models
from random import randint
from django.db.models import Q, Count, Case, When, Max, Sum
from comentarios.forms import FormComentario
from django.contrib import messages
from django.db import connection
from django.views.generic import View
# Create your views here.


class PostIndex(ListView):
    model = Post

    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    # reescrevendo metodo queryset

    def get_queryset(self):
        # metodo da classe pai a qual retorna um QuerySet
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')
        # Ordena o query set inversamente por id e filtra do post publicado
        qs = qs.order_by('-id').filter(publicado_post=True)
        # Conta o numero de comentarios QUANDO no Comentario.publicado_comentario for True. Então conte 1.
        qs = qs.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )

        return qs

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['connection'] = connection

        return contexto


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        # AO FAZER ISTO, VOCÊ NÃO PERDE O QUE FOI ESCRITO NO CÓDIGO ANTERIOR
        qs = super().get_queryset()

        # Em self.kwargs, contém o parâmetro enviado pelo método Get de nosso html
        # Sua estrutura é um dicionário {'categoria':valor_enviado}
        cat = Categoria.objects.values('nome_cat')

        categoria = self.kwargs.get('categoria', None)
        print('categoria', categoria)
        lista = []
        for v in cat:
            for e in v.values():
                lista.append(e.lower())
        if categoria not in lista:
            return qs

        # Caso nao haja categoria, retorne o qs padrão
        if not categoria:
            return qs
        # Para filtrar os posts ao clicar na categoria
        # Busque em Foreign Key categoria_post(Post) a coluna nome_cat(Categoria)
        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)
        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')
        # SE A CAIXA ESTÁ VAZIA, RETORNE A CONSULTA PADRÃO
        if not termo:
            return qs
        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__username__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo) |
            Q(titulo_post__icontains=termo)

        )
        return qs


# class PostDetalhes(UpdateView):
#     template_name = 'posts/post_detalhes.html'
#     model = Post
#     form_class = FormComentario
#     context_object_name = 'post'

#     def form_valid(self, form):
#         post = self.get_object()
#         print(post)
#         comentario = Comentario(**form.cleaned_data)

#         comentario.post_comentario = post

#         if self.request.user.is_authenticated:
#             print(self.request.user)
#             comentario.usuario_comentario = self.request.user

#         comentario.save()
#         messages.success(self.request, 'Comentario enviado com sucesso. ')
#         return redirect('post_detalhes', pk=post.id)

#     def get_context_data(self, **kwargs):

#         contexto = super().get_context_data(**kwargs)
#         post = self.get_object()

#         cometarios = Comentario.objects.filter(
#             publicado_comentario=True, post_comentario=post.id)
#         contexto['comentarios'] = cometarios
#         print(contexto['comentarios'])
#         return contexto

class PostDetalhes(View):
    template_name = 'posts/post_detalhes.html'

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        # PEGA O VALOR DO KWARGS (DICIONARIO {'pkey':103})
        pk = self.kwargs.get('pk')
        # RETORNA O OBJETO POST (id 103)
        post = Post.objects.get(pk=pk)
        # RETORNA COMENTARIOS COM post_comentario = 103 e publicado_comentario = True
        comentarios = Comentario.objects.filter(
            post_comentario=post, publicado_comentario=True)
        # CRIA FORMULÁRIO
        form = FormComentario(request.POST or None)
        self.contexto = {
            'post': post,
            'comentarios': comentarios,
            'form': form,

        }

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):
        # PEGA O FORMULÁRIO DO CONTEXTO
        form = self.contexto['form']

        if not form.is_valid():
            return render(request, self.template_name, self.contexto)

        comentario = form.save(commit=False)

        if request.user.is_authenticated:
            comentario.usuario_comentario = request.user

        comentario.post_comentario = self.contexto['post']
        comentario.save()
        messages.success(request, 'Seu comentario foi enviado para revisão')
        return redirect('post_detalhes', pk=self.kwargs.get('pk'))


def gera_titulo(caminho):
    lista_titulos = []
    with open(caminho, 'r', encoding='utf-8') as file:
        titulos = file.readlines()
        for linha in titulos:
            lista_titulos.append(linha)
    return lista_titulos[randint(0, len(lista_titulos)-1)]


def cria_conteudo():
    texto = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nesciunt sint,'
    'asperiores error eum delectus obcaecati recusandae facilis maiores assumenda quae adipisci non dolores unde!'
    ' Deserunt iure voluptates perferendis officiis nam!'
    return texto


def gera_id_cat():
    id_categorias = []
    for categoria in Categoria.objects.all():
        id_categorias.append(categoria.id)
    num_cat = id_categorias[randint(0, len(id_categorias)-1)]
    nome_cat = Categoria.objects.get(id=num_cat)
    return num_cat


def escolhe_imagem():

    diretorio = 'media/2023/02/27/chip_circuit_processor_140251_1280x720.jpg'
    return diretorio


def cria_post(request):
    lista = []
    # for e in range(15):
    #     post = Post()
    #     post.titulo_post = gera_titulo('modelos_titulos.txt')
    #     usuario_post = User.objects.get(id=randint(1, len(User.objects.all())))
    #     post.autor_post = usuario_post
    #     post.data_post = timezone.now()
    #     post.conteudo_post = cria_conteudo()
    #     post.excerto_post = 'Conteudo gerado por script'
    #     categoria = Categoria.objects.get(id=gera_id_cat())
    #     post.imagem_post = escolhe_imagem()
    #     post.categoria_post = categoria
    #     post.publicado_post = True
    #     post.save()

    comentarios = Comentario.objects.annotate(
        numero_coment=Count('publicado_comentario'))

    print(len(comentarios))
    return HttpResponse(f'')
