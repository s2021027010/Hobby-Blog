from click import Choice, Option
from django import forms
from django.forms import EmailInput, ModelForm, PasswordInput, TextInput, Textarea, Select
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Accounts.models import UserProfile 
from django.contrib.auth.hashers import make_password

class UserRegisterForm(ModelForm):  
    class Meta:
        model =  UserProfile
        fields = ('first_name', 'last_name', 'email', 'password', 'gender', 'town_address', 'country_address', 'phone_number', 'date_DoB')
        widgets = {
            'first_name': TextInput(attrs={'class': "input100", 'style': 'max-width: 300px;', 'required': 'True' }),
            'last_name': TextInput(attrs={'class': "input100", 'style': 'max-width: 300px;', 'required': 'True'  }),
            'email': EmailInput(attrs={ 'class': "input100",  'style': 'max-width: 300px;', 'required': 'True'  }),
            'password' : PasswordInput(attrs={ 'class': "input100", 'style': 'max-width: 300px;', 'required': 'True'  }),
            'gender': Select(attrs={'type': "text", 'class': "input100", 'style': 'max-width: 300px;', 'required': 'True'  }),
            'town_address': Textarea(attrs={'type': "textarea", 'class': "input100", 'style': 'height: 60px;', 'required': 'True' }),
            'country_address': Textarea(attrs={'type': "textarea", 'class': "input100", 'style': 'height: 60px;', 'required': 'True'  }),
            'phone_number': TextInput(attrs={'type': "tel", 'class': "input100", 'style': 'max-width: 300px;', 'required': 'True'  }), 
            'date_DoB': TextInput(attrs={'type': "date", 'class': "input100", 'style': 'max-width: 300px;', 'required': 'True'  }), 
        }

class UserLoginForm(ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('username', 'password') 
        widgets = {
            'username': EmailInput(attrs={ 'class': "input100",  'style': 'max-width: 300px;', 'required': 'True'  }),
            'password': PasswordInput(attrs={ 'class': "input100", 'style': 'max-width: 300px;', 'required': 'True'  }),
    }