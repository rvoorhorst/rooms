from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from apps.base.models import Comment, User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
