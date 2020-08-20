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
    game_object = Game_Object.objects.select_related('game', 'object').get(game__slug='wow', object__slug='account')

    condition_race = Q(attribute__name='Race', value='Dwarf')
    condition_level = Q(attribute__name='Level', value='3')
    conditions_values = (condition_race, condition_level)

    condition_game_object = Q(game_object=game_object)
    filtered_products = Product.objects.filter(condition_game_object)
    for condition in conditions_values:
        filtered_products = filtered_products.filter(values__in=Value.objects.filter(condition))

    context = {'game_object': game_object, 'products': filtered_products}

    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    add()
    return HttpResponse('yes')