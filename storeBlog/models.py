from asyncio.windows_events import NULL
from email.policy import default
from enum import auto
from datetime import datetime, time, date, timezone
from random import choices
import uuid, re 
import django

from django.contrib import messages
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from Accounts.models import UserProfile

class Blog_Post(models.Model):
    blog_id = models.CharField(_("Blog ID"), primary_key = True, unique = True, max_length = 50) 
    blog_email = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    blog_Title = models.CharField(_("Title Name"), max_length = 255, null = True, blank = True)  
    blog_Category = models.CharField(_("Blog Category"), max_length = 255, null = True, blank = True)
    blog_type = models.CharField(max_length = 50, blank = True, choices = [("Text", "Text"), ("Image", "Image"), ("Video", "Video")]) 
    blog_Post_Text = models.TextField(_("Post Text"), max_length = 50000, null = True, blank = True)
    blog_file = models.ImageField(_("Post Image/Video"), upload_to = "Post/", width_field = None, height_field = None, max_length = 1000, blank = True)

    created_at = models.DateTimeField(_("Created Date"), default = django.utils.timezone.now)
    def __str__(self):
        return self.blog_id
    
class blog_Catego(models.Model):
    cate_id = models.CharField(_("Category ID"), primary_key = True, unique = True, max_length = 50)
    cate_name = models.CharField(max_length = 50, blank = True, null = True)

    def __str__(self):
        return self.cate_name

class Comment_Blog(models.Model):
    comment_pk = models.CharField(_("Comment ID"), primary_key = True, unique = True, max_length = 50) 
    comment_blog_id = models.ForeignKey(Blog_Post, on_delete=models.CASCADE)
    comment_email = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment_type = models.CharField(max_length = 50, blank = True)
    Comment_Text = models.TextField(_("Comment Text"), max_length = 10000, null = True, blank = True)

    created_at = models.DateTimeField(_("Created Date"), default = django.utils.timezone.now)
    
    def __str__(self):
        return self.comment_pk + " < | > " + self.comment_type
    
class blog_Favorite(models.Model):
    fav_pk = models.CharField(_("Favorite ID"), primary_key = True, unique = True, max_length = 50)
    fav_id = models.ForeignKey(Blog_Post, on_delete=models.CASCADE)
    fav_email = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.fav_pk
