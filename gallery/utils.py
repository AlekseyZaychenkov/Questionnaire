import logging

from gallery.models import Gallery, Image

log = logging.getLogger(__name__)


def delete_accounts_images(account):
    galleries = Gallery.objects.filter(owner=account)

    for gal in galleries:
        images = Image.objects.filter(gallery=gal)
        for img in images:
            delete_image(img)


def delete_image(image):
    if image:
        image.delete()
    else:
        log.error(f"Image entry with id='{image.id}' does not exist.")
