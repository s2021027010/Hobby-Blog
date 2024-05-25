from django.shortcuts import redirect, render
from django.contrib.auth.models import User 
from django.template import loader
from fileinput import FileInput
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required 
import datetime, uuid, re 
from .tokens import generate_token
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.conf import settings 
from BlogNews import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserLoginForm
from Accounts.models import UserProfile

def login(request): 
    form = UserLoginForm() 
    if request.method == "POST": 
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            obj_user = authenticate(request, username = username, password = password)
            profile_obj = UserProfile.objects.filter(email = username).first()
            if profile_obj is None:
                messages.error(request, 'User or E-mail not found.')
                return redirect('login')
            if not profile_obj.is_verified:
                messages.error(request, 'User is not verified check your E-mail.')
                return redirect('login')
            if obj_user is  None:
                messages.error(request, 'Wrong password.')
                return redirect('login') 
                
            auth.login(request , obj_user) 
            return redirect('home')
            
    context = {
            'login': form,
        }
    return render(request, 'login.html',context )
from django.contrib.auth.hashers import make_password
def register(request):    
    submitted = False
    if request.method == "POST":
        register = UserRegisterForm(request.POST)
        if register.is_valid(): 
            email = request.POST.get('email')  
            register.save() 
            submitted = True
            send_mail_after_registration(email)
            messages.success(request, 'Email Successfully Register. \n We have sent an email to you , \"Please check your mail to Verify\"')
                
            return redirect('login')
    else:
        register = UserRegisterForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'register' :register, 
        'submitted': submitted,
    }
    return render(request, 'signup.html', context)

def verify(request , auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token = auth_token).first()
  
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.') 
                return redirect('login')
            
            profile_obj.is_verified = True 
            profile_obj.save() 
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request,'activation_failed.html')

def send_mail_after_registration(email):
    obj_user = UserProfile.objects.get(email = email)
    token = obj_user.auth_token
    subject = 'Hobby Blog : Activation Code'
    domain = settings.VBcode
    message = f'Welcome to Hobby Blog News !! \n Hi {email}, \n Please confirm your email by clicking on the following link.\n \n Confirmation Link: {domain}/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from , recipient_list, fail_silently = True )


def logout(request):
    auth.logout(request)
    return redirect("login")