from django.contrib import admin

from admin_tool import models, forms


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    form = forms.CollectionForm
    list_display = ['display_name', 'internal_name', 'created_by', 'published', 'updated_at']
    # list_filter = ['created_by', 'published']
    search_fields = ['display_name', 'internal_name', 'created_by']
    readonly_fields = ['created_by', 'updated_at', 'created_at']

    def get_fieldsets(self, request, obj=None):
        """Don't show readonly fields on create"""
        fieldsets = super(CollectionAdmin, self).get_fieldsets(request, obj)
        if not obj:
            fields = fieldsets[0][1]['fields']
            fields = filter(lambda x: x not in self.readonly_fields, fields)
            fieldsets[0][1]['fields'] = fields
        return fieldsets

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ['media_content', 'show', 'episode_number', 'season_number']


@admin.register(models.Movie)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ['media_content']


@admin.register(models.Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ['media_content']
