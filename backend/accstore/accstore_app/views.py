from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import *
from .utils import tools


def index(request):
    games = Game.objects.all()
    games_with_objects = []
    for game in games:
        games_with_objects.append({'game': game, 'objects': game.g_objects.all()})

    context = {'games_with_objects': games_with_objects}
    return render(request, 'accstore_app/index.html', context)


def game_page(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    g_objects = game.g_objects.all()

    context = {'game': game,
               'objects': g_objects}
    return render(request, 'accstore_app/game_page.html', context)


def game_object_page(request, game_slug, object_slug):
    game = Game.objects.get(slug=game_slug)
    g_object = Object.objects.get(game=game, slug=object_slug)
    products = Product.objects.filter(game_object=Game_Object.objects.get(game=game, object=g_object))

    context = {'game': game,
               'object': g_object,
               'products': products}
    return render(request, 'accstore_app/game_object_page.html', context)


def product_page(request, game_slug, object_slug, product_id):
    game = Game.objects.get(slug=game_slug)
    g_object = Object.objects.get(game=game, slug=object_slug)
    product = Product.objects.get(pk=product_id)
    values = product.values.all()

    context = {'game': game,
               'object': g_object,
               'product': product,
               'values': values}
    return render(request, 'accstore_app/product_page.html', context)


def add_product_page(request, game_slug, object_slug):
    pass


def filter_page(request):
    game = Game.objects.get(slug='world-of-warcraft')
    g_object = Object.objects.get(game=game, slug='accounts')

    condition_race = Q(attribute__name='Race', value='Dwarf')
    condition_level = Q(attribute__name='Level', value='3')
    conditions_values = (condition_race, condition_level)

    condition_game_object = Q(game_object__game=game, game_object__object=g_object)
    filtered_products = Product.objects.filter(condition_game_object)
    for condition in conditions_values:
        filtered_products = filtered_products.filter(values__in=Value.objects.filter(condition))

    context = {'game': game,
               'object': g_object,
               'products': filtered_products}
    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    tools.add_models(add_random_products=True)
    return HttpResponse('Completed')
