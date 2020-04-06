from account.models import *
from account.api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *


from rest_framework.generics import CreateAPIView

class SignUp(CreateAPIView):
	serializer_class=UserCreationSerializers



class LoginView(APIView):
	serializer_class=UserLoginSerializers

	def post(self, request, *args, **kwargs):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception = True):
			new_data=serializer.data
			return Response(new_data, status = HTTP_200_OK)
		return Response(serializer.errors, status = HTTP_400_OR_BAD_REQUEST)

