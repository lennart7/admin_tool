from django.contrib import admin

from admin_tool import models, forms


@admin.register(models.ContentList)
class ContentListAdmin(admin.ModelAdmin):
    form = forms.ContentListForm
    list_display = ('name',)
    exclude = ['curated', 'type']
    filter_horizontal = ('movies',)

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
#
#class ContentListMovieInline(admin.TabularInline):
#    form = forms.MovieForm
#    model = models.ContentListMovie
#    fk_name = 'content_list'
