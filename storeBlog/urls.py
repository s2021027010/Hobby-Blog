from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views import View 
from . import views 
from django.urls import path

# AddBlog
urlpatterns = [
    path('home/' , views.home, name='home'), 
    # path('AddPost/' , views.AddPost, name='AddPost'), 
    path('showPost/<str:id>' , views.showPost, name='showPost'), 
    path('commentBlog/<str:pk>' , views.commentBlog, name='commentBlog'),
    path('profile/' , views.profile, name='profile'),  
    path('EditProfile/' , views.EditProfile, name='EditProfile'),  
    path('search/' , views.search, name='search'), 
    path('add_favorite/' , views.add_favorite, name='add_favorite'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)