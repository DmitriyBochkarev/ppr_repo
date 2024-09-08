from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, WorkerComment, Message, ClientComment, Feedback


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

class WorkerCommentForm(forms.ModelForm):
    class Meta:
        model = WorkerComment
        fields = ['text']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class ClientCommentForm(forms.ModelForm):
    class Meta:
        model = ClientComment
        fields = ['text']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']