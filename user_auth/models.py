from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True);
    full_name = models.CharField(max_length=150, blank =True)
    profile_pic = models.ImageField(upload_to='profile/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    
    def get_profile_pic(self):
        if self.profile_pic:
            return self.profile_pic.url
        return static('images/other/author-default.png')
    
    def __str__(self):
        return self.user.username
    
# Create your models here.
