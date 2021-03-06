from django.contrib import admin

from admin_tool import models, forms


class BaseAdmin(admin.ModelAdmin):
    """Common behavior such as removing readonly fields from create"""

    def get_fieldsets(self, request, obj=None):
        """Don't show readonly fields on create"""
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            fields = fieldsets[0][1]['fields']
            fields = filter(lambda x: x not in self.readonly_fields, fields)
            fieldsets[0][1]['fields'] = fields
        return fieldsets


@admin.register(models.Collection)
class CollectionAdmin(BaseAdmin):
    form = forms.CollectionForm
    list_display = ['display_name', 'internal_name', 'created_by', 'published', 'updated_at']
    # list_filter = ['created_by', 'published']
    search_fields = ['display_name', 'internal_name', 'created_by']
    readonly_fields = ['created_by', 'updated_at', 'created_at']

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form


@admin.register(models.ContentTag)
class ContentTagAdmin(BaseAdmin):
    form = forms.ContentTagForm
    list_display = ['tag', 'created_at']
    readonly_fields = ['updated_at', 'created_at']

    class Meta:
        model = models.ContentTag
        fields = '__all__'


@admin.register(models.UserTag)
class UserTagAdmin(BaseAdmin):
    form = forms.UserTagForm
    list_display = ['tag', 'created_at']
    readonly_fields = ['updated_at', 'created_at']

    class Meta:
        model = models.ContentTag
        fields = '__all__'


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


class WatchedAtInline(admin.StackedInline):
    model = models.WatchedAt
    readonly_fields = ['created_at', 'content']
    fields = ['created_at', 'content']
    # don't show extra records
    extra = 0

    def has_add_permission(self, request):
        return False

    def content(self, obj):
        """Custom inline which displays the title and content type of the
        watched content"""
        types = {'Episode': models.Episode, 'Movie': models.Movie}
        if not obj.id:
            return ''
        target = types[obj.watchable_type]
        res = target.objects.get(pk=obj.watchable_id)
        return '{}: {}'.format(obj.watchable_type, res.title)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number')
    readonly_fields = ['created_at', 'updated_at']
    inlines = [WatchedAtInline]
