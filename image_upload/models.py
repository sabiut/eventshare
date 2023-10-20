from django.db import models
from django.conf import settings


class UploadedImage(models.Model):
    image = models.ImageField(
        upload_to='uploaded_images/', storage=settings.DEFAULT_FILE_STORAGE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return settings.MEDIA_URL + self.image.name
