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

            prevalues = []
            nonpre_attributes = []

            for attribute_ in object_['ATTRIBUTES']:
                # create attributes
                name = attribute_['name']
                is_predefined = (lambda x: x == 'True')(attribute_['is_predefined'])
                typeof = attribute_['typeof']
                attribute = Attribute(name=name, game_object=Game_Object.objects.get(game=game, object=object), typeof=typeof,
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
                                      description='')
                    product.save()
                    product.pre_values.add(*values_for_product)

                    for attribute in nonpre_attributes:
                        choice = random.choice(choices_nonpre)
                        Value(product_nonprevalue=product, value=choice, attribute=attribute).save()
                        product.title += f' {choice}'
                        product.save()


