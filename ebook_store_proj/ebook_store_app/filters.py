import django_filters
from django_filters import CharFilter

from .models import *


class BookFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Book
        fields = ['title', 'genre_id', 'author_id']
    
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(BookFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['title'].field.widget.attrs.update({'class': 'form-control mr-sm-2', 'placeholder':'Search'})
        self.filters['genre_id'].field.widget.attrs.update({'class':'dropbtn'})
        self.filters['author_id'].field.widget.attrs.update({'class':'dropbtn'})
