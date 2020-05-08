from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from product.models import Product
from django.views.generic import *
from product.models import Product
from django.views import View
from product.mixins import AddMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class SignUp(View):
    form_class=UserRegistrationForm
    template_name='account/signup.html'

    def get(self, request):
        form = self.form_class()
        phone_form = PhonenumberForm()
        return render(request, self.template_name, {"form":form, 'phone_form':phone_form})

    def post(self, request):
        form = self.form_class(request.POST)
        phone_form=PhonenumberForm(request.POST)
        if form.is_valid() and phone_form.is_valid():
            form.save()
            user=User.objects.filter().last()
            phone=Profile.objects.get(user=user)
            phone.contact=phone_form.cleaned_data['contact']
            phone.save()
            return redirect('login')
        return render(request, self.template_name, {"form":form, 'phone_form':phone_form})



def LoginView(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print(username)
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid Username or password')
    else:
        form=LoginForm()
    return render(request, 'account/login.html', {'form':form})



@login_required
def Logout(request):
    logout(request)
    return redirect("home")


class Profile(View):
    template_name='account/profile.html'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        product=Product.objects.filter(user=request.user)
        context={'user_form':user_form, 'profile_form':profile_form,'product':product}
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        context={'user_form':user_form, 'profile_form':profile_form}
        return render(request, self.template_name, context)


class UserProfile(LoginRequiredMixin, AddMixin, View):
    template_name='userprofile.html'
    model=User

    def get(self, request, pk):
        product = self.get_object()
        return render(request, self.template_name, {"product":product})


def usernotification(request):
    return render(request, 'newnotification.html')

