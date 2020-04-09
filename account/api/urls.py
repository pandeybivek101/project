"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from account.api.views import *

urlpatterns = [
	
    path('signup/', SignUp.as_view(), name='api_signup'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('profile/', Profile.as_view(), name='api_profile'),
    #path('userprofile/<int:pk>', UserProfile.as_view(), name='userprofile'),
]
