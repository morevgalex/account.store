from django.db import models


class User(models.Model):
    login = models.CharField(verbose_name='Логин', max_length=32, unique=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    sha_password = models.CharField(verbose_name='Пароль', max_length=64)
    role = models.ForeignKey('Role', verbose_name='Роль', on_delete=models.PROTECT)

    def __str__(self):
        return self.login


class Seller(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.login


class Role(models.Model):
    ROLES = ((0, 'admin'),
             (1, 'moderator'),
             (2, 'user'),
             (3, 'seller'))
    role = models.IntegerField(verbose_name='Роль', choices=ROLES, unique=True)

    permission = models.OneToOneField('Permission', verbose_name='Разрешения', null=True, blank=True,
                                      on_delete=models.PROTECT)

    def __str__(self):
        return self.role


class Permission(models.Model):
    pass
    # TODO


class Session(models.Model):
    key = models.CharField(verbose_name='Key', max_length=256, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired = models.DateTimeField()
