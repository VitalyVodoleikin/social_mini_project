from django.db import models


class Post(models.Model):
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name="Текст поста", blank=False, help_text="Минимум 2 символа")
    image = models.ImageField(verbose_name="Изображение", blank=False, upload_to='posts/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)  # сортировка по дате (новые сверху)
        indexes = (
            models.Index(
                fields=[
                    'author',
                    '-created_at'
                ]
            ),
        )

    def __str__(self):
        preview = (self.content[:20] + "...") if self.content else ""
        return f'Post by {self.author.username}: {preview}'
