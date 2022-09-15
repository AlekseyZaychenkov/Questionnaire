import os

from django.db import models
from django.dispatch import receiver

from account.models import Account


class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to='images/')
    text = models.CharField(max_length=2048, null=True, blank=True)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image_field:
        if os.path.isfile(os.path.join(instance.image_field.path)):
            os.remove(os.path.join(instance.image_field.path))
