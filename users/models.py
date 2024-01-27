import uuid
from typing import Optional

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from users.managers import CustomUserManager


class UserModel(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_access_token(self, access_token: Optional[str]) -> None:
        self.access_token = access_token
        self.save()

    def __str__(self) -> str:
        return f'{self.uuid} | {self.email} | {self.is_staff}'
