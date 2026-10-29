
from django.contrib.auth.decorators import login_required  # Exige que o usuário esteja conectado
from django.shortcuts import render, redirect  # Renderiza páginas e redireciona após salvar

from ..forms import PostForm  # Importa o formulário de criação de posts


@login_required  # Impede visitantes não autenticados de criar publicações
def create_post(request):

    if request.method == 'POST':  # Verifica se o formulário foi enviado
        form = PostForm(request.POST)  # Recebe os dados enviados pelo navegador

        if form.is_valid():  # Valida os campos do formulário
            post = form.save(commit=False)  # Prepara o post sem salvá-lo ainda
            post.user = request.user  # Define o autor como o usuário conectado
            post.save()  # Salva a publicação no banco de dados

            return redirect('post_view', id=post.id)  # Abre a publicação recém-criada

    else:
        form = PostForm()  # Cria um formulário vazio ao abrir a página

    return render(
        request,
        'projectus/create_post.html',  # Template da página de criação
        {
            'tag_title': 'Criar publicação - ProjectUs',
            'form': form,  # Envia o formulário para o template
        }
    )
