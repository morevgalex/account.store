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
    return HttpResponse(game_slug)


def game_object_page(request, game_slug, object_slug):
    pass


def product_page(request, game_slug, object_slug, product_id):
    pass


def add_product_page(request, game_slug, object_slug):
    pass