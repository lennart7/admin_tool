from django.contrib import admin

from admin_tool import models


class ContentListMovieInline(admin.TabularInline):
    model = models.ContentListMovie
    extra = 1
    readonly_fields = ['movie_title']
    def movie_title(self, instance):
        return instance.movie.title


@admin.register(models.ContentList)
class ContentListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ['curated', 'type']
    inlines = [ContentListMovieInline]

    readonly_fields = ['updated_at', 'created_at']


@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(models.Movie)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(models.Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title',)
#
#
# class GenresMoviesInline(admin.TabularInline):
#     # TODO: this should not be necessary, we should just
#     # be able to specify the join table in the models def,
#     # without using "through" since Genre-Movies doesn't have any
#     # extra carried attributes
#     model = models.GenresMovies
#     extra = 1
#     readonly_fields = ['genre_name']
#     def genre_name(self, instance):
#         return instance.genre.genre
