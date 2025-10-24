# inventory/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. A rota raiz ('') aponta para a view de login.
    #    O nome 'login' permanece o mesmo.
    path('', views.login_view, name='login'),
    
    # 2. A lista de estoque agora fica em 'inventory/'
    #    O nome 'item_list' permanece o mesmo.
    path('inventory/', views.item_list, name='item_list'),

    # 3. A rota de logout permanece
    path('logout/', views.logout_view, name='logout'),

    # 4. Rota para criar um novo item
    path('inventory/add/', views.item_create_view, name='item_add'),
]