from django import forms

from admin_tool import models

from sortedm2m.forms import SortedMultipleChoiceField


class BaseForm(forms.ModelForm):
    """Base form to allow us to pass a "required" argument
    into a field constructor. See the CollectionForm display_name field."""
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"


class ContentTagForm(BaseForm):
    tag = forms.CharField(required=True)
    movies = SortedMultipleChoiceField(
        queryset=models.Movie.objects.all(),
        required=False,
    )
    shows = SortedMultipleChoiceField(
        queryset=models.Show.objects.all(),
        required=False,
    )
    episodes = SortedMultipleChoiceField(
        queryset=models.Episode.objects.all(),
        required=False,
    )
    collections = SortedMultipleChoiceField(
        queryset=models.Collection.objects.all(),
        required=False,
    )


class UserTagForm(BaseForm):
    tag = forms.CharField(required=True)
    users = SortedMultipleChoiceField(
        queryset=models.User.objects.all(),
        required=False,
    )


class CollectionForm(BaseForm):

    class Meta:
        model = models.Collection
        fields = '__all__'

    display_name = forms.CharField(required=True)
    internal_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['movies'].initial = self.instance.movies.all()
            self.fields['shows'].initial = self.instance.shows.all()
            self.fields['episodes'].initial = self.instance.episodes.all()
            self.fields['collections'].initial = self.instance.collections.all()

    def clean(self, *args, **kwds):
        """Before saving relationships, make sure we have no mixed
        content types, as it is unclear how to implement this via django forms.
        Collections also can't contain themselves."""
        super().clean(*args, **kwds)
        if sum([(len(self.cleaned_data[attr]) > 0) for attr in
                ['movies', 'shows', 'episodes', 'collections']]) > 1:
            raise forms.ValidationError("""Mixed content types are currently not supported. \
    The collection may only have one of the following different types: 'movies', 'shows', 'episodes', 'collections'.""")
        if self.instance in self.cleaned_data['collections']:
            raise forms.ValidationError("""A collection cannot contain itself!""")

    def save(self, commit=True):
        collection = super(CollectionForm, self).save(commit=False)

        if not collection.id and self.current_user:
            if self.current_user.first_name or self.current_user.last_name:
                collection.created_by = self.current_user.first_name + self.current_user.last_name
            else:
                collection.created_by = self.current_user.username

        if commit:
            collection.save()

        if collection.pk:
            collection.movies = self.cleaned_data['movies']
            collection.shows = self.cleaned_data['shows']
            collection.episodes = self.cleaned_data['episodes']
            collection.collections = self.cleaned_data['collections']
            self.save_m2m()

        return collection
