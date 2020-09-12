from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import ChatMessageForm
from .models import *
from . import forms
from .settings import ROLES
from .utils import tools, auth
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404, get_list_or_404

from .utils.auth import get_auth_data
from .utils.tools import get_sha, FilterError


def set_lang(f):
    def func(*args, **kwargs):
        lang = kwargs['lang']
        args[0].lang=lang

        return f(*args, **kwargs)
    return func


@set_lang
@require_GET
def index(request, **kwargs):
    chat_form = ChatMessageForm()

    chat_1 = Chat.objects.get_or_create(id=1)
    g_chat = GlobalChat.objects.get_or_create(chat=chat_1[0])
    if chat_1[1]:
        g_chat[0].users.add(*User.objects.all().values_list('id'))

    g_messages = Message.objects.all().filter(chat=chat_1[0])

    games = Game.objects.all()
    paginator, page = tools.paginate(request, games, baseurl=reverse('index', kwargs={'lang': request.lang}))

    context = {'games': page.object_list, 'paginator': paginator, 'page': page, 'chat_form': chat_form,
               'messages': g_messages, 'chat_id': chat_1[0].id}
    return render(request, 'accstore_app/base.html', context)


@require_POST
def send_message(request, **kwargs):
    if request.user:
        text = str(request.POST.get('message'))
        chat_id = int(request.POST.get('chat_id', 1))
        Message.objects.create(text=text, chat_id=chat_id, user=request.user)
        url = request.headers['Referer']
        if not url:
            return HttpResponseRedirect(reverse('index', kwargs={'lang': request.lang}))

    return HttpResponseRedirect(url)


@set_lang
def login(request, **kwargs):
    login_form = forms.LoginForm()
    error = ''
    if request.method == 'POST' and request.user:
        error = 'Вы уже вошли'
    elif request.method == 'POST':
        login_, password, url = get_auth_data(request)
        sessid = auth.do_login(login_, password)
        if sessid:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessid', sessid, httponly=True, domain='127.0.0.1',
                                expires=datetime.now() + timedelta(days=7))
            return response
        else:
            error = 'Неверный логин / пароль'

    return render(request, 'accstore_app/login.html', context={'error': error, 'login_form': login_form})


@set_lang
def register(request, **kwargs):
    login_form = forms.RegisterForm()
    error = ''
    if request.method == 'POST' and request.user:
        error = 'Вы уже вошли'
    elif request.method == 'POST':
        login_, password, url = get_auth_data(request)
        email = request.POST.get('email')
        User.objects.create(login=login_, sha_password=get_sha(password), email=email)
        print(login_, password)
        sessid = auth.do_login(login_, password)
        if sessid:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessid', sessid, httponly=True, domain='127.0.0.1',
                                expires=datetime.now() + timedelta(days=7))
            return response
        else:
            error = 'Неверный логин / пароль'

    return render(request, 'accstore_app/register.html', context={'error': error, 'login_form': login_form})


@set_lang
def logout(request, **kwargs):
    url = request.GET.get('continue', '/')
    if request.session:
        key = request.session.key
        Session.objects.get(key=key).delete()
        response = HttpResponseRedirect(url)
        response.set_cookie('sessid', key, expires=datetime(year=1975, month=1, day=1))
        return response

    return HttpResponseRedirect(url)


@set_lang
def user_page(request, user_id, **kwargs):
    target_user = get_object_or_404(User, id=user_id)
    products = Product.objects.all().filter(seller__user=target_user)

    paginator, page = tools.paginate(request, products,
                                     baseurl=reverse('user_page', kwargs={'lang': request.lang, 'user_id': target_user.id}))

    chat_form = ChatMessageForm()
    p_chat, p_messages, chat_id = None, None, None
    if request.user and request.user != target_user:
        try:
            p_chat = PersonalChat.objects.filter(users=request.user).get(users=target_user)
            print(p_chat)


        except PersonalChat.DoesNotExist:
            try:
                chat_id = Chat.objects.last().id + 1
            except TypeError:
                chat_id = 2

            chat = Chat.objects.create(id=chat_id)
            p_chat = PersonalChat.objects.create(chat=chat)
            p_chat.users.set([request.user, target_user])

            p_chat = PersonalChat.objects.filter(users=request.user).get(users=target_user)

        chat = Chat.objects.get(id=p_chat.chat.id)
        chat_id = chat.id
        p_messages = Message.objects.filter(chat=chat)

    context = {'target_user': target_user, 'products': page.object_list,
               'roles': ROLES, 'paginator': paginator, 'page': page, 'messages': p_messages, 'chat_form': chat_form,
               'chat_id': chat_id}
    return render(request, 'accstore_app/user_page.html', context)


@set_lang
@require_GET
def games(request, game_slug, **kwargs):
    game = get_object_or_404(Game, slug=game_slug)
    products = Product.objects.filter(game_object__game=game)
    paginator, page = tools.paginate(request, products, baseurl=game.get_absolute_url())

    context = {'game': game, 'products': page.object_list, 'paginator': paginator, 'page': page}
    return render(request, 'accstore_app/game_page.html', context)


@set_lang
@require_GET
def add_game(request):
    pass


@set_lang
@require_GET
def game_object(request, game_slug, object_slug, **kwargs):
    game = get_object_or_404(Game, slug=game_slug)
    object = get_object_or_404(Object, game=game, slug=object_slug)
    products = get_list_or_404(Product, game_object=get_object_or_404(Game_Object, game=game, object=object))
    paginator, page = tools.paginate(request, products,
                                     baseurl=reverse('game_object', kwargs={'lang': request.lang, 'game_slug': game_slug,
                                                                            'object_slug': object_slug}))

    context = {'game': game,
               'object': object,
               'products': page.object_list,
               'paginator': paginator,
               'page': page}
    return render(request, 'accstore_app/game_object_page.html', context)


@set_lang
@require_GET
def products(request, game_slug, object_slug, product_id, **kwargs):
    game = get_object_or_404(Game, slug=game_slug)
    object = get_object_or_404(Object, game=game, slug=object_slug)
    product = get_object_or_404(Product, pk=product_id)
    values = product.pre_values.all().union(Value.objects.filter(product_nonprevalue=product))

    context = {'game': game,
               'object': object,
               'product': product,
               'values': values}
    return render(request, 'accstore_app/product_page.html', context)


@set_lang
def add_product(request, lang, game_slug, object_slug):
    # TODO
    pass


@set_lang
@require_GET
def filter_products(request, **kwargs):
    game = get_object_or_404(Game, slug='world-of-warcraft')
    object = get_object_or_404(Object, slug='accounts')

    try:
        filtered_products = tools.sort_helper(game, object)
    except FilterError:
        filtered_products = []

    context = {'game': game, 'object': object, 'products': filtered_products}

    return render(request, 'accstore_app/filter_page.html', context)


@set_lang
def config(request, config_id, **kwargs):
    tools.add_models('accstore_app/data/data.json', add_random_products=True, amount=100)
    return HttpResponse('Completed')


@set_lang
def hack(request, **kwargs):
    pass
    # TODO attempt to hack site via csrf or ddos attack
