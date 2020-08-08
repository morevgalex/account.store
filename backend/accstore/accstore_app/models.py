from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=128, db_index=True)
    description = models.TextField(null=True, blank=True)

class Object(models.Model):
    name = models.CharField(max_length=128, primary_key=True, db_index=True)

class Game_Object(models.Model):
    pass

class Attribute(models.Model):
    pass

class Value(models.Model):
    pass

class Product(models.Model):
    pass