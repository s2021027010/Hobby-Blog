from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View
import sys , os
from . import views 
from django.urls import include, path
from django.conf.urls import include

urlpatterns = [
    path('login/' , views.login, name='login'),  
    path('register/' , views.register, name='register'),  
    path('logout/' , views.logout, name='logout'), 
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('verify/<auth_token>' , views.verify , name="verify"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)