from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """User 모델에서 사용하기 위한 UserManager 생성"""
    def create_user(self, email, password=None, **extra_fields):
        """일반 유저로 생성"""
        if not email:
            raise ValueError('이메일을 입력해주세요')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """
        superuser 일반적으로 아이디/비밀번호만 받기 때문에 **kwargs 배제
        superuser 로 생성할 경우 필드값을 True 로 변경
        """
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    CHOICE_GENDER = (
        ('man', '남성'),
        ('woman', '여성')
    )

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # 일반 유저는 staff 권한이 없어야 함(default=False)
    is_staff = models.BooleanField(default=False)

    alias = models.CharField(max_length=20, null=True, unique=True)
    gender = models.CharField(max_length=5, choices=CHOICE_GENDER)
    profile_img = models.ImageField(upload_to='profile', blank=True, null=True)
    cover_img = models.ImageField(upload_to='cover', blank=True, null=True)
    address = models.CharField(max_length=100)
    introduce = models.TextField(max_length=255)

    # UserManager 을 재정의하여 사용
    objects = UserManager()
    # USERNAME 을 email 로 사용
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']
