from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.views.generic import *
from product.models import Product

# Create your views here.

def SignUp(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'registration Success.You can login Now.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {"form":form})


@login_required
def Logout(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form })


def UserProfile(request, pk):
    product = User.objects.get(pk=pk)
    return render(request, 'userprofile.html', {"product":product})

def usernotification(request):
    return render(request, 'newnotification.html')

