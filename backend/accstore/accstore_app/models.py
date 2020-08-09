from django.db import models


class Game(models.Model):
    title = models.CharField(verbose_name='Название', primary_key=True, max_length=128, db_index=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    slug = models.SlugField(verbose_name='slug', max_length=32, unique=True)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['title']

    def __str__(self):
        return self.title


class Object(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128, primary_key=True, db_index=True)
    plural_name = models.CharField(verbose_name='Множ. число', max_length=128)
    slug = models.SlugField(verbose_name='slug', max_length=32, unique=True)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Game_Object(models.Model):
    game_title = models.ForeignKey(Game, on_delete=models.PROTECT, verbose_name = 'Игра', db_index=True)
    object_name = models.ForeignKey(Object, on_delete=models.PROTECT, verbose_name='Объект', db_index=True)

    class Meta:
        unique_together = (('game_title', 'object_name'),)
        verbose_name = 'Игра и объект'
        verbose_name_plural = 'Игры и объекты'
        ordering = ['game_title', 'object_name']

    def __str__(self):
        return f'{self.game_title} {self.object_name}'


class Attribute(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128, db_index=True)
    game_object_id = models.ForeignKey(Game_Object, on_delete=models.PROTECT, verbose_name='Объект игры')

    TYPES = (
        ('int', 'Число'),
        ('float', 'Дробный'),
        ('string', 'Строка'),
        ('bool', 'Булево'),
        ('date', 'Дата'),
    )
    type_of = models.CharField(verbose_name='Тип', max_length=16, choices=TYPES)

    ANSWERS = (
        (True, 'Да'),
        (False, 'Нет'),
    )
    is_predefined = models.BooleanField(verbose_name='Предопределенный атрибут?', choices=ANSWERS)

    class Meta:
        verbose_name = 'Аттрибут объекта игры'
        verbose_name_plural = 'Аттрибуты объекта игры'

    def __str__(self):
        return f'{self.game_object_id} {self.name} {self.type_of}'


class Value(models.Model):
    attribute_id = models.ForeignKey(Attribute, on_delete=models.PROTECT, verbose_name='Аттрибут')
    string_value = models.CharField(verbose_name='Строковое значение', max_length=64, blank=True, null=True)
    integer_value = models.IntegerField(verbose_name='Целое значение', blank=True, null=True)
    float_value = models.FloatField(verbose_name='Дробное значение', blank=True, null=True)
    bool_value = models.BooleanField(verbose_name='Булево значение', blank=True, null=True)
    date_value = models.DateField(verbose_name='Дата', blank=True, null=True)

    class Meta:
        verbose_name = 'Значение аттрибута объекта игры'
        verbose_name_plural = 'Значения аттрибута объекта игры'

    def __str__(self):
        return f'{self.attribute_id} {self.string_value or self.integer_value or self.float_value or self.bool_value or self.date_value}'


class Product(models.Model):
    game_object_id = models.ForeignKey(Game_Object, on_delete=models.PROTECT, verbose_name='Объект игры')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Товар {self.game_object_id} id({self.pk})'


class Product_Value(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    value_id = models.ForeignKey(Value, on_delete=models.CASCADE, verbose_name='Значение')

    class Meta:
        verbose_name = 'Товар_Значение'
        verbose_name_plural = 'Товары_Значения'

    def __str__(self):
        return f'{self.value_id}'
