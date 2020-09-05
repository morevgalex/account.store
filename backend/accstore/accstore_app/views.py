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
               'g_objects': g_objects}
    return render(request, 'accstore_app/game_page.html', context)


def game_object_page(request, game_slug, object_slug):
    game = Game.objects.get(slug=game_slug)
    object = Object.objects.get(game=game, slug=object_slug)
    products = Product.objects.filter(game_object=Game_Object.objects.get(game=game, object=object))

    context = {'game': game,
               'object': object,
               'products': products}
    return render(request, 'accstore_app/game_object_page.html', context)


def product_page(request, game_slug, object_slug, product_id):
    game = Game.objects.get(slug=game_slug)
    object = Object.objects.get(game=game, slug=object_slug)
    product = Product.objects.get(pk=product_id)
    values = product.pre_values.all().union(Value.objects.filter(product_nonprevalue=product))

    context = {'game': game,
               'object': object,
               'product': product,
               'values': values}
    return render(request, 'accstore_app/product_page.html', context)


def add_product_page(request, game_slug, object_slug):
    pass


def filter_page(request):
    game = Game.objects.get(slug='world-of-warcraft')
    object = Object.objects.get(slug='accounts')

    condition_game_object = Q(attribute__game_object__game=game, attribute__game_object__object=object)

    condition_prevalue = Q(product_nonprevalue__isnull=True) & condition_game_object
    condition_race = Q(attribute__name='Race', value='Dwarf') & condition_prevalue
    condition_class = Q(attribute__name='Class', value='Mage') & condition_prevalue
    conditions_for_prevalue = (condition_race, condition_class)

    condition_nonpre = Q(product_nonprevalue__isnull=False) & condition_game_object
    condition_level = Q(attribute__name='Level', value='NonPreValue1') | Q(attribute__name='Level',
                                                                           value='NonPreValue2')
    conditions_for_nonpre = (condition_nonpre, condition_level)

    filtered_products = Product.objects

    for condition in conditions_for_prevalue:
        filtered_products = filtered_products.filter(pre_values=Value.objects.get(condition))

    for condition in conditions_for_nonpre:
        filtered_products = filtered_products.filter(
            id__in=Value.objects.filter(condition).values_list('product_nonprevalue'))

    context = {'game': game,
               'object': object,
               'products': filtered_products}
    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    tools.add_models('accstore_app/data/data.json', add_random_products=True, amount=1000)
    return HttpResponse('Completed')
