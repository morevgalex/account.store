from django.contrib import admin
from .models import *


class GameAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class ObjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class Game_ObjectAdmin(admin.ModelAdmin):
    list_display = ('game', 'object',)
    list_display_links = ('game', 'object',)
    search_fields = ('game__title', 'object__name',)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('game_object', 'name',)
    list_display_links = ('game_object', 'name',)
    search_fields = ('game_object__game__title', 'game_object__object__name', 'name')


class ValueAdmin(admin.ModelAdmin):
    search_fields = ('attribute__game_object__game__title',
                     'attribute__game_object__object__name',
                     'attribute__name', 'value')


admin.site.register(Game, GameAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Game_Object, Game_ObjectAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(Product)
admin.site.register(Product_PreValue)
