from django.db import models


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    upload_date = models.DateTimeField(auto_now_add=True)
