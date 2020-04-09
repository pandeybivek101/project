from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, CharField, ValidationError, SerializerMethodField
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from account.models import *

class UserProfileSerializers(serializers.ModelSerializer):

	profile_pic=SerializerMethodField()

	class Meta:
		model=User
		fields=['username', 'email', 'profile_pic']

	def get_profile_pic(self, obj):
		user_record={}
		usr=get_object_or_404(Profile, user=obj)
		return usr.image.url


class UserProfilePicSerializers(serializers.ModelSerializer):
	class Meta:
		model=Profile
		fields=['image']


class UserCreationSerializers(serializers.ModelSerializer):

	confirm_password = CharField(label = 'Confirm Email')

	class Meta:
		model=User
		fields=['username', 'email', 'password', 'confirm_password']

		extra_kwargs={
		"password":{"write_only":True},
		'confirm_password':{'write_only':True},
		}

	def validate(self, data):
		email=data['email']
		email_qs=User.objects.filter(email=email)
		if email_qs:
			raise ValidationError("Email already Exists")
		return data


	def validate_confirm_password(self, value):
		data = self.get_initial()
		password = data.get("password")
		confirm_password = value
		if len(password)<8:
			raise ValidationError('Password must have at least 8 character')
		if password != confirm_password:
			raise ValidationError('Password and confirm password must match.')
		return value


	def create(self, validated_data):
		username=validated_data['username']
		email=validated_data['email']
		password=validated_data['password']
		encrypted_password=make_password(password)
		user=User(username=username, email=email, password=encrypted_password)
		user.save()
		return validated_data


class UserLoginSerializers(serializers.Serializer):
	username=serializers.CharField(label='username')
	password=serializers.CharField(label='password')

	class Meta:
		model=User
		fields=['username', 'password']

		extra_kwargs={
		"password":{"write_only":True},
		}

	def validate(self, data):
		username=data['username']
		password=data['password']
		if not username and not password:
			raise ValidationError('No Credentials were given')
		user=User.objects.filter(username=username).first()
		if user:
			checked_password=user.check_password(password)
			if checked_password:
				return data
			else:
				raise ValidationError('Incorrect Credentials')
		else:
			raise ValidationError('No username exists with this credentials')

				

			






			