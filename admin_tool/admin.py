from django.contrib import admin

from admin_tool.models import Genres, People, Movies


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('genre',)


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'rating')
