from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hack/', views.index, name='hack'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('config/<int:config_id>/', views.config),
    path('filter/', views.filter_products),
    path('<str:game_slug>/', views.games, name='game'),
    path('<str:game_slug>/<str:object_slug>/', views.game_object, name='game_object'),
    path('<str:game_slug>/<str:object_slug>/<int:product_id>/', views.products, name='product'),
    path('add/', views.add_game, name='add_game'),
    path('<str:game_slug>/add/', views.add_object, name='add_object'),
    path('<str:game_slug>/<str:object_slug>/add/', views.add_product, name='add_product_page'),
]