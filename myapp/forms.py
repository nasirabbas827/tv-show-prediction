from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'date_of_birth', 'phone_number', 'address', 'profile_picture']

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Comment
        fields = ['text', 'rating_numerical', 'rating_thumb_up', 'rating_thumb_down', 'rating_star']
