from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<str:game_slug>/', views.game_page, name='game_page'), #страничка игры
    path('<str:game_slug>/<str:object_slug>/', views.game_object_page, name='game_object_page'), #страничка товаров игры
    path('<str:game_slug>/<str:object_slug>/<int:product_id>/', views.product_page, name='product_page'), #страничка товара
    path('<str:game_slug>/<str:object_slug>/add/', views.add_product_page, name='add_product_page'), #страничка добавления товара игры
]