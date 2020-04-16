from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
	email = models.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']


class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control', 
		'placeholder':'Username',
		'id':'username',
		'name':'name'
		}), 
	required=True, max_length=30)
	password=forms.CharField(widget=forms.PasswordInput(
		attrs={"class":"form-control",
		 "placeholder":"Password",
		 'id':'password',
		 }), 
	required=True)
	