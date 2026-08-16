from django.db import models
from users.models import CustomUser

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # сортировка по дате (новые сверху)

    def __str__(self):
        return f'Post by {self.author.username}'
