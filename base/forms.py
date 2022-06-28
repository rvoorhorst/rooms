from django.contrib.auth.forms import UserCreationForm
from base.models import User
from django.forms import ModelForm
from base.models import Comment


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
