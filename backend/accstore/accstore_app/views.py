from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .utils import tools
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, get_list_or_404

from .utils.tools import FilterError


@require_GET
def index(request):
    games = get_list_or_404(Game)
    paginator, page = tools.paginate(request, games, baseurl=reverse('index'))

    context = {'games': page.object_list, 'paginator': paginator, 'page': page}
    return render(request, 'accstore_app/base.html', context)


@require_GET
def game_page(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    products = Product.objects.filter(game_object__game=game)
    paginator, page = tools.paginate(request, products, baseurl=game.get_absolute_url())

    context = {'game': game, 'products': page.object_list, 'paginator': paginator, 'page': page}
    return render(request, 'accstore_app/game_page.html', context)


@require_GET
def game_object_page(request, game_slug, object_slug):
    game = get_object_or_404(Game, slug=game_slug)
    object = get_object_or_404(Object, game=game, slug=object_slug)
    products = get_list_or_404(Product, game_object=get_object_or_404(Game_Object, game=game, object=object))
    paginator, page = tools.paginate(request, products, baseurl=reverse('game_object', kwargs={'game_slug': game_slug,
                                                                                               'object_slug': object_slug}))

    context = {'game': game,
               'object': object,
               'products': page.object_list,
               'paginator': paginator,
               'page': page}
    return render(request, 'accstore_app/game_object_page.html', context)


@require_GET
def product_page(request, game_slug, object_slug, product_id):
    game = get_object_or_404(Game, slug=game_slug)
    object = get_object_or_404(Object, game=game, slug=object_slug)
    product = get_object_or_404(Product, pk=product_id)
    values = product.pre_values.all().union(Value.objects.filter(product_nonprevalue=product))

    context = {'game': game,
               'object': object,
               'product': product,
               'values': values}
    return render(request, 'accstore_app/product_page.html', context)


def add_product_page(request, game_slug, object_slug):
    pass


@require_GET
def filter_page(request):
    game = get_object_or_404(Game, slug='world-of-warcraft')
    object = get_object_or_404(Object, slug='accounts')

    try:
        filtered_products = tools.sort_helper(game, object)
    except FilterError:
        filtered_products = []

    context = {'game': game, 'object': object, 'products': filtered_products}

    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    tools.add_models('accstore_app/data/data.json', add_random_products=True, amount=1000)
    return HttpResponse('Completed')
