from product.api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .mixins import *
from .permissions import *


class AddProductItem(MainCreateGetAPIViewMixin, APIView):
	serializer_class=AddProductSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save(user=self.request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProduct(generics.ListAPIView):
	serializer_class = ProductListSerializer
	filter_backends = [DjangoFilterBackend]
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'catagory__catagory']

	def get_queryset(self):
		return Product.objects.all()
	

class DetailView(GetObjectMixin, APIView):
	serializer_class=ProductDetailSerializer
	permission_classes=[IsProductOwner]

	def get(self, request, pk):
		user=self.request.user
		product=self.get_object()
		serializer=self.serializer_class(product)
		if user.is_authenticated:
			if not product.views.filter(id=user.id).exists():
				product.views.add(user)
		return Response(serializer.data)

	def put(self, request, pk):
		product=self.get_object()
		serializer = self.serializer_class(product, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		product=self.get_object()
		product.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



class LikeProduct(GetObjectMixin, RetrieveUpdateAPIView):
	serializer_class=UpvoteSerializer
	queryset=Product.objects.all()
	ermission_classes = [IsAuthenticated]

	def perform_update(self, serializer):
		user=self.request.user
		product=self.get_object()
		if product.likes.filter(id=user.id).exists():
			product.likes.remove(user)
		else:
			product.likes.add(user)
			instance = product.save()
		return Response()


class AddComment(GetObjectMixin, APIView):
	serializer_class=AddCommentSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request, pk):
		serializer = self.serializer_class()
		return Response(serializer.data)

	def post(self, request, pk):
		product=self.get_object()
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user, product=product)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AddReply(MainCreateGetAPIViewMixin, APIView):
	serializer_class = AddReplySerializer
	Model=Replies
	field_name='comment'
	permission_classes = [IsAuthenticated]


	def post(self, request, pk):
		comment=get_object_or_404(Comment, pk=self.kwargs['pk'])
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save(replied_user=request.user, comment=comment)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DetailReply(MainAPIViewMixin):
	serializer_class=AddReplySerializer
	model=Replies
	permission_classes = [IsAuthenticated, IsReplyOwner]


class DetailComment(MainAPIViewMixin):
	serializer_class=AddCommentSerializer
	model=Comment
	permission_classes = [IsAuthenticated, IsCommentOwner]



		


			








		










		