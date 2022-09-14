from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):

    def create_user(self, email, nick_name, password):
        user = self.model(email=email, nick_name=nick_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nick_name, password):
        user = self.create_user(email=email, nick_name=nick_name,  password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    # person
    email = models.EmailField(verbose_name="E-Mail", max_length=60, unique=True)
    nick_name = models.CharField(verbose_name="Nickname", max_length=20)

    # necessary
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # to use email as a login field
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ["nick_name"]

    objects = AccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
