from typing import Iterable
from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from ="name", unique=True )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
 
            self.slug = f"{base_slug}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Blog(models.Model):
    STATUS = (
        ('0', "DRAFT"),
        ('1', "PUBLISH")
    )
    
    SECTION = (
        ("Recent", "Recent"),
        ("Popular", "Popular"),
        ("Trending", "Trending"),
        ("Main_Post", "Main_Post")
        
        
    )
    
    title = models.CharField(max_length=100)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="images/")
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='blog', on_delete=models.CASCADE)
    blog_slug = AutoSlugField(populate_from ="title", unique=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1,default="DRAFT")
    section = models.CharField(max_length=20, choices=SECTION, default="Recent")
    def __str__(self) -> str:
        return f"{self.title} ({self.category})"
# Create your models here.


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    blog_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    comment = models.TextField()
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE,related_name="replies")
    
    def save(self, *args, **kwargs):
        # Automatically set the blog_id when saving a comment
        if self.post:
            self.blog_id = self.post.id
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
