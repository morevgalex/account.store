from django.contrib import admin
from .models import *

class GameAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)


class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(Game, GameAdmin)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Game_Object)
admin.site.register(Attribute)
admin.site.register(Value)
admin.site.register(Product)
# admin.site.register(Game)
