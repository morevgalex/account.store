from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import QuerySet, Q, FilteredRelation
from .models import *
from .create_models import add
from django.db.models import Subquery


def index(request):
    games = Game.objects.all()
    games_with_objects = []
    for game in games:
        game_objects = Game_Object.objects.filter(game__title=game.title)
        games_with_objects.append({'game': game, 'game_objects': game_objects})
    context = {'games_with_objects': games_with_objects}
    return render(request, 'accstore_app/index.html', context)


def game_page(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    game_objects = Game_Object.objects.filter(game__title=game.title)
    context = {'game': game, 'game_objects': game_objects}
    return render(request, 'accstore_app/game_page.html', context)


def game_object_page(request, game_slug, object_slug):
    game_object = Game_Object.objects.get(game__slug=game_slug, object__slug=object_slug)
    products = Product.objects.filter(game_object=game_object)
    context = {'game_object': game_object, 'products': products}
    return render(request, 'accstore_app/game_object_page.html', context)


def product_page(request, game_slug, object_slug, product_id):
    game_object = Game_Object.objects.get(game__slug=game_slug, object__slug=object_slug)
    product = Product.objects.get(pk=product_id)
    product_values = Product_Value.objects.filter(product=product)
    context = {'game_object': game_object,
               'product': product,
               'product_values': product_values}
    return render(request, 'accstore_app/product_page.html', context)


def add_product_page(request, game_slug, object_slug):
    pass


def filter_page(request):
    print('----------------------')
    game_object = Game_Object.objects.select_related('game', 'object').get(game__slug='wow', object__slug='account')


    condition0 = Q(game_object=game_object)
    condition1 = Q(value__attribute__name='Race', value__value='Dwarf')
    condition2 = Q(value__attribute__name='Level', value__value='3')
    products = Product.objects.filter(condition0, pk__in=Product_Value.objects.filter(condition1).values('product').filter(product__in=Subquery(Product_Value.objects.filter(condition2).values('product'))))


    context = {'game_object': game_object, 'products': products}
    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    add()
    return HttpResponse('yes')