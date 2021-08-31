from django_filters import rest_framework as rf_filter
from .models import Movie

def get_client_ip(request):
    """Получение ip пользователя"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(rf_filter.BaseInFilter, rf_filter.CharFilter):
    pass


class MovieFilter(rf_filter.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__name', lookup_expr='in')
    year = rf_filter.RangeFilter()

    class Meta:
        model = Movie
        fields = ('genres', 'year', 'category')