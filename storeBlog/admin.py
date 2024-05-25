from django.contrib import admin
from .models import Blog_Post, Comment_Blog, blog_Catego, blog_Favorite
 
admin.site.register(Blog_Post)
admin.site.register(Comment_Blog)
admin.site.register(blog_Catego)
admin.site.register(blog_Favorite)