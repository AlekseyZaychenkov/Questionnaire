from django.contrib import admin

from account.models import Account
from gallery.models import Gallery, Image

from django_object_actions import DjangoObjectActions

from gallery.utils import delete_accounts_images


class AccountAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('email', 'nick_name', 'is_active',)

    def delete_images(self, request, account):
        delete_accounts_images(account)

    delete_images.label = "Delete all user's images"
    delete_images.short_description = "Delete images for this user"

    change_actions = ('delete_images',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Image)
admin.site.register(Gallery)

