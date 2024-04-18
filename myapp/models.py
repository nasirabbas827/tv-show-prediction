from django.contrib.auth.models import User
from django.db import models
from django.core import validators

from django.db import models
from django.contrib.auth.models import User
from django.core import validators

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    phone_number = models.CharField(
        max_length=20,
        default="",
        blank=True,
        null=True,
        validators=[validators.RegexValidator(regex='^[0-9]*$', message='Enter a valid phone number.', code='invalid_number')]
    )  # Only allow numeric values
    address = models.TextField(default="", blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')  # Add this line for profile picture

    def __str__(self):
        return self.user.username


from django.db import models

class Show(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    airing_time = models.DateTimeField()
    show_picture = models.ImageField(upload_to='show_pics/', null=True, blank=True) 

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from .models import Show

from django.db import models

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    text = models.TextField()
    rating_numerical = models.IntegerField()
    rating_thumb_up = models.BooleanField(default=False)
    rating_thumb_down = models.BooleanField(default=False)
    rating_star = models.IntegerField()
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sentiment_label = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.show.title}"
