from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "image")

    def clean_content(self):
        content = self.cleaned_data.get("content") or ""
        if len(content.strip()) < 2:
            raise forms.ValidationError("Текст поста должен содержать минимум 2 символа.")
        return content

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content", "") or ""
        image = cleaned_data.get("image")
        if not content.strip() and not image:
            raise forms.ValidationError("Пост должен содержать текст или изображение.")
        return cleaned_data
