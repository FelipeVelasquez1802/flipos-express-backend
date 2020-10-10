from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender='users.User')
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)
        user_id = instance.id
        User.objects.filter(id=user_id).update(token=token.key)


class User(AbstractUser):
    token = models.CharField(verbose_name="Token", max_length=150, null=True, blank=True)
