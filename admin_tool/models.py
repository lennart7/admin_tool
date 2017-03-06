from __future__ import unicode_literals
from django.utils import timezone

from django.db import models


class ContentList(models.Model):
    curated = models.NullBooleanField()
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    # have django update these on modify / add
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    movies = models.ManyToManyField('Movie', related_name='content_lists', through='ContentListMovie')
    shows = models.ManyToManyField('Show', related_name='content_lists', through='ContentListShow')
    episodes= models.ManyToManyField('Episode', related_name='content_lists', through='ContentListEpisode')

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        self.modified = timezone.now()
        return super(ContentList, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Content List'
        verbose_name_plural = 'Content Lists'
        managed = False
        db_table = 'content_lists'


class ContentListEpisode(models.Model):
    content_list = models.ForeignKey(ContentList, primary_key=True)
    episode = models.ForeignKey('Episode', primary_key=True)

    class Meta:
        managed = False
        db_table = 'content_lists_episodes'


class ContentListMovie(models.Model):
    content_list = models.ForeignKey(ContentList, primary_key=True)
    movie = models.ForeignKey('Movie', primary_key=True)

    class Meta:
        managed = False
        db_table = 'content_lists_movies'


class ContentListShow(models.Model):
    content_list = models.ForeignKey(ContentList, primary_key=True)
    show = models.ForeignKey('Show', primary_key=True)

    class Meta:
        managed = False
        db_table = 'content_lists_shows'


class Episode(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    season_number = models.IntegerField(blank=True, null=True)
    episode_number = models.IntegerField(blank=True, null=True)
    media_content = models.ForeignKey('MediaContents', models.DO_NOTHING, blank=True, null=True)
    show = models.ForeignKey('Show', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episodes'


class MediaContents(models.Model):
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


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    in_theaters = models.NullBooleanField()
    media_content = models.ForeignKey(MediaContents, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class Show(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    air_day_of_week = models.CharField(max_length=255, blank=True, null=True)
    air_time = models.CharField(max_length=255, blank=True, null=True)
    media_content = models.ForeignKey(MediaContents, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shows'


class User(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
