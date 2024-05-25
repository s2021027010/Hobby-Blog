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

#  verbose_name='Username',
# ('first_name', 'last_name', 'email', 'password', 'gender', 'town_address', 'country_address', 'phone_number', 'date_DoB', 'profile_image')
class UserProfile(AbstractBaseUser, PermissionsMixin): 
    objects = UserManager()
    username    = models.CharField(_("Username"), unique=True, max_length = 50) 
    email       = models.EmailField(_("Email Address"), unique=True, max_length = 50)
    first_name  = models.CharField(_("First Name"), max_length = 30, null=True, blank=True)
    last_name   = models.CharField(_("Last Name"), max_length = 50, null=True, blank=True)
    is_active   = models.BooleanField(_("Active"), default = True, null=False)
    is_staff    = models.BooleanField(_("Staff"), default = False, null=False)
    
    gender = models.CharField(_("User Gender"), max_length = 50, default = "Male", blank = True, choices = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    town_address = models.TextField(_("Town Address"), max_length = 500, blank = True)
    country_address = models.TextField(_("Country Address"), max_length = 500, blank = True)
    phone_number = models.CharField(_("Phone Number"), max_length = 50, blank = True)
    date_DoB = models.DateField(_("Date of Birth"), default = django.utils.timezone.now)  
    created_at = models.DateTimeField(_("Created Date"), default = django.utils.timezone.now)
    profile_image = models.ImageField(_("Profile Image"), upload_to="Profile/", width_field = None, height_field = None, max_length = 1000, blank = False, null=False, default="/Profile/defaultDP.png")
    
    auth_token = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(_("Verify Account"), default = False, null=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        fullname = self.first_name + " " + self.last_name
        return self.fullname
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


    def clean(self):
        super().clean()
        self.username = self.email
        self.password = make_password(self.password)
        self.auth_token = str(uuid.uuid4())

     
    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email 
    '''
    def update_last_login(sender, user, **kwargs): 
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
    '''
