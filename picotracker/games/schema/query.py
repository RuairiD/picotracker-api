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
        timeframe=graphene.String(required=False, default_value="week"),
    )

    def resolve_games(self, info, timeframe):
        latest_datetime = timezone.now() - TIMEFRAMES[timeframe]

        import time; time.sleep(1)

        games = Game.objects.filter(
            time_created__gte=latest_datetime,
            # Only return games that have at least one star
            # to partly filter the shovelware.
            stars__gte=1,
        ).order_by(
            '-rating'
        ).all()[:18]

        return [
            GameType.from_model(game)
            for game in games
        ]
