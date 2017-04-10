from __future__ import unicode_literals

from django.utils import timezone
from django.db import models

from sortedm2m.fields import SortedManyToManyField


class BaseModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id and hasattr(self, 'created_at'):
            self.created_at = timezone.now()
        if hasattr(self, 'updated_at'):
            self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class Collection(BaseModel):
    display_name = models.CharField(max_length=255, blank=True, null=True,
                                    help_text="Public name for the collection")
    internal_name = models.CharField(max_length=255, blank=True, null=True,
                                     help_text="Internal name for the collection")
    created_by = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(help_text="Whether or not this collection is currently active.")
    # have django update these on modify / add
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    movies = SortedManyToManyField('Movie', sort_value_field_name='order', blank=True,
                                   through='CollectionMovie', related_name='collections')
    shows = SortedManyToManyField('Show', sort_value_field_name='order', related_name='collections',
                                   through='CollectionShow', blank=True)
    episodes = SortedManyToManyField('Episode', sort_value_field_name='order', related_name='collections',
                                     through='CollectionEpisode', blank=True)
    collections = SortedManyToManyField('Collection', sort_value_field_name='order', related_name='parents',
                                        through='CollectionChildren', blank=True)

    def __str__(self):
        return 'Collection: %s created_by: %s' % (self.display_name, self.created_by)

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
        managed = False
        db_table = 'collections'


class CollectionMovie(BaseModel):
    movie = models.ForeignKey("Movie", primary_key=True)
    collection = models.ForeignKey(Collection, primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collections_movies'


class CollectionChildren(BaseModel):
    collection = models.ForeignKey(Collection, primary_key=True)
    child = models.ForeignKey(Collection, primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collections_self_join'


class CollectionEpisode(BaseModel):
    collection = models.ForeignKey(Collection, primary_key=True)
    episode = models.ForeignKey('Episode', primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collections_episodes'


class CollectionShow(BaseModel):
    collection = models.ForeignKey(Collection, primary_key=True)
    show = models.ForeignKey('Show', primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collections_shows'


class Episode(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    season_number = models.IntegerField(blank=True, null=True)
    episode_number = models.IntegerField(blank=True, null=True)
    media_content = models.ForeignKey('MediaContents', models.DO_NOTHING, blank=True, null=True)
    show = models.ForeignKey('Show', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episodes'

    def __str__(self):
        return '%s, Episode %s: %s' % (self.show.title, self.episode_number, self.title)


class Movie(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    in_theaters = models.NullBooleanField()
    media_content = models.ForeignKey('MediaContents', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'

    def __str__(self):
        return 'Movie: %s' % self.title


class Show(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    air_day_of_week = models.CharField(max_length=255, blank=True, null=True)
    air_time = models.CharField(max_length=255, blank=True, null=True)
    media_content = models.ForeignKey('MediaContents', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shows'

    def __str__(self):
        return 'Show: %s' % self.title


class MediaContents(BaseModel):
    original_title = models.CharField(max_length=255, blank=True, null=True)
    alternative_titles = models.TextField(blank=True, null=True)  # This field type is a guess.
    overview = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)
    guidebox_id = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    imdb_id = models.CharField(max_length=255, blank=True, null=True)
    rottentomatoes = models.CharField(max_length=255, blank=True, null=True)
    maturity_rating = models.CharField(max_length=255, blank=True, null=True)
    wikipedia_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'media_contents'

    def __str__(self):
        return 'MediaContents: %s' % self.original_title


class User(BaseModel):
    email = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
