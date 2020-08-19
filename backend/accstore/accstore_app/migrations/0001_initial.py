# Generated by Django 3.1 on 2020-08-17 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Название')),
                ('is_predefined', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], verbose_name='Предопределенный атрибут?')),
            ],
            options={
                'verbose_name': 'Аттрибут объекта игры',
                'verbose_name_plural': 'Аттрибуты объекта игры',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('slug', models.SlugField(max_length=32, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Game_Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accstore_app.game', verbose_name='Игра')),
            ],
            options={
                'verbose_name': 'Игра и объект',
                'verbose_name_plural': 'Игры и объекты',
                'ordering': ['game', 'object'],
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Название')),
                ('plural_name', models.CharField(max_length=128, verbose_name='Множ. число')),
                ('slug', models.SlugField(max_length=32, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('game_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accstore_app.game_object', verbose_name='Объект игры')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=64, null=True, verbose_name='Значение')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accstore_app.attribute', verbose_name='Аттрибут')),
            ],
            options={
                'verbose_name': 'Значение аттрибута объекта игры',
                'verbose_name_plural': 'Значения аттрибута объекта игры',
                'unique_together': {('attribute', 'value')},
            },
        ),
        migrations.CreateModel(
            name='Product_Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accstore_app.product', verbose_name='Товар')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accstore_app.value', verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Товар_Значение',
                'verbose_name_plural': 'Товары_Значения',
            },
        ),
        migrations.AddField(
            model_name='game_object',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accstore_app.object', verbose_name='Объект'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='game_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accstore_app.game_object', verbose_name='Объект игры'),
        ),
        migrations.AlterUniqueTogether(
            name='game_object',
            unique_together={('game', 'object')},
        ),
    ]
