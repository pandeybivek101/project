from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GetObjectMixin:

	def get_object(self, *args, **kwargs):
		return Product.objects.get(pk=self.kwargs['pk'])

	def get(self, request, pk):
		product=self.get_object()
		serializer=self.serializer_class(product)
		return Response(serializer.data)


class MainAPIViewMixin(APIView):
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



class MainCreateGetAPIViewMixin(APIView):
	serializer_class=''

	def get(self, request, *args, **kwargs):
		serializer = self.serializer_class()
		return Response(serializer.data)


