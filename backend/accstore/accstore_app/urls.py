from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config/<int:config_id>/', views.config_page),
    path('filter/', views.filter_page),
    path('<str:game_slug>/', views.game_page, name='game'),
    path('<str:game_slug>/<str:object_slug>/', views.game_object_page, name='game_object'),
    path('<str:game_slug>/<str:object_slug>/<int:product_id>/', views.product_page, name='product'),
    path('<str:game_slug>/<str:object_slug>/add/', views.add_product_page, name='add_product_page'),
]