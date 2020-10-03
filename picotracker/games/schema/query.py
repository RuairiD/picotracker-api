import graphene
from datetime import timedelta
from django.utils import timezone

from picotracker.games.models import Game
from picotracker.games.schema.types import GameType


TIMEFRAMES = {
    "day": timedelta(days=1),
    "week": timedelta(weeks=1),
    "month": timedelta(days=30),
}


class Query(graphene.ObjectType):
    games = graphene.List(
        GameType,
        sort_method=graphene.String(required=False, default_value="hot"),
    )

    def resolve_games(self, info, sort_method):
        games = Game.objects.filter(
            # Only return games that have at least one star
            # to partly filter the shovelware.
            stars__gte=1,
        )

        if sort_method in TIMEFRAMES:
            latest_datetime = timezone.now() - TIMEFRAMES[sort_method]
            games = games.filter(
                time_created__gte=latest_datetime,
            ).order_by(
                '-stars',
                '-comments',
                '-rating',
            )
        else:
            games = games.order_by(
                '-rating',
                '-stars',
                '-comments',
            )

        games = games.all()[:18]

        return [
            GameType.from_model(game)
            for game in games
        ]
