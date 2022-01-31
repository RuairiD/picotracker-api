import json
import math
from datetime import datetime
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from pyquery import PyQuery

from picotracker.games.models import Developer
from picotracker.games.models import Game
from picotracker.games.models import Tag


MAX_AGE = timedelta(days=365)


class Command(BaseCommand):
    """
    Delete games that are over MAX_AGE old since these games will not appear in the Hot list and
    do not need to be tracked.
    """
    help = "Delete old games from the database."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        datetime_threshold = timezone.now() - MAX_AGE
        Game.objects.filter(
            time_created__lte=datetime_threshold
        ).delete()
        # Also delete developers for whom all of their games have been deleted.
        Developer.objects.filter(
            games__isnull=True
        ).delete()
