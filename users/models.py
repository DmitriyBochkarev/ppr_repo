
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from searchwork.models import Task
from django.urls import reverse
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        # output_size = (480, 480)
        # img.thumbnail(output_size)
        # coordinates = (0, 0, 300, 300)
        # cropped = img.crop(coordinates)
        #
        # cropped.save(self.image.path)
        def crop_center(img, crop_width: int, crop_height: int) -> Image:
            """
            Функция для обрезки изображения по центру.
            """
            img_width, img_height = img.size
            return img.crop(((img_width - crop_width) // 2,
                                 (img_height - crop_height) // 2,
                                 (img_width + crop_width) // 2,
                                 (img_height + crop_height) // 2))


        def crop_max_square(img):
            return crop_center(img, min(img.size), min(img.size))


        img = crop_max_square(img)

        output_size = (300, 300)
        img.thumbnail(output_size)

        img.save(self.image.path)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    about = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} Client'
    def get_absolute_url(self):
        return reverse('my-tasks', kwargs={'username': self.user.username})

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, default=0)
    experience = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} Worker'

    def get_absolute_url(self):
        return reverse('tasks-home')

class Candidate(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    offer = models.TextField(null=True)

    def __str__(self):
        return f'{self.worker.user.username} Candidate'

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.task.id})

class WorkerComment(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='worker_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.text}'


class Conversation(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user1.username} <-> {self.user2.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"


class ClientComment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.text}'


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
