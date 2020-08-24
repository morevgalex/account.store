from django.db import models


class Game(models.Model):
    title = models.CharField(verbose_name='Название', max_length=128, db_index=True, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    slug = models.SlugField(verbose_name='slug', max_length=32, unique=True)
    g_objects = models.ManyToManyField('Object',
                                     through='Game_Object',
                                     verbose_name='Объекты')

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['title']

    def __str__(self):
        return self.title


class Object(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128, unique=True, db_index=True)
    plural_name = models.CharField(verbose_name='Множ. число', max_length=128)
    slug = models.SlugField(verbose_name='slug', max_length=32, unique=True)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Game_Object(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, verbose_name = 'Игра', db_index=True)
    object = models.ForeignKey(Object, on_delete=models.PROTECT, verbose_name='Объект', db_index=True)

    class Meta:
        unique_together = (('game', 'object'), )
        verbose_name = 'Игра и объект'
        verbose_name_plural = 'Игры и объекты'
        ordering = ['game', 'object']

    def __str__(self):
        return f'{self.game} - {self.object}'


class Attribute(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128, db_index=True)
    game_object = models.ForeignKey(Game_Object, on_delete=models.PROTECT, verbose_name='Объект игры')

    TYPES = (
        ('str', 'Строка'),
        ('int', 'Целое число'),
        ('float', 'Число с плавающей точкой'),
    )
    typeof = models.CharField(verbose_name='Тип аттрибута', max_length=16, choices=TYPES)

    ANSWERS = (
        (True, 'Да'),
        (False, 'Нет'),
    )
    is_predefined = models.BooleanField(verbose_name='Предопределенный атрибут?', choices=ANSWERS)

    class Meta:
        unique_together = (('name', 'game_object'),)
        verbose_name = 'Аттрибут объекта игры'
        verbose_name_plural = 'Аттрибуты объекта игры'

    def __str__(self):
        return f'{self.game_object} - {self.name}'


class Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT, verbose_name='Аттрибут')
    value = models.CharField(verbose_name='Значение', max_length=64, blank=True, null=True)

    class Meta:
        unique_together = (('attribute', 'value'),)
        verbose_name = 'Значение аттрибута объекта игры'
        verbose_name_plural = 'Значения аттрибута объекта игры'

    def __str__(self):
        return f'{self.attribute} - {self.value}'


class Product(models.Model):
    title = models.CharField(verbose_name='Название', max_length=64)
    game_object = models.ForeignKey(Game_Object, on_delete=models.PROTECT, verbose_name='Объект игры')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    values = models.ManyToManyField(Value,
                                    through='Product_Value',
                                    verbose_name='Значения')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Товар {self.game_object} - id({self.pk})'


class Product_Value(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    value = models.ForeignKey(Value, on_delete=models.CASCADE, verbose_name='Значение')

    class Meta:
        unique_together = (('product', 'value'), )
        verbose_name = 'Товар_Значение'
        verbose_name_plural = 'Товары_Значения'

    def __str__(self):
        return f'{self.product} - {self.value}'
