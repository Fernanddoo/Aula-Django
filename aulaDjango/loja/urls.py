# loja/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página principal que lista os produtos (Read)
    path('', views.lista_produtos, name='lista_produtos'),

    # Rota para o formulário de adicionar um novo produto (Create)
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),

    # Rota para editar um produto existente (Update)
    path('editar/<int:pk>/', views.editar_produto, name='editar_produto'),

    # Rota para excluir um produto (Delete)
    path('excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),
]