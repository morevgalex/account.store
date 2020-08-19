from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import QuerySet, Q
from .models import *
from .create_models import add


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
    game_objects = Game_Object.objects.filter(game_title=game.title)
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
    game_object = Game_Object.objects.get(game__slug='wow', object__slug='account')
    # product_values1 = Product_Value.objects.filter(product__game_object=game_object, value__value='Dwarf')
    # print(product_values1)
    # product_values2 = Product_Value.objects.filter(product__game_object=game_object, value__value='3')
    # print(product_values2)

    # почему это работает? ведь после intersection получается пустой QuerySet,
    # но values_list показывает что сущности, имеющие product в нем есть

    # products_id = product_values1.intersection(product_values2).values_list('product')
    # print(products_id)
    # products = Product.objects.filter(pk__in=list(map(lambda x: x[0],products_id)))
    # print(products)
    condition = Q(product__game_object=game_object) & (Q(value__attribute__name='Race', value__value='Dwarf') | Q(value__attribute__name='Level', value__value='3'))
    products_id_list: QuerySet = list(map(lambda x: x[0], Product_Value.objects.filter(condition).values_list('product')))
    print(f'products_id_list: {products_id_list}')
    # 2 - число атрибутов объекта игры, по которым происходит сортировка, в данном случае 2 атрибута: раса и уровень
    products_id_list_filtered = list(filter(lambda x: products_id_list.count(x) == 2, products_id_list))
    print(f'products_id_list_filtered: {products_id_list_filtered}')
    products = Product.objects.filter(pk__in=products_id_list_filtered)
    context = {'game_object': game_object, 'products': products}
    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    add()
    return HttpResponse('yes')