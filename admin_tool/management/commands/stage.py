import asyncio

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from admin_tool.models import Movie, Show, Episode, WatchList, User, WatchedAt, Collection
from client.guidebox import fetch


class Command(BaseCommand):

    help = "Staging data for US1, US2, and US3"

    def handle(self, *args, **options):
        loop = asyncio.get_event_loop()
        user = stage_or_get_user()
        loop.run_until_complete(stage_us1_data())
        loop.run_until_complete(stage_us2_data(user))
        stage_recently_watched(user)
        loop.run_until_complete(stage_sample_collections())


def stage_or_get_user():
    try:
        user = User(**{'email': 'testuser@test.com',
                       'name': 'Test User',
                       'phone_number': '415-321-1234'})
        user.save()
    except IntegrityError:
        user = User.objects.first()

    return user


async def stage_us1_data():
    """Simple script to stage data for US1.
    See https://vinge-tech-notes.herokuapp.com/user_stories/us01_target_continue_watching.html."""
    US1_shows = ['Billions', 'Mr.Robot', 'Silicon Valley', 'House of Cards',
                 'Veep', 'Suits', 'The Good Wife']

    for show_name in US1_shows:
        params = dict(type='show', field='title', query=show_name)
        result = await fetch('search', params=params)
        # NOTE: this does not account for duplicate records,
        # which exist in guidebox!
        record = result['results'][0]
        record = await fetch('shows/{}'.format(record['id']))
        show_id = record['id']
        show = Show.from_guidebox(**record)

        episodes = await fetch('shows/{}/episodes'.format(show_id), params=dict(limit=50))
        for episode in episodes['results']:
            episode['show'] = show
            episode = Episode.from_guidebox(**episode)
        return show


async def stage_us2_data(user):
    """Stage US2 data.
    See https://vinge-tech-notes.herokuapp.com/user_stories/us02_target_watch_list.html"""
    US2_shows = ['Vikings', 'The Night Of', 'Vice Principals', 'Stranger Things',
                 'Atlanta', 'Narcos']
    US2_movies = ['The Revenant', 'Captain America: Civil War', 'Deadpool', 'The Big Short', 'XMen: Apocalypse']
    watch_list = WatchList(user=user)
    watch_list.save()
    for movie_name in US2_movies:
        params = dict(type='movie', field='title', query=movie_name)
        result = await fetch('search', params=params)
        # NOTE: this does not account for duplicate records,
        # which exist in guidebox!
        if len(result['results']) == 0:
            import ipdb; ipdb.set_trace()  # noqa
        record = result['results'][0]
        movie = Movie.from_guidebox(**record)
        watch_list.movies.add(movie)

    for show_name in US2_shows:
        params = dict(type='show', field='title', query=show_name)
        result = await fetch('search', params=params)
        # NOTE: this does not account for duplicate records,
        # which exist in guidebox!
        record = result['results'][0]
        show = Show.from_guidebox(**record)
        watch_list.shows.add(show)


def stage_recently_watched(user):
    # get random 10 episodes
    # note this can be very slow, but this is just for staging..
    episodes = Episode.objects.order_by('?').all()[:10]
    for episode in episodes:
        WatchedAt.objects.create(user=user,
                                 watchable_id=episode.id,
                                 watchable_type='Episode')
    movies = Movie.objects.order_by('?').all()[:10]
    for movie in movies:
        WatchedAt.objects.create(user=user,
                                 watchable_id=movie.id,
                                 watchable_type='Movie')


async def stage_sample_collections():
    # 80's classics
    # https://projects.invisionapp.com/share/9F7PV02CE#/screens/168435578
    movies = ['Home Alone', 'Batman', 'Hook', 'Gremlins', 'My Girl',
              'The Karate Kid', 'Cool Runnings', 'The NeverEnding Story']
    collection = Collection.objects.create(**{'display_name': "80's classics",
                                              'internal_name': 'a test',
                                              'created_by': 'testuser',
                                              'published': True})
    for index, movie_name in enumerate(movies):
        params = dict(type='movie', field='title', query=movie_name)
        result = await fetch('search', params=params)
        record = result['results'][0]
        movie = Movie.from_guidebox(**record)
        collection.movies.add(movie)
