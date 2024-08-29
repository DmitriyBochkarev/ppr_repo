from django import forms

# CATEGORY_CHOICES = (
#     ('Любой', 'Любой'),
#     ('Земля', 'Земля'),
#     ('Канашка', 'Канашка'),
#     ('Вода', 'Вода'),
#     ('Электрика', 'Электрика'),
# )
#
# TYPE_CHOICES = (
#     ('Любой', 'Любой'),
#     ('Исполнительная документация', 'Исполнительная документация'),
#     ('Проектная/рабочая документация', 'Проектная/рабочая документация'),
#     ('ПОС', 'ПОС'),
#     ('ППР/ППРК', 'ППР/ППРК'),
#     ('Геодезия', 'Геодезия'),
# )
#
# STATUS_CHOICES = (
#     ('Любой', 'Любой'),
#     ('Поиск исполнителя', 'Поиск исполнителя'),
#     ('В процессе', 'В процессе'),
#     ('Выполнена', 'Выполнена'),
# )
#
# ORDER_BUDGET_CHOICES = (
#     ('Нет', 'Нет'),
#     ('По возрастанию', 'По возрастанию'),
#     ('По убыванию', 'По убыванию'),
# )
# ORDER_DATE_CHOICES = (
#     ('Нет', 'Нет'),
#     ('Сначала новые', 'Сначала новые'),
#     ('Сначала старые', 'Сначала старые'),
# )
#
# class FilterForm(forms.Form):
#     # Форма фильтров
#     category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
#     type = forms.ChoiceField(choices=TYPE_CHOICES)
#     budget_from = forms.DecimalField(max_digits=18, decimal_places=2, initial=0)
#     budget_to = forms.DecimalField(max_digits=18, decimal_places=2, initial=9999999999999999)
#     status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
#     ordering_budget = forms.ChoiceField(choices=ORDER_BUDGET_CHOICES, required=False)
#     ordering_date = forms.ChoiceField(choices=ORDER_DATE_CHOICES, required=False)
