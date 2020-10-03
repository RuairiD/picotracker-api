import json
import math
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from pyquery import PyQuery

from picotracker.games.models import Developer
from picotracker.games.models import Game

BBS_URL = 'https://www.lexaloffle.com/bbs/lister.php?use_hurl=1&cat=7&sub=0&page={page}&mode=&sub=2'
MAX_PAGES = 3

class Command(BaseCommand):
    """
    """
    help = "Update games in database from BBS."

    def add_arguments(self, parser):
        pass

    def update_game_rating(self, game):
        days_since_release = (timezone.now() - game.time_created).days
        if days_since_release < 1:
            days_since_release = 1
        rating = (game.stars + 0.1 * game.comments) / (1.1 ** days_since_release)
        game.rating = rating
        game.save()

    def update_game_from_data(self, game_data):
        bbs_id = int(game_data[0])
        name = game_data[2]
        stars = int(game_data[12])
        comments = int(game_data[13])
        image_url = game_data[3]

        time_created_raw = game_data[6]
        time_created_unaware = datetime.strptime(time_created_raw, '%Y-%m-%d %H:%M:%S')
        time_created = timezone.now().tzinfo.localize(time_created_unaware)

        developer_bbs_id = int(game_data[7])
        developer_username = game_data[8]

        # If image_url is not a proper thumbail, thread does not contain a cart
        # and should be ignored.
        if "/bbs/thumbs" not in image_url:
            return

        print(bbs_id, name, stars, comments, image_url, time_created, developer_bbs_id, developer_username)

        developer = Developer.objects.filter(bbs_id=developer_bbs_id).first()
        if not developer:
            developer = Developer(
                bbs_id=developer_bbs_id,
                username=developer_username,
            )
        developer.save()

        game = Game.objects.filter(bbs_id=bbs_id).first()
        if not game:
            game = Game(
                bbs_id=bbs_id,
                name=name,
                comments=comments,
                stars=stars,
                image_url=image_url,
                time_created=time_created,
                developer=developer,
            )
        else:
            game.name = game.name
            game.comments = game.comments
            game.stars = stars
            game.comments = comments
            game.image_url = image_url
            game.time_created = time_created
            game.developer = developer
        game.save()

    def handle(self, *args, **options):
        for page in range(1, MAX_PAGES + 1):
            tree = PyQuery(url=BBS_URL.format(page=page))
            # Converting Javascript to Python for the mentally feeble.
            games_data = json.loads(
                tree.text().split('pdat=')[1].split('; var')[0].replace("`", "'").replace(",]", "]").replace("['",'["').replace("',",'",').replace(", '",', "').replace(",'",',"').replace("']",'"]').replace(",,",",").replace("], ]", "] ]"),
            )
            for game_data in games_data:
                self.update_game_from_data(game_data)

        # Update ratings for all games
        for game in Game.objects.all():
            self.update_game_rating(game)

