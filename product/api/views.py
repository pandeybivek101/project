from product.api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework import generics
from django.db.models import Q
from django.shortcuts import get_object_or_404


class GetObject:

	def get_object(self, *args, **kwargs):
		return Product.objects.get(pk=self.kwargs['pk'])

	def get(self, request, pk):
		product=self.get_object()
		serializer=self.serializer_class(product)
		return Response(serializer.data)


class MainAPIView(APIView):
	serializer_class=''
	model=None

	def get_object(self, *args, **kwargs):
		return self.model.objects.get(pk=self.kwargs.get('pk'))

	def get(self, request, pk):
		content=self.get_object()
		serializer=self.serializer_class(content)
		return Response(serializer.data)

	def put(self, request, pk):
		instance=self.get_object()
		serializer = self.serializer_class(instance, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		instance=self.get_object()
		instance.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class MainCreateGetAPIView(APIView):
	serializer_class=''

	def get(self, request, *args, **kwargs):
		serializer = self.serializer_class()
		return Response(serializer.data)



class AddProductItem(MainCreateGetAPIView, APIView):
	serializer_class=AddProductSerializer

	'''def get(self, request):
		serializer = self.serializer_class()
		return Response(serializer.data)'''


	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save(user=self.request.user)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProduct(APIView):
	serializer_class = AddProductSerializer

	def get_queryset(self):
		return Product.objects.all()
	
	def get(self, request):
		record=self.get_queryset()
		serializer=ProductListSerializer(record, many=True)
		return Response(serializer.data)


class DetailView(GetObject, APIView):
	serializer_class=ProductDetailSerializer

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


class UpdateProductview(GetObject, APIView):
	serializer_class=AddProductSerializer
	queryset=Product.objects.all()

	def put(self, request, pk):
		product=self.get_object()
		serializer = self.serializer_class(product, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LikeProduct(GetObject, RetrieveUpdateAPIView):
	serializer_class=UpvoteSerializer
	queryset=Product.objects.all()

	def perform_update(self, serializer):
		user=self.request.user
		product=self.get_object()
		if product.likes.filter(id=user.id).exists():
			product.likes.remove(user)
		else:
			product.likes.add(user)
			instance = product.save()
		return Response()


class Search(ListAPIView):
	serializer_class=AddProductSerializer

	def get_queryset(self, request):
		pass
		'''query=request.GET.get('q')
		if query:
			result=self.model.objects.filter(Q(title__icontains = query) | Q(
				catagory__catagory__icontains = query)).order_by('-pub_date')

			return result
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''


class AddComment(GetObject, APIView):
	serializer_class=AddCommentSerializer


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


class DetailComment(MainAPIView):
	serializer_class=AddCommentSerializer
	model=Comment

	'''def get_object(self, *args, **kwargs):
		return Comment.objects.get(pk=self.kwargs.get('pk'))

	def get(self, request, pk):
		comment=self.get_object()
		serializer=self.serializer_class(comment)
		return Response(serializer.data)

	def put(self, request, pk):
		comment=self.get_object()
		serializer = self.serializer_class(comment, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		comment=self.get_object()
		comment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)'''


class AddReply(MainCreateGetAPIView, APIView):
	serializer_class = AddReplySerializer
	Model=Replies
	field_name='comment'

	'''def get(self, request, pk):
		serializer = self.serializer_class()
		return Response(serializer.data)'''

	def post(self, request, pk):
		comment=get_object_or_404(Comment, pk=self.kwargs['pk'])
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save(replied_user=request.user, comment=comment)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailReply(MainAPIView):
	serializer_class=AddReplySerializer
	model=Replies

	'''def get_object(self, *args, **kwargs):
		return Replies.objects.get(pk=self.kwargs.get('pk'))

	def get(self, request, pk):
		replies=self.get_object()
		serializer=self.serializer_class(replies)
		return Response(serializer.data)


	def put(self, request, pk):
		replies=self.get_object()
		serializer = self.serializer_class(replies, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		replies=self.get_object()
		replies.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)'''



		


			








		










		