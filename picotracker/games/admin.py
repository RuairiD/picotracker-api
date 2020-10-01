from django.contrib import admin
from picotracker.games.models import Game
from picotracker.games.models import Developer


class GameAdmin(admin.ModelAdmin):
    pass


class DeveloperAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Developer, DeveloperAdmin)
