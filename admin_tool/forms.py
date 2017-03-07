from django import forms

from admin_tool import models

from django.contrib.admin.widgets import FilteredSelectMultiple


class ContentListForm(forms.ModelForm):
    class Meta:
        model = models.ContentList
        fields = '__all__'

    movies = forms.ModelMultipleChoiceField(
        queryset=models.Movie.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Movies',
            is_stacked=False
        )
    )
    shows = forms.ModelMultipleChoiceField(
        queryset=models.Show.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Shows',
            is_stacked=False
        )
    )
    episodes = forms.ModelMultipleChoiceField(
        queryset=models.Episode.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Episodes',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(ContentListForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['movies'].initial = self.instance.movies.all()
            self.fields['shows'].initial = self.instance.shows.all()
            self.fields['episodes'].initial = self.instance.episodes.all()

    def save(self, commit=True):
        content_list = super(ContentListForm, self).save(commit=False)
        if commit:
            content_list.save()

        if content_list.pk:
            content_list.movies = self.cleaned_data['movies']
            content_list.shows = self.cleaned_data['shows']
            content_list.episodes = self.cleaned_data['episodes']
            self.save_m2m()

        return content_list

