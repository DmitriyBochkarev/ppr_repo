
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from searchwork.models import Task
from django.urls import reverse


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
    rating = models.IntegerField(null=True)
    experience = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} Worker'

    def get_absolute_url(self):
        return reverse('tasks-home')

class Candidate(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.task.id})



