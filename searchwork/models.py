from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

STATUS_CHOICES = (
    ('Поиск исполнителя', 'Поиск исполнителя'),
    ('В процессе', 'В процессе'),
    ('Выполнена', 'Выполнена'),
)

TYPE_CHOICES = (
    ('Исполнительная документация', 'Исполнительная документация'),
    ('Проектная/рабочая документация', 'Проектная/рабочая документация'),
    ('ПОС', 'ПОС'),
    ('ППР/ППРК', 'ППР/ППРК'),
    ('Геодезия', 'Геодезия'),
)
CATEGORY_CHOICES = (
    ('Земля', 'Земля'),
    ('Канашка', 'Канашка'),
    ('Вода', 'Вода'),
    ('Электрика', 'Электрика'),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_user")
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="worker_user")
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Поиск исполнителя')
    budget = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, null=False, default='Исполнительная документация')
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, null=False, default='Земля')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('my-tasks', kwargs={'username': self.author.username})



class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.text}'

