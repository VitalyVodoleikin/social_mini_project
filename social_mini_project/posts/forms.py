from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "image")

    def clean_content(self):
        content = self.cleaned_data["content"]
        if len(content.strip()) < 2:
            raise forms.ValidationError("Текст поста должен содержать минимум 2 символа.")
        return content
