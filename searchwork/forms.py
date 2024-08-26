from django import forms

CATEGORY_CHOICES = (
    ('Любой', 'Любой'),
    ('Земля', 'Земля'),
    ('Канашка', 'Канашка'),
    ('Вода', 'Вода'),
    ('Электрика', 'Электрика'),
)

TYPE_CHOICES = (
    ('Любой', 'Любой'),
    ('Исполнительная документация', 'Исполнительная документация'),
    ('Проектная/рабочая документация', 'Проектная/рабочая документация'),
    ('ПОС', 'ПОС'),
    ('ППР/ППРК', 'ППР/ППРК'),
    ('Геодезия', 'Геодезия'),
)


class FilterForm(forms.Form):
    # Форма фильтров
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    type = forms.ChoiceField(choices=TYPE_CHOICES)
