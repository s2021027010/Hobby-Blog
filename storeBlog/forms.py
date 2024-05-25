from click import Choice, Option
from django import forms
from django.forms import EmailInput, ModelForm, PasswordInput, TextInput, Textarea, Select, ImageField, CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Accounts.models import UserProfile 
from storeBlog.models import Blog_Post, Comment_Blog, blog_Catego, blog_Favorite
from django.contrib.auth.hashers import make_password


class BlogPostForm(ModelForm): 
    # blog_Category = forms.ModelMultipleChoiceField(queryset=blog_Catego.objects.all(), required=False, widget=forms.CheckboxSelectMultiple) 
    class Meta:
        model =  Blog_Post
        fields = ('blog_Title', 'blog_file' ) # ('blog_id', 'blog_email', 'blog_Title', 'blog_Category', 'blog_type', 'blog_Post_Text', 'blog_file')
        widgets = { 
            'blog_Title' : TextInput(attrs={'type' : 'text', 'class': "input100", 'style': 'max-width: 550px;', 'required': 'True' }),
            'blog_file' : TextInput(attrs={'type' : 'file','class': "input100", 'style': 'max-width: 550px;' }),
            # 'blog_Category' : CheckboxSelectMultiple(attrs={'type' : 'text', 'class': "input100", 'style': 'max-width: 550px;' }),
            # 'blog_Post_Text' : Textarea(attrs={'type' : 'textarea', 'class': "input100", 'style': 'max-width: 550px; height: 180px;' }),
        }

class UpdateBlogPostForm(ModelForm):  
    class Meta:
        model =  Blog_Post
        fields = ('blog_Title' , 'blog_file') # ('blog_id', 'blog_email', 'blog_Title', 'blog_Category', 'blog_type', 'blog_Post_Text', 'blog_file')
        widgets = { 
            'blog_Title' : TextInput(attrs={'type' : 'text', 'class': "input100", 'style': 'max-width: 550px;', 'required': 'True' }),
            # 'blog_Category' : TextInput(attrs={'type' : 'text', 'class': "input100", 'style': 'max-width: 550px;' }),
            'blog_file' : TextInput(attrs={'type' : 'file','class': "input100", 'style': 'max-width: 550px;' }),
            # 'blog_Post_Text' : Textarea(attrs={'type' : 'textarea', 'class': "input100", 'style': 'max-width: 550px; height: 190px;' }),
        }



class ProfileEditForm(ModelForm): 
     
    class Meta:
        model =  UserProfile
        fields = ('profile_image', 'first_name', 'last_name','gender', 'town_address', 'country_address','phone_number', 'date_DoB'  )  
        widgets = {
            'profile_image' : TextInput(attrs={'type' : 'file','class': "input100", 'style': 'max-width: 550px;' }),
            'first_name': TextInput(attrs={'class': "input100", 'style': 'max-width: 300px;'}),
            'last_name': TextInput(attrs={'class': "input100", 'style': 'max-width: 300px;'}), 
            'gender': Select(attrs={'type': "text", 'class': "input100", 'style': 'max-width: 300px;'}),
            'town_address': Textarea(attrs={'type': "textarea", 'class': "input100", 'style': 'height: 60px;'}),
            'country_address': Textarea(attrs={'type': "textarea", 'class': "input100", 'style': 'height: 60px;'}),
            'phone_number': TextInput(attrs={'type': "tel", 'class': "input100", 'style': 'max-width: 300px;'}), 
            'date_DoB': TextInput(attrs={'type': "date", 'value': "2024-01-01", 'class': "input100", 'style': 'max-width: 300px;'}), 
        }
