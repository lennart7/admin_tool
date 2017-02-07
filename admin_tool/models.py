# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Genres(models.Model):
    genre = models.CharField(max_length=99999, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class People(models.Model):
    name = models.CharField(max_length=99999, blank=True, null=True)
    description = models.CharField(max_length=99999, blank=True, null=True)
    wikipedia_id = models.IntegerField(blank=True, null=True)
    freebase = models.CharField(max_length=99999, blank=True, null=True)
    themoviedb = models.IntegerField(blank=True, null=True)
    tvrage = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'people'
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class Movies(models.Model):
    title = models.CharField(max_length=99999, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    release_year = models.IntegerField(blank=True, null=True)
    themoviedb = models.IntegerField(blank=True, null=True)
    original_title = models.CharField(max_length=99999, blank=True, null=True)
    alternative_titles = models.CharField(max_length=99999, blank=True, null=True)
    imdb = models.CharField(max_length=99999, blank=True, null=True)
    pre_order = models.NullBooleanField()
    in_theaters = models.NullBooleanField()
    release_date = models.DateTimeField(blank=True, null=True)
    rating = models.CharField(max_length=99999, blank=True, null=True)
    rottomtomatoes = models.IntegerField(blank=True, null=True)
    freebase = models.CharField(max_length=99999, blank=True, null=True)
    wikipedia_id = models.IntegerField(blank=True, null=True)
    metacritic = models.CharField(max_length=99999, blank=True, null=True)
    common_sense_media = models.CharField(max_length=99999, blank=True, null=True)
    poster_120x171 = models.CharField(max_length=99999, blank=True, null=True)
    poster_240x342 = models.CharField(max_length=99999, blank=True, null=True)
    poster_400x570 = models.CharField(max_length=99999, blank=True, null=True)

    genres = models.ManyToManyField(Genres, related_name='movies', through='GenresMovies')
    people = models.ManyToManyField(People, related_name='movies', through='MoviesPeople')

    class Meta:
        managed = False
        db_table = 'movies'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

# Join Tables
# NOTE the foreign keys did not get set automatically by inspectdb!

class GenresMovies(models.Model):
    genre = models.ForeignKey(Genres, primary_key=True)
    movie = models.ForeignKey(Movies, primary_key=True)

    class Meta:
        managed = False
        db_table = 'genres_movies'


class MoviesPeople(models.Model):
    # eek. django automatically appends _id
    person = models.ForeignKey(People, primary_key=True)
    movie = models.ForeignKey(Movies, primary_key=True)

    class Meta:
        managed = False
        db_table = 'movies_people'


class Users(models.Model):
    name = models.CharField(max_length=99999, blank=True, null=True)
    email = models.CharField(max_length=99999, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    api_key = models.CharField(max_length=99999, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
