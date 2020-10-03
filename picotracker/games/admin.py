from django.contrib import admin
from picotracker.games.models import Game
from picotracker.games.models import Developer


class GameAdmin(admin.ModelAdmin):
    search_fields = ['developer__username']
    list_display = (
        'name',
        'stars',
        'comments',
        'rating',
        'time_created',
    )


class DeveloperAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Developer, DeveloperAdmin)
