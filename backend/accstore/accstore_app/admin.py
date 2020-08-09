from django.contrib import admin
from .models import *

class GameAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class ObjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class Game_ObjectAdmin(admin.ModelAdmin):
    list_display = ('game_title', 'object_name',)
    list_display_links = ('game_title', 'object_name',)
    search_fields = ('game_title__title', 'object_name__name',)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('game_object_id', 'name',)
    list_display_links = ('game_object_id', 'name',)
    search_fields = ('game_object_id__game_title__title', 'game_object_id__object_name__name', 'name')


class ValueAdmin(admin.ModelAdmin):
    search_fields = ('attribute_id__game_object_id__game_title__title',
                     'attribute_id__game_object_id__object_name__name',
                     'attribute_id__name',)



admin.site.register(Game, GameAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Game_Object, Game_ObjectAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(Product)
admin.site.register(Product_Value)
