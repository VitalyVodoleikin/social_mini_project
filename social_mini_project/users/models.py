from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models


def validate_file_size(value):
        max_size_mb = 10
        if value.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f'Файл не должен превышать {max_size_mb} МБ.')


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name="Почта", unique=True)
    username = models.CharField(max_length=150, verbose_name="Логин", unique=True)

    avatar = models.ImageField(verbose_name="Аватар", blank=True, null=True, upload_to='avatars/')
    bio = models.TextField(max_length=500, verbose_name="О себе", blank=True, null=True)
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)

    class Meta:
        ordering = ("pk", "username")
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
