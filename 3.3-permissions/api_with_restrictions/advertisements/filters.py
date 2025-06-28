from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # Фильтр по дате создания: от-до
    created_at = DateFromToRangeFilter()

    # Фильтр по статусу: OPEN / CLOSED
    status = filters.CharFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status']
