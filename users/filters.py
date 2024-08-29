import django_filters
from . models import Worker


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
