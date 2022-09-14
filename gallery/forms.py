# -*- coding: utf-8 -*-
import logging
import os

from django import forms

from gallery.models import Gallery, Image
from gallery.validators import validate_file_extension

log = logging.getLogger(__name__)


class ImageCreateForm(forms.ModelForm):
    image_field = forms.ImageField(widget=forms.ClearableFileInput(), validators=[validate_file_extension])
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 10}), required=False)

    def set_gallery(self, gallery):
        image = self.instance
        image.gallery = gallery
        self.instance = image

    def save(self, commit=True):
        image = self.instance
        if commit:
            image.save()

        return image

    class Meta:
        model = Image
        exclude = ('gallery', )


class ImageEditForm(forms.ModelForm):
    image_field = forms.ImageField(widget=forms.ClearableFileInput(), validators=[validate_file_extension], required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 10}), required=False)

    def save(self, commit=True):
        image = self.instance
        if commit:
            image.save()

        return image

    class Meta:
        model = Image
        exclude = ('image_field', 'text', 'gallery',)


class ImageDeleteForm(forms.Form):
    image_id = forms.CharField(required=True)

    def delete(self):
        image_id = self.data["image_id"]
        image = Image.objects.get(id=image_id)
        if image:
            # TODO: delete image file
            image.delete()
        else:
            log.error(f"Image entry with id='{image_id}' does not exist.")
