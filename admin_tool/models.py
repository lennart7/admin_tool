from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.core.exceptions import FieldDoesNotExist

from mysite.utils import map_guidebox_keys

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


class MediaContent(BaseModel):
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
        return 'MediaContent: %s' % self.original_title


class WatchList(BaseModel):
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    user = models.OneToOneField('User', blank=False, related_name='watch_list', on_delete=models.CASCADE)
    movies = models.ManyToManyField('Movie', blank=True,
                                    through='WatchListMovie', related_name='watch_lists')
    shows = models.ManyToManyField('Show', related_name='watch_lists',
                                   through='WatchListShow', blank=True)
    episodes = models.ManyToManyField('Episode', related_name='watch_lists',
                                      through='WatchListEpisode', blank=True)

    def __str__(self):
        return 'WatchList: %s' % self.user.name

    class Meta:
        verbose_name = 'WatchList'
        verbose_name_plural = 'WatchLists'
        managed = False
        db_table = 'watch_lists'


class WatchListMovie(BaseModel):
    movie = models.ForeignKey("Movie", primary_key=True)
    watch_list = models.ForeignKey(WatchList, primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'movies_watch_lists'


class WatchListEpisode(BaseModel):
    watch_list = models.ForeignKey(WatchList, primary_key=True)
    episode = models.ForeignKey('Episode', primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'episodes_watch_lists'


class WatchListShow(BaseModel):
    watch_list = models.ForeignKey(WatchList, primary_key=True)
    show = models.ForeignKey('Show', primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'shows_watch_lists'


class Collection(BaseModel):
    display_name = models.CharField(max_length=255, blank=True, null=True,
                                    help_text="Public name for the collection")
    internal_name = models.CharField(max_length=255, blank=True, null=True,
                                     help_text="Internal name for the collection")
    created_by = models.CharField(max_length=255, blank=True, null=True)
    published = models.BooleanField(help_text="Whether or not this collection is currently active.")
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
        db_table = 'collection_movies'


class CollectionChildren(BaseModel):
    collection = models.ForeignKey(Collection, primary_key=True)
    child = models.ForeignKey(Collection, primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collection_self_joins'


class CollectionEpisode(BaseModel):
    collection = models.ForeignKey(Collection, primary_key=True)
    episode = models.ForeignKey('Episode', primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collection_episodes'


class CollectionShow(BaseModel):
    collection = models.ForeignKey(Collection, primary_key=True)
    show = models.ForeignKey('Show', primary_key=True)
    order = models.IntegerField()

    # for sortedm2m plugin
    _sort_field_name = 'order'

    class Meta:
        managed = False
        auto_created = True
        db_table = 'collection_shows'


class ContentTag(BaseModel):
    tag = models.CharField(max_length=255, blank=True, null=True,
                           help_text="Public name for the collection")
    movies = SortedManyToManyField('Movie', sorted=False, blank=True,
                                   through='ContentTagMovie', related_name="content_tags")
    episodes = SortedManyToManyField('Episode', sorted=False, blank=True,
                                     through='ContentTagEpisode', related_name="content_tags")
    shows = SortedManyToManyField('Show', sorted=False, blank=True,
                                  through='ContentTagShow', related_name="content_tags")
    collections = SortedManyToManyField('Collection', sorted=False, blank=True,
                                        through='ContentTagCollection', related_name="content_tags")
    guidebox_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return 'Tag: %s' % self.tag

    class Meta:
        verbose_name = 'Content Tag'
        verbose_name_plural = 'Content Tags'
        managed = False
        db_table = 'content_tags'


class ContentTagMovie(BaseModel):
    movie = models.ForeignKey("Movie", primary_key=True)
    content_tag = models.ForeignKey(ContentTag, primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'content_tag_movies'


class ContentTagEpisode(BaseModel):
    episode = models.ForeignKey("Episode", primary_key=True)
    content_tag = models.ForeignKey(ContentTag, primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'content_tag_episodes'


class ContentTagShow(BaseModel):
    show = models.ForeignKey("Show", primary_key=True)
    content_tag = models.ForeignKey(ContentTag, primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'content_tag_shows'


class ContentTagCollection(BaseModel):
    collection = models.ForeignKey("Collection", primary_key=True)
    content_tag = models.ForeignKey(ContentTag, primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'content_tag_collections'


class UserTag(BaseModel):
    tag = models.CharField(max_length=255, blank=True, null=True,
                           help_text="tag name")
    users = SortedManyToManyField('User', sorted=False, blank=True, through='UserTagUsers')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return 'Tag: %s' % self.tag

    class Meta:
        verbose_name = 'User Tag'
        verbose_name_plural = 'User Tags'
        managed = False
        db_table = 'user_tags'


class UserTagUsers(BaseModel):
    user = models.ForeignKey("User", primary_key=True)
    user_tag = models.ForeignKey(UserTag, primary_key=True)

    class Meta:
        managed = False
        auto_created = True
        db_table = 'user_tags_users'


class User(BaseModel):
    email = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return 'User: %s' % self.name


class MediaRecord(BaseModel):

    class Meta:
        abstract = True

    @classmethod
    def from_guidebox(cls, *args, **kwds):
        model_kwds = dict()
        other_kwds = dict()
        for attr, value in map_guidebox_keys(kwds).items():
            try:
                cls._meta.get_field(attr)
                model_kwds[attr] = value
            except FieldDoesNotExist:
                other_kwds[attr] = value

        instance = cls(*args, **model_kwds)
        instance.save()
        if 'tags' in kwds:
            for tag in kwds.get('tags'):
                tag = map_guidebox_keys(tag)
                tag_obj = ContentTag.objects.filter(tag=tag).first()
                if not tag_obj:
                    tag_obj = ContentTag.objects.create(**tag)
                instance.content_tags.add(tag_obj)
        return instance


class Episode(MediaRecord):
    title = models.CharField(max_length=255, blank=True, null=True)
    season_number = models.IntegerField(blank=True, null=True)
    episode_number = models.IntegerField(blank=True, null=True)
    media_content = models.ForeignKey('MediaContent', models.DO_NOTHING, blank=True, null=True)
    show = models.ForeignKey('Show', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episodes'

    def __str__(self):
        return '%s, Episode %s: %s' % (self.show.title, self.episode_number, self.title)


class Movie(MediaRecord):
    title = models.CharField(max_length=255, blank=True, null=True)
    in_theaters = models.NullBooleanField()
    media_content = models.ForeignKey('MediaContent', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'

    def __str__(self):
        return 'Movie: %s' % self.title


class Show(MediaRecord):
    title = models.CharField(max_length=255, blank=True, null=True)
    air_day_of_week = models.CharField(max_length=255, blank=True, null=True)
    air_time = models.CharField(max_length=255, blank=True, null=True)
    media_content = models.ForeignKey('MediaContent', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shows'

    def __str__(self):
        return 'Show: %s' % self.title


class WatchedAt(BaseModel):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE,
                             related_name='watched_ats')
    watchable_type = models.CharField(max_length=20, blank=False, null=False)
    watchable_id = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'watched_ats'

    def __str__(self):
        return 'WatchedAt %s: %s' % (self.watchable_type, self.watchable_id)
