from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import *
from .utils import tools
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404, get_list_or_404


@require_GET
def index(request):
    games = get_list_or_404(Game)
    paginator, page = tools.paginate(request, games, baseurl=reverse('index'))

    context = {'games': page.object_list, 'paginator': paginator, 'page': page}
    return render(request, 'accstore_app/index.html', context)


@require_GET
def game_page(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    products = Product.objects.filter(game_object__game=game)
    paginator, page = tools.paginate(request, products, baseurl=Game.get_absolute_url())

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

    condition_game_object = Q(attribute__game_object=get_object_or_404(Game_Object, game=game, object=object))

    condition_prevalue = Q(product_nonprevalue__isnull=True) & condition_game_object
    condition_race = Q(attribute__name='Race', value='Dwarf') & condition_prevalue
    condition_class = Q(attribute__name='Class', value='Mage') & condition_prevalue
    conditions_for_prevalue = (condition_race, condition_class)

    condition_nonpre = Q(product_nonprevalue__isnull=False) & condition_game_object
    condition_level = Q(attribute__name='Level', value='NonPreValue1') | Q(attribute__name='Level',
                                                                           value='NonPreValue2')
    conditions_for_nonpre = (condition_game_object, condition_nonpre, condition_level)

    filtered_products = Product.objects
    context = {'game': game, 'object': object, 'products': []}

    for condition in conditions_for_prevalue:
        try:
            filtered_products = filtered_products.filter(pre_values=Value.objects.get(condition))
        except Value.DoesNotExist:
            return render(request, 'accstore_app/filter_page.html', context)

    for condition in conditions_for_nonpre:
        filtered_products = filtered_products.filter(
            id__in=Value.objects.filter(condition).values_list('product_nonprevalue'))

    context['products'] = filtered_products

    return render(request, 'accstore_app/filter_page.html', context)


def config_page(request, config_id):
    tools.add_models('accstore_app/data/data.json', add_random_products=True, amount=1000)
    return HttpResponse('Completed')
