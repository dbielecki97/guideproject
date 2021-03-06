import django_filters

from .models import Attraction, Category


class AttractionListFilter(django_filters.FilterSet):
    categories = django_filters.ModelChoiceFilter(
        label='Kategoria', queryset=Category.objects.all(), empty_label="wszystkie")

    class Meta:
        model = Attraction
        fields = ['categories']
