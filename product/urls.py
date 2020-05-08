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
from django.urls import path,include
from . import views
from product.views import *


urlpatterns =[
    path('addproduct/', AddProductItem.as_view(), name='addproduct'),
    path('search/', Search.as_view(), name='search'),
    path('<int:pk>', ProductDetailView.as_view(), name='detailview'),
    path('<int:pk>/update-product', UpdateProductview.as_view(), name='update_product'),
    path('<int:pk>/delete-product', DeleteProductView.as_view(), name='delete_product'),
    path('user/<str:username>', UserProductlistView.as_view(), name='userproduct'),
    path('catagory/<str:catagory>', productcatagorylist.as_view(), name='product-catagory'),
    path('catagory/<str:catagory>/subcatagory/<str:sub_catagory>', 
        productsubcatagorylist.as_view(), name='product-subcatagory'),
    path('upvote/<int:pk>', LikeProduct.as_view(), name='upvote'),
    path('deletecomment/<int:pk>', DeleteComment.as_view(), name = 'deletecomment'),
    path('editcomment/<int:pk>', EditComment.as_view(), name = 'editcomment'),
    path('reply/<int:pk>', AddReply.as_view(), name='addreply'),
    path('replyedit/<int:pk>', EditReplyView.as_view(), name = 'editreply'),
    path('addcomment/<int:pk>', AddComment.as_view(), name = 'addcomment'),
    path('message/', views.AddMessage, name = 'message'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('dialogs/<str:username>', views.ChatView, name='chat'),

]
