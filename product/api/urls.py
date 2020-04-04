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
from product.api.views import *

urlpatterns = [
	path('addproduct/', AddProductItem.as_view(), name='api_addproduct'),
	path('', ListProduct.as_view(), name='api_list'),
	path('<int:pk>', DetailView.as_view(), name='api_detailview'),
    path('<int:pk>/update-product', DetailView.as_view(), name='api_update_product'),
    path('<int:pk>/delete-product', DetailView.as_view(), name='api_delete_product'),
    path('<int:pk>/upvote', LikeProduct.as_view(), name='api_upvote'),
    #('search/', Search.as_view(), name='api_search'),
    path('addcomment/<int:pk>', AddComment.as_view(), name = 'api_addcomment'),
    path('detailcomment/<int:pk>', DetailComment.as_view(), name = 'api_detailcomment'),
    path('editcomment/<int:pk>', DetailComment.as_view(), name = 'api_editcomment'),
    path('deletecomment/<int:pk>', DetailComment.as_view(), name = 'api_deletecomment'),
    path('reply/<int:pk>', AddReply.as_view(), name='api_addreply'),
    path('replyedit/<int:pk>', DetailReply.as_view(), name = 'api_editreply'),
    path('replydelete/<int:pk>', DetailReply.as_view(), name = 'api_deletereply'),
    path('replydetail/<int:pk>', DetailReply.as_view(), name = 'api_detailreply'),

]
