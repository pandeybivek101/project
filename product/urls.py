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
    #path('addproduct/', views.AddProductItem, name='addproduct'),
    path('search/', views.Search, name='search'),
    path('<int:pk>', views.DetailView, name='detailview'),
    path('<int:pk>/update-product', UpdateProductview.as_view(), name='update_product'),
    path('<int:pk>/delete-product', DeleteProductView.as_view(), name='delete_product'),
    path('user/<str:username>', UserProductlistView.as_view(), name='userproduct'),
    path('catagory/<str:catagory>', productcatagorylist.as_view(), name='product-catagory'),
    path('<int:pk>/upvote', views.LikeProduct, name='upvote'),
    path('deletecomment/<int:pk>', DeleteComment.as_view(), name = 'deletecomment'),
    path('editcomment/<int:pk>', views.EditComment, name = 'editcomment'),
]
