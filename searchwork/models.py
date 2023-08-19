from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


STATUS_CHOICES = (
    ('Поиск исполнителя', 'Поиск исполнителя'),
    ('В процессе', 'В процессе'),
    ('Выполнена', 'Выполнена'),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_user")
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="worker_user")
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='Поиск исполнителя')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('my-tasks', kwargs={'username': self.author.username})

