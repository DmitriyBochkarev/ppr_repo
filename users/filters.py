import django_filters
from . models import Worker, Client


class WorkerFilter(django_filters.FilterSet):
    class Meta:
        model = Worker
        fields = {
            'rating': ['lt', 'gt'],            # Фильтры по рейтингу
        }

    sort_by = django_filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('-rating', '-rating'),
        )
    )

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'rating': ['lt', 'gt'],            # Фильтры по рейтингу
        }

    sort_by = django_filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('-rating', '-rating'),
        )
    )