import django_filters
from django_filters import FilterSet
from .models import Post
from django import forms

class PostFilter(FilterSet):
    date = django_filters.DateFilter(
    field_name='publication_time',
    widget=forms.DateInput(attrs={'type':'date'}),
    label='Date', lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {
           'title': ['icontains'],
           'authorship': ['exact'],
       }
