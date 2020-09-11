import hashlib
from accstore_app.models import *
import random
import json
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accstore_app.settings import SALT


def add_models(path, add_random_products=False, amount=100):
    admin, moder, sellers, users = add_users()

    games = json.load(open(path))

    # create game
    for game_ in games:
        title = game_['title']
        description = game_['description']
        slug = game_['slug']
        game = Game(title=title, description=description, slug=slug)
        game.save()

        for object_ in game_['OBJECTS']:
            # create objects (and game_objects)
            name = object_['name']
            plural_name = object_['plural_name']
            slug = object_['slug']
            object = game.g_objects.create(name=name, plural_name=plural_name, slug=slug)

            prevalues = []
            nonpre_attributes = []

            for attribute_ in object_['ATTRIBUTES']:
                # create attributes
                name = attribute_['name']
                is_predefined = (lambda x: x == 'True')(attribute_['is_predefined'])
                typeof = attribute_['typeof']
                attribute = Attribute(name=name, game_object=Game_Object.objects.get(game=game, object=object),
                                      typeof=typeof,
                                      is_predefined=is_predefined)
                attribute.save()

                prevalues_set = []

                if is_predefined:
                    for value_ in attribute_['VALUES']:
                        # create values
                        value = Value(value=value_, attribute=attribute)
                        value.save()
                        if add_random_products:
                            prevalues_set.append(value)

                    if add_random_products:
                        prevalues.append(prevalues_set)
                else:
                    nonpre_attributes.append(attribute)

            if add_random_products:
                if nonpre_attributes:
                    choices_nonpre = [f'NonPreValue{x}' for x in range(5)]

                for number in range(amount):
                    values_for_product = []
                    for prevalues_set in prevalues:
                        values_for_product.append(random.choice(prevalues_set))

                    title = ' '.join([value.value for value in values_for_product])

                    product = Product(title=title, game_object=Game_Object.objects.get(game=game, object=object),
                                      description='', seller = random.choice(sellers), is_active=True)
                    product.save()
                    product.pre_values.add(*values_for_product)

                    for attribute in nonpre_attributes:
                        choice = random.choice(choices_nonpre)
                        Value(product_nonprevalue=product, value=choice, attribute=attribute).save()
                        product.title += f' {choice}'
                        product.save()

                    for i in range(10):
                        user = random.choice(users)
                        seller = product.seller
                        if user != seller.user:
                            order = Order.objects.create(user=random.choice(users), product=product, status=0)
                            Dispute.objects.create(order=order, status=0)


def add_users():
    role_adm = Role.objects.create(role=0)
    role_mod = Role.objects.create(role=1)
    role_usr = Role.objects.create(role=2)
    role_sel = Role.objects.create(role=3)

    admin = User.objects.create(login='admin', sha_password=get_sha('admin'), email='mor.evg.alex@gmail.com',
                                role=role_adm)
    moder = User.objects.create(login='moder', sha_password=get_sha('moder'), email='moder@moder.com',
                                role=role_mod)
    user1 = User.objects.create(login='seller1', sha_password=get_sha('seller1'), email='seller1@seller1.com',
                                    role=role_sel)
    user2 = User.objects.create(login='seller2', sha_password=get_sha('seller2'), email='seller2@seller2.com',
                                    role=role_sel)
    user3 = User.objects.create(login='user3', sha_password=get_sha('user3'), email='user3@user3.com',
                                role=role_usr)
    user4 = User.objects.create(login='user4', sha_password=get_sha('user4'), email='user4@user4.com',
                                role=role_usr)
    seller1 = Seller.objects.create(user=user1)
    seller2 = Seller.objects.create(user=user2)

    return admin, moder, (seller1, seller2), (user1, user2, user3, user4)


def paginate(request, qs, limit_name='limit', default_limit=10, max_limit=100, page_name='page', baseurl=''):
    try:
        limit = int(request.GET.get(limit_name, default_limit))
    except ValueError:
        limit = default_limit
    if limit > max_limit:
        limit = default_limit
    try:
        page = int(request.GET.get(page_name, 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    paginator.baseurl = baseurl + f'?{page_name}='
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page


def sort_helper(game, object, conditions='TODO'):
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

    for condition in conditions_for_prevalue:
        try:
            filtered_products = filtered_products.filter(pre_values=Value.objects.get(condition))
        except Value.DoesNotExist:
            raise FilterError('Error in condition')

    for condition in conditions_for_nonpre:
        filtered_products = filtered_products.filter(
            id__in=Value.objects.filter(condition).values_list('product_nonprevalue'))

    return filtered_products


class FilterError(Exception):
    def __init__(self, text):
        self.text = text


def get_sha(string):
    return hashlib.sha256((string + SALT).encode('ascii')).digest()
