from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    pass


class User(AbstractUser):
    CHOICE_GENDER = (
        ('man', '남성'),
        ('woman', '여성')
    )

    alias = models.CharField(max_length=10)
    gender = models.CharField(max_length=5, choices=CHOICE_GENDER)
    profile_img = models.ImageField(upload_to='user', blank=True)
    cover_img = models.ImageField(upload_to='cover')
    introduce = models.TextField(max_length=255)
