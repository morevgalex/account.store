from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def index(request):
    games = Game.objects.all()
    games_with_objects = []
    for game in games:
        game_objects = Game_Object.objects.filter(game_title=game.title)
        games_with_objects.append({'game': game, 'game_objects': game_objects})
    context = {'games_with_objects': games_with_objects}
    print(context)
    return render(request, 'accstore_app/index.html', context)


def game_page(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    game_objects = Game_Object.objects.filter(game_title=game.title)
    pass


def game_object_page(request, game_slug, object_slug):
    game = Game.objects.get(slug=game_slug)
    game_object = Game_Object.objects.get(game_title=game.title, object_name__slug=object_slug)
    context = {'game': game, 'game_object': game_object}
    print(context)
    return render(request, 'accstore_app/game_object_page.html', context)


def product_page(request, game_slug, object_slug, product_id):
    pass


def add_product_page(request, game_slug, object_slug):
    pass