from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User_profile_manager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('this file is required')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, name, password):
        """ create and saved new superuser with given detail"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Resents a UserProfile  inside our system"""
    email = models.EmailField(max_length=300, unique=True)
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = User_profile_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """update to get full users name"""
        return self.name

    def get_email(self):
        """update to get email"""
        return self.email

    def __str__(self) -> str:
        return self.email


class profileFeedItems(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text_status = models.CharField(max_length=200)
    date_create = models.DateTimeField(auto_now_add=True)

    def get_text_status(self):
        return f"{self.user.name} {self.text_status}"

    def __str__(self):
        return self.text_status

# # This code is triggered whenever a new user has been created and saved to the database
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
