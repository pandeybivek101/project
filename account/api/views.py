from account.models import *
from account.api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


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


class LogoutView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		logout(request)
		return Response({"Message":'Logout Success'})


class Profile(APIView):
	serializer_class=UserProfileSerializers
	permission_classes = [IsAuthenticated]

	def get_object(self, *args, **kwargs):
		return get_object_or_404(User, id=self.request.user.id)
	
	def get(self, request, *args, **kwargs):
		usr=self.get_object()
		serializer=self.serializer_class(usr)
		return Response(serializer.data)

	def put(self, request, *args, **kwargs):
		usr=self.get_object()
		profile_image=get_object_or_404(Profile, user=usr)
		serializer=self.serializer_class(usr, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors)





