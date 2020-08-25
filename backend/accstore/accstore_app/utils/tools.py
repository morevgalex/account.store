from accstore_app.models import *
import random
import json


def add_models(path, add_random_products=False, amount=100):
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

            values = []

            for attribute_ in object_['ATTRIBUTES']:
                # create attributes
                name = attribute_['name']
                is_predefined = attribute_['is_predefined']
                typeof = attribute_['typeof']
                attribute = Attribute(name=name, game_object=Game_Object.objects.get(game=game, object=object), typeof=typeof,
                                      is_predefined=(lambda x: x == 'True')(is_predefined))
                attribute.save()

                values_set = []

                for value_ in attribute_['VALUES']:
                    # create values
                    value = Value(value=value_, attribute=attribute)
                    value.save()
                    if add_random_products:
                        values_set.append(value)

                if add_random_products:
                    values.append(values_set)

            if add_random_products:
                for number in range(amount):
                    values_for_product = []
                    for value_set in values:
                        values_for_product.append(random.choice(value_set))

                    title = ' '.join([value.value for value in values_for_product])

                    product = Product(title=title, game_object=Game_Object.objects.get(game=game, object=object),
                                      description='')
                    product.save()
                    product.values.add(*values_for_product)



