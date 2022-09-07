from django.db import models

from account.models import Account


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to='images/')
    text = models.CharField(max_length=2048, null=True, blank=True)
