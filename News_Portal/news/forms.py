from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post, User


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


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        return user

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']