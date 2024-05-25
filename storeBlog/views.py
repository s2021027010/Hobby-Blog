import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User 
from django.template import loader
from fileinput import FileInput
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required 
import datetime
import uuid, re 
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.conf import settings 
from BlogNews import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from storeBlog.models import Blog_Post, Comment_Blog, blog_Catego, blog_Favorite
from Accounts.models import UserProfile
from .forms import BlogPostForm, UpdateBlogPostForm, ProfileEditForm
# Create your views here. Blog_Post

def home(request):  
    USER_email = request.user.email
    blog = BlogPostForm() 
    if request.method == "POST": 
        auth_token = str(uuid.uuid4())
        blog = BlogPostForm(request.POST) 
        if blog.is_valid(): 
            blog_id = auth_token
            blog_Title = request.POST.get('blog_Title')
            blog_Category = request.POST.get('blog_Category')
            blog_Post_Text = request.POST.get('blog_Post_Text')  
            blog_email = get_object_or_404(UserProfile, email= USER_email)
            if blog_Title == "":
                messages.success(request, "Blog Title are must required at Creating a Blogs!!!")
                return redirect('home')
            if blog_Category == "" or  blog_Category == " ":
                blog_Category = "N/A"
            if blog_Post_Text == "":
                blog_Post_Text = "N/A"
            if len(request.FILES) != 0:
                blog_file =  request.FILES['blog_file']
            else:
                blog_file = "None"
            
            if blog_file != "" and blog_file != "None":
                exe = os.path.splitext(str(blog_file))
                file_exe = exe[1]
                if (file_exe == ".jpg") or (file_exe == ".jpng") or (file_exe == ".jpeg") or (file_exe == ".png") or (file_exe == ".gif") or (file_exe == ".cr2") or (file_exe == ".nef") or (file_exe == ".orf") or (file_exe == ".sr2") or (file_exe == ".bmp") or (file_exe == ".tif") or (file_exe == ".tiff") or (file_exe == ".raw") or (file_exe == ".eps") or (file_exe == ".AI") or (file_exe == ".psd"):
                    blog_type = "Image"
                elif (file_exe == ".mp4") or (file_exe == ".ogg") or (file_exe == ".webm") or (file_exe == ".mpeg4") or (file_exe == ".flv") or (file_exe == ".mpg") or (file_exe == ".mpeg") or (file_exe == ".avi") or (file_exe == ".wmv") or (file_exe == ".rm") or (file_exe == ".mov") or (file_exe == ".swf"):
                    blog_type = "Video"
                else:
                      blog_type = "Text" 
            else:
                blog_type = "Text"
        
            obj_Blog = Blog_Post.objects.create(
                blog_email = blog_email,
                blog_id = blog_id,
                blog_Title = blog_Title,
                blog_Category = blog_Category,
                blog_Post_Text = blog_Post_Text, 
                blog_type = blog_type,
                blog_file = blog_file,

            )
            obj_Blog.save()
            messages.success(request, "Your Blog are Successfully Uploaded...")
            add_Category(request, blog_Category, address = 'home')
            return redirect('home')
    obj_Catego = blog_Catego.objects.all()
    Show_blog = Blog_Post.objects.all()
    context = { 
        'Add_Blog' : blog,
        'Show_blog': Show_blog,
        'obj_Catego': obj_Catego,
     }
    return render(request, 'home.html', context)
 
def showPost(request, id):
    Show_blog = Blog_Post.objects.filter(blog_id = id).first()
    USER_email = request.user.email
    initial_data = {'blog_Title': Show_blog.blog_Title, 'blog_Category': Show_blog.blog_Category, 'blog_file': Show_blog.blog_file}
    EditBlog = UpdateBlogPostForm(initial=initial_data) 
    if request.method == "POST":  
        EditBlog = BlogPostForm(request.POST)
        if EditBlog.is_valid(): 
            blog_Title = request.POST.get('blog_Title')
            blog_Category = request.POST.get('blog_Category')
            blog_Post_Text = request.POST.get('blog_Post_Text')  
            blog_email = get_object_or_404(UserProfile, email= USER_email)
            if blog_Title == "":
                messages.success(request, "Blog Title are must required at Creating a Blogs!!!")
                return redirect('home')
            if blog_Category == "" or  blog_Category == " ":
                blog_Category = "N/A"
            if blog_Post_Text == "":
                blog_Post_Text = "N/A"
            if len(request.FILES) != 0:
                blog_file =  request.FILES['blog_file']
            else:
                blog_file = Show_blog.blog_file
            
            if blog_file != "" and blog_file != "None":
                exe = os.path.splitext(str(blog_file))
                file_exe = exe[1]
                if (file_exe == ".jpg") or (file_exe == ".jpng") or (file_exe == ".jpeg") or (file_exe == ".png") or (file_exe == ".gif") or (file_exe == ".cr2") or (file_exe == ".nef") or (file_exe == ".orf") or (file_exe == ".sr2") or (file_exe == ".bmp") or (file_exe == ".tif") or (file_exe == ".tiff") or (file_exe == ".raw") or (file_exe == ".eps") or (file_exe == ".AI") or (file_exe == ".psd"):
                    blog_type = "Image"
                elif (file_exe == ".mp4") or (file_exe == ".ogg") or (file_exe == ".webm") or (file_exe == ".mpeg4") or (file_exe == ".flv") or (file_exe == ".mpg") or (file_exe == ".mpeg") or (file_exe == ".avi") or (file_exe == ".wmv") or (file_exe == ".rm") or (file_exe == ".mov") or (file_exe == ".swf"):
                    blog_type = "Video"
                else:
                      blog_type = "Text" 
            else:
                blog_type = "Text"
            Update_blog = Blog_Post.objects.get(blog_id = id)
            Update_blog.blog_email = blog_email
            Update_blog.blog_Title = blog_Title
            Update_blog.blog_Category = blog_Category
            Update_blog.blog_Post_Text = blog_Post_Text 
            Update_blog.blog_type = blog_type
            Update_blog.blog_file = blog_file 
            Update_blog.save()
            add_Category(request, blog_Category, address = '/blog/showPost/' + id)
            messages.success(request, "Your Blog are Updated Successfully...")
            return redirect('/blog/showPost/' + id)
    obj_ID = get_object_or_404(Blog_Post, blog_id = id)
    obj_comment = Comment_Blog.objects.filter(comment_blog_id = obj_ID ).all()
    obj_reply = Comment_Blog.objects.filter(comment_blog_id = obj_ID ).all()
    obj_Catego = blog_Catego.objects.all()
    relate_blog = Blog_Post.objects.filter().all()
    context = { 
        'Show_blog': Show_blog,
        'Edit_Blog': EditBlog,
        'obj_comment': obj_comment,
        'obj_reply': obj_reply,
        'obj_Catego': obj_Catego,
        'relate_blog': relate_blog,
     }
    return render(request, 'showPost.html', context)
def commentBlog(request, pk):
    USER_email = request.user.email
    if request.method == "POST":
        comment_pk = str(uuid.uuid4())
        obj_email = get_object_or_404(UserProfile, email= USER_email)
        obj_ID = get_object_or_404(Blog_Post, blog_id = pk)
        comment_type = request.POST.get('comment_type')
        Comment_Text = request.POST.get('comment_Text')
        if Comment_Text == "":
            messages.success(request, "Comment Field Text must be filled...")
            return redirect('/blog/showPost/' + pk)
        
        paste_comment = Comment_Blog.objects.create(
            comment_pk = comment_pk,
            comment_blog_id = obj_ID,
            comment_email = obj_email,
            comment_type = comment_type,
            Comment_Text = Comment_Text,
        )
        paste_comment.save()
        return redirect('/blog/showPost/' + pk)
    return redirect('/blog/showPost/' + pk)

def add_Category(request, PassCate, address):
    if request.method == "POST":
        cateName = PassCate
        if cateName == "N/A":
            return redirect(address)
        else:
            print("before: " + cateName)
            cate = cateName.split()
            # print("after: " + cate)
            for i in range(0, len(cate)): 
                if blog_Catego.objects.filter(cate_name = cate[i]).first():
                    print("if: " + cate[i])
                    pass
                else:
                    print("else: " + cate[i])
                    try:
                        add_cate = blog_Catego.objects.create(
                            cate_id = str(uuid.uuid4()),
                            cate_name = cate[i],
                        )
                        add_cate.save() 
                    except Exception as e:
                        print(e)
            return redirect(address)
    return redirect(address)

def profile(request):
    USER_email = request.user.email
    obj_profile = UserProfile.objects.filter(email = USER_email).first()
    #obj_Catego = blog_Catego.objects.filter(email = USER_email).all()
    obj_Catego = blog_Catego.objects.all()
    obj_email = get_object_or_404(UserProfile, email= USER_email)
    profile_fav = blog_Favorite.objects.filter(fav_email = obj_email).all()
    Show_blog_fav = Blog_Post.objects.filter().all() 
    Show_blog = Blog_Post.objects.filter(blog_email = obj_profile).all() 

    blog = BlogPostForm()
    editProfile = ProfileEditForm()
    context = {
        'obj_profile':  obj_profile, 
        'Show_blog': Show_blog,
        'Show_blog_fav': Show_blog_fav,
        # 'obj_Catego': obj_Catego,
        'Add_Blog' : blog,
        'obj_Catego': obj_Catego,
        'profile_fav': profile_fav,
        'editProfile': editProfile, 
    }
    return render(request, 'profile.html', context)
def EditProfile(request):
    USER_email = request.user.email 
    editProfile = ProfileEditForm()
    Profile_edit = UserProfile.objects.get(email = USER_email)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        town_address = request.POST.get('town_address')
        country_address = request.POST.get('country_address')
        phone_number = request.POST.get('phone_number')
        date_DoB = request.POST.get('date_DoB')

        if first_name == "":
            first_name = Profile_edit.first_name
        if last_name == "":
            last_name = Profile_edit.last_name
        if gender == "":
            gender = Profile_edit.gender
        if town_address == "":
            town_address = Profile_edit.town_address 
        if country_address == "":
            country_address = Profile_edit.country_address
        if phone_number == "":
            phone_number = Profile_edit.phone_number
        if date_DoB == "2024-01-01":
            date_DoB = Profile_edit.date_DoB

        if len(request.FILES) != 0:
            profile_image =  request.FILES['profile_image']
        else:
            profile_image = Profile_edit.profile_image

        try:
            Profile_edit.first_name = first_name
            Profile_edit.last_name = last_name
            Profile_edit.gender = gender
            Profile_edit.town_address = town_address
            Profile_edit.country_address = country_address
            Profile_edit.phone_number = phone_number
            Profile_edit.date_DoB =  date_DoB
            Profile_edit.profile_image =  profile_image
            Profile_edit.save()
            messages.success(request, "Your Profile are successfully Update...")
        except Exception as e:
            print(e) 
    return redirect(profile)

def add_favorite(request):
    if request.method == "POST":
        USER_email = request.user.email
        fav_pk = request.POST.get('favorite_id')
        fav_pk_token = str(uuid.uuid4())
        if fav_pk == "":
            return redirect("home")
        else:
            obj_ID = get_object_or_404(Blog_Post, blog_id = fav_pk)
            obj_email = get_object_or_404(UserProfile, email= USER_email)
            obj_ID_check = blog_Favorite.objects.filter(fav_id = obj_ID, fav_email = obj_email).first() 

            try:
                if obj_ID_check is None:
                    make_favorit = blog_Favorite.objects.create(
                    fav_pk = fav_pk_token, fav_id = obj_ID, fav_email = obj_email,
                    )
                    make_favorit.save()
                else:
                    obj_ID_check.delete()
                    return redirect("home") 
            except Exception as e:
                print(e)
    return redirect("home")

# ***********************************   *Search*   ***************************************************
# @login_required
def search(request):
    template = loader.get_template('Search.html')    
    search = request.GET['search']   
    mySearch = (Blog_Post.objects.filter(blog_Title__contains = search ) | Blog_Post.objects.filter(blog_Category__contains = search).values() | Blog_Post.objects.filter(blog_type__contains = search).values() | Blog_Post.objects.filter(blog_Post_Text__contains = search).values() | Blog_Post.objects.filter(created_at__contains = search).values())

    context = { 
        'mySearch': mySearch,     
        } 
    return HttpResponse(template.render(context, request))


