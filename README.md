# Picotracker (API)

Picotracker provides an alternative sorting system to the Lexaloffle BBS. Instead of sorting games forum-style where any game can be bumped to the top of the list with a new comment, Picotracker prioritises games based on their BBS engagement (likes and comments), while penalising older games by reducing a game's rating based on how many days have elapsed since its release.

Ratings are calculated using the following formula, where `t` is the number of days since the game's release.

<img src="https://latex.codecogs.com/gif.latex?rating&space;=&space;\frac{(likes&space;+&space;\frac{comments}{10})}{1.2&space;^&space;t}" title="rating = \frac{(likes + \frac{comments}{10})}{1.2 ^ t}" alt="rating = (likes + comments/10)/(1.2 ^ t)" />

## Running
This is a pretty standard Django project for the most part. As-is, it is designed to be run on Heroku, but setting `DEBUG = True` in `settings.py` will allow it to run on `localhost` with a sqlite DB. Run these inside a python3 virtualenv:

 1. `pip install -r requirements.txt # Install dependencies`
 2. `python manage.py migrate # Create database tables`
 3. `python manage.py runserver # Done.`

## API
Everything is served from a single `/graphql` endpoint with a single query: `games`. A query retrieving everything available would look like:

```
query Games($sortMethod: String) {
    games(sortMethod: $sortMethod) {
        bbsId
        name
        stars
        comments
        timeCreated
        imageUrl
        tags
        developer {
            bbsId
            username
        }
    }
}
```

where `sortMethod` is one of `hot` (for weighted rankings), `day`, `week` or `month` (for highest engagement in the given time period, without any weighting).

## Scheduled Jobs
A combination of `apscheduler` and `django_apscheduler` are used to update the games in the database every 3 hours.

----

The frontend portion of "Picotracker" can be found [here](https://github.com/ruairid/picotracker-web).
