from account.models import *
from account.api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.generics import CreateAPIView

class SignUp(CreateAPIView):
	serializer_class=UserCreationSerializers



class LoginView(APIView):
	serializer_class=UserLoginSerializers

	def post(self, request, *args, **kwargs):
		serializer=self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception = True):
			username=serializer.validated_data['username']
			password=serializer.validated_data['password']
			user=authenticate(username=username, password=password)
			token=Token.objects.get(user=user)
			login(request, user)
			return Response({"Message":"Login Success",
				'username':username,
				'Token':token.key,
				})
		return Response(serializer.errors)

