import django_filters
from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Author
from django import forms

class PostFilter(FilterSet):
    title = CharFilter(
        label='Заголовок',
        lookup_expr='iregex')

    authorship = ModelChoiceFilter(
        empty_label='Все авторы',
        label='Автор',
        queryset=Author.objects.all())

    date = django_filters.DateFilter(
        field_name='publication_time',
        widget=forms.DateInput(attrs={'type':'date'}),
        label='Дата',
        lookup_expr='date__gte')

