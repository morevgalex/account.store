from .models import *
import random


def add():
    add_random_products = True
    wow = {'title': 'World of Warcraft',
           'description': '',
           'slug': 'world-of-warcraft',
           'OBJECTS': ({
                           'name': 'Account',
                           'plural_name': 'Accounts',
                           'slug': 'accounts',
                           'ATTRIBUTES': ({
                                              'name': 'Race',
                                              'is_predefined': True,
                                              'VALUES': ('Dwarf', 'Elf', 'Human', 'Dead'),
                                          },
                                          {
                                              'name': 'Leves',
                                              'is_predefined': True,
                                              'VALUES': ('1', '2', '3', '4', '5'),
                                          },
                                          {
                                              'name': 'Class',
                                              'is_predefined': True,
                                              'VALUES': (
                                                  'Warrior', 'Mage', 'Rogue', 'Priest', 'Paladin',
                                                  'Shaman', 'Monk'),
                                          },
                                          {
                                              'name': 'Server',
                                              'is_predefined': True,
                                              'VALUES': ('EU', 'RU'),
                                          }
                           )
                       },
                       {
                           'name': 'Item',
                           'plural_name': 'Items',
                           'slug': 'items',
                           'ATTRIBUTES': ({
                                              'name': 'Race',
                                              'is_predefined': True,
                                              'VALUES': ('Dwarf', 'Elf', 'Human', 'Dead'),
                                          },
                                          {
                                              'name': 'Leves',
                                              'is_predefined': True,
                                              'VALUES': ('1', '2', '3', '4', '5'),
                                          },
                                          {
                                              'name': 'Class',
                                              'is_predefined': True,
                                              'VALUES': (
                                                  'Warrior', 'Mage', 'Rogue', 'Priest', 'Paladin',
                                                  'Shaman', 'Monk'),
                                          },
                                          {
                                              'name': 'Server',
                                              'is_predefined': True,
                                              'VALUES': ('EU', 'RU'),
                                          }
                           )
                       },
           )
           }
    wot = {'title': 'World of Tanks',
           'description': '',
           'slug': 'world-of-tanks',
           'OBJECTS': ({
                           'name': 'Tank',
                           'plural_name': 'Tank',
                           'slug': 'Tank',
                           'ATTRIBUTES': (
                               {
                                   'name': 'Level',
                                   'is_predefined': True,
                                   'VALUES': ('1', '2', '3', '4', '5'),
                               },
                               {
                                   'name': 'Class',
                                   'is_predefined': True,
                                   'VALUES': (
                                       'Light', 'Medium', 'Heavy', 'Artillery'),
                               },
                               {
                                   'name': 'Server',
                                   'is_predefined': True,
                                   'VALUES': ('EU', 'RU'),
                               }
                           )
                       },

           )
           }

    games = (wow, wot)

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
                attribute = Attribute(name=name, game_object=Game_Object.objects.get(game=game, object=object),
                                      is_predefined=is_predefined)
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
                for number in range(random.randint(30, 50)):
                    values_for_product = []
                    for value_set in values:
                        values_for_product.append(random.choice(value_set))

                    title = ' '.join([value.value for value in values_for_product])

                    product = Product(title=title, game_object=Game_Object.objects.get(game=game, object=object),
                                      description='')
                    product.save()
                    product.values.add(*values_for_product)



