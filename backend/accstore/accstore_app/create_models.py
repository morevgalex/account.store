from .models import *


def add_game(title):
    game = Game(title=title, description='', slug=title.replace(' ','').lower())
    game.save()
    return game


def add_object(name):
    object_ = Object(name=name, plural_name=name+'s', slug=name.replace(' ', '').lower())
    object_.save()
    return object_


def add_game_object(game, object):
    game_object = Game_Object(game=game, object=object)
    game_object.save()
    return game_object


def add_attribute(game_object, *args):
    attributes = []
    for arg in args:
        attribute = Attribute(name=arg, game_object=game_object, is_predefined=True)
        attribute.save()
        attributes.append(attribute)
    return attributes


def add_values(attribute, *args):
    values = []
    for arg in args:
        value = Value(attribute=attribute, value=arg)
        value.save()
        values.append(value)
    return values


def add_product(title, game_object):
    product = Product(title=title, game_object=game_object, description='')
    product.save()
    return product


def add_product_values(product, *args):
    for arg in args:
        product_value = Product_Value(product=product, value=arg)
        product_value.save()


def add():
    game = add_game('Wow')

    object = add_object('Account')

    game_object = add_game_object(game, object)
    attributes = add_attribute(game_object, 'Race', 'Level', 'Class')
    values_race = add_values(attributes[0], 'Dwarf', 'Elf', 'Human')
    values_levels = add_values(attributes[1], '1', '2', '3')
    values_classes = add_values(attributes[2], 'Warrior', 'Mage', 'Rogue')

    product = add_product('Warrior Dwarf 2lvl', game_object)
    add_product_values(product, values_race[0], values_levels[1], values_classes[0])

    product = add_product('Mage Elf 1lvl', game_object)
    add_product_values(product, values_race[1], values_levels[0], values_classes[1])

    product = add_product('Mage Dwarf 3lvl', game_object)
    add_product_values(product, values_race[0], values_levels[2], values_classes[1])

    product = add_product('Rogue Human 2lvl', game_object)
    add_product_values(product, values_race[2], values_levels[1], values_classes[2])

    product = add_product('Mage Human 3lvl', game_object)
    add_product_values(product, values_race[2], values_levels[2], values_classes[1])

    object = add_object('Item')
    game_object = add_game_object(game, object)
    attributes = add_attribute(game_object, 'Type', 'Level')
    values_types = add_values(attributes[0], 'Weapon', 'Other', 'Clothe')
    values_levels = add_values(attributes[1], '1', '2', '3')

    product = add_product('Dagger+7 2lvl', game_object)
    add_product_values(product, values_types[0], values_levels[1])

    product = add_product('Shield+1 1lvl', game_object)
    add_product_values(product, values_types[2], values_levels[0])

    game = add_game('WorldOfTanks')
    game_object = add_game_object(game, object)



