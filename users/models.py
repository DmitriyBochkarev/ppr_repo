
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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