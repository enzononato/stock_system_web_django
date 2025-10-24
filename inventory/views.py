# inventory/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, History
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ItemForm

#
# 1. FUNÇÃO DE LOGIN
#
def login_view(request):
    """
    Substitui a sua antiga tela de login do Tkinter.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redireciona para a lista de itens após o login
            return redirect('item_list')
    else:
        form = AuthenticationForm()
        
    return render(request, 'inventory/login.html', {'form': form})

#
# 2. FUNÇÃO DE LOGOUT
#
def logout_view(request):
    logout(request)
    # Redireciona de volta para a tela de login
    return redirect('login')

#
# 3. FUNÇÃO DA LISTA DE ESTOQUE (PROTEGIDA POR LOGIN)
#
@login_required 
def item_list(request):
    """
    Substitui a sua "Aba Estoque".
    """
    itens = Item.objects.filter(is_active=True).order_by('id')
    
    context = {
        'itens': itens,
    }
    
    return render(request, 'inventory/item_list.html', context)


@login_required
def item_create_view(request):
    """
    Lida com a criação de um novo item no estoque.
    """
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # Salva o item no banco
            item = form.save()
            
            # Cria o registro de histórico
            History.objects.create(
                item=item,
                operador=request.user, # request.user é o usuário logado
                operation='Cadastro'
            )
            
            # Redireciona para a lista de estoque
            return redirect('item_list')
    else:
        # Se for um GET, apenas exibe um formulário em branco
        form = ItemForm()
    
    context = {
        'form': form
    }
    return render(request, 'inventory/item_form.html', context)