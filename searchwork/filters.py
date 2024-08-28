import django_filters
from . models import Task

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'budget': ['lt', 'gt'],            # Фильтры по цене
            'category': ['exact', 'icontains'],
            'type': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
        }

    sort_by = django_filters.OrderingFilter(
        fields=(
            ('budget', 'budget'),
            ('-budget', '-budget'),
            ('date-posted', 'date-posted'),

            ('-date-posted', '-date-posted'),
        )
    )