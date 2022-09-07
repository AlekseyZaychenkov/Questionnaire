# -*- coding: utf-8 -*-
import logging

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
        photo = self.instance
        if commit:
            photo.save()

        return photo

    class Meta:
        model = Image
        exclude = ('gallery', )


class ImageEditForm(forms.ModelForm):
    image_field = forms.ImageField(widget=forms.ClearableFileInput(), validators=[validate_file_extension])
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 10}), required=False)

    def set_gallery(self, gallery):
        image = self.instance
        image.gallery = gallery
        self.instance = image

    def save(self, commit=True):
        photo = self.instance
        if commit:
            photo.save()

        return photo

    class Meta:
        model = Image
        exclude = ('gallery', )


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
