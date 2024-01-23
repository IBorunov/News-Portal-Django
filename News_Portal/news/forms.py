from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['authorship', 'title', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if len(title) > 100:
            raise ValidationError(
                "Название должно быть в пределах 100 символов."
            )
        if text is not None and len(text) < 20:
            raise ValidationError(
                "Текст слишком короткий.")

        return cleaned_data