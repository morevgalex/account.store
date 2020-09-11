from django.db import models

from accstore_app.models_pack.models_items import Product
from accstore_app.models_pack.models_user import User


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.PROTECT)

    STATUSES = ((0, 'active'),
                (1, 'done'),
                (2, 'in_dispute'))
    status = models.CharField(verbose_name='Статус', choices=STATUSES, max_length=32)


class Dispute(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.PROTECT)

    STATUSES = ((0, 'opened'),
                (1, 'closed'),)
    status = models.CharField(verbose_name='Статус', choices=STATUSES, max_length=32)


class Chat(models.Model):
    id = models.AutoField(primary_key=True)


class AbstractChat(models.Model):
    chat = models.OneToOneField(Chat, verbose_name='Чат', on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class PersonalChat(AbstractChat):
    pass


class GlobalChat(AbstractChat):
    moderators = models.ManyToManyField(User)


class ModeredPersonalChat(AbstractChat):
    moderators = models.ManyToManyField(User)


class Message(models.Model):
    text = models.CharField(verbose_name='Текст', max_length=256)
    chat = models.ForeignKey(Chat, verbose_name='Чат', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)