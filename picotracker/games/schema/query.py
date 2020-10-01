import graphene

from picotracker.games.models import Game
from picotracker.games.schema.types import GameType


class Query(graphene.ObjectType):
    games = graphene.List(GameType)

    def resolve_games(self, info):
        games = Game.objects.order_by(
            '-rating'
        ).all()[:9]

        return [
            GameType.from_model(game)
            for game in games
        ]
