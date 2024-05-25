 
import re
from django import template 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from django.db.models import Sum
from django.shortcuts import get_object_or_404 

from storeBlog.models import Blog_Post, Comment_Blog, blog_Favorite
from Accounts.models import UserProfile
register = template.Library()
'''
from storeBlog.models import ( )
from storeAccount.models import db_Profile
register = template.Library()
'''
#{{view_Product.db_Product_ID|Review_count}}
#{{prod.db_Product_ID|email:user.email}}
# -------------------------------------------<< >>-------------------------------------------------------
'''
@register.filter
def wish_count(value):
    count = db_Medicine.objects.filter(db_Wishlist_email = value).all().count() 
    return count

@register.filter(name="email", is_safe=True)
def wishlist(ID, email):
    if med_Cart_list.objects.filter(db_Wishlist_ID = ID, db_Wishlist_email = email).first() :
        item = "heart_broken"
    else:
        item = "favorite" 
    return item
''' 

@register.filter
def Comment_count(value):
    obj_ID = get_object_or_404(Blog_Post, blog_id = value)
    count = Comment_Blog.objects.filter(comment_blog_id = obj_ID).all().count() 
    return count

@register.filter
def Favorite_count(value):
    obj_ID = get_object_or_404(Blog_Post, blog_id = value)
    count = blog_Favorite.objects.filter(fav_id = obj_ID).all().count() 
    return count


@register.filter
def Cate_Split(value): 
    cate = Blog_Post.objects.filter(blog_id = value).first()
    cate_name = cate.blog_Category.split(' ')   
    return cate_name


@register.filter
def Relate_Post(value): 
    cate = Blog_Post.objects.filter(blog_id = value).first()
    cate_name = cate.blog_Post_Text.split(' ')  
    seen = set()
    seek = set()
    for line in cate_name:
        line_lower = line.lower()
        if line_lower in seen:
            pass
        else:
            seen.add(line_lower)  
    anytext = (seen)  
    seek.add(' '.join(word for word in anytext if len(word)>4))
    for see in seek:
        catlo = see 
    listed = list(catlo.split(" ")) 
    for lst in listed:
        mySearch = (Blog_Post.objects.filter(blog_Post_Text__contains = lst) | Blog_Post.objects.filter(blog_Title__contains = lst ) | Blog_Post.objects.filter(blog_Category__contains = lst ))
    # print(mySearch)
    return mySearch

@register.filter
def Relate_Show_img(value): 
    cate = Blog_Post.objects.filter(blog_id = value).first()
    file = cate.blog_file
    return file

@register.filter
def Relate_Show_title(value): 
    cate = Blog_Post.objects.filter(blog_id = value).first()
    title = cate.blog_Title
    return title

@register.filter
def Relate_Show_type(value): 
    cate = Blog_Post.objects.filter(blog_id = value).first()
    type = cate.blog_type
    return type

@register.filter
def Relate_Show_ID(value): 
    cate = Blog_Post.objects.filter(blog_id = value).first()
    id = cate.blog_id
    return id