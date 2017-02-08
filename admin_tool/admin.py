from django.contrib import admin

from admin_tool import models


@admin.register(models.Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('genre',)


@admin.register(models.People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PeopleMoviesInline(admin.TabularInline):
    model = models.MoviesPeople
    extra = 1


class GenresMoviesInline(admin.TabularInline):
    # TODO: this should not be necessary, we should just
    # be able to specify the join table in the models def,
    # without using "through" since Genre-Movies doesn't have any
    # extra carried attributes
    model = models.GenresMovies
    extra = 1


@admin.register(models.Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating')
    # inlines = (GenresMoviesInline, PeopleMoviesInline)
