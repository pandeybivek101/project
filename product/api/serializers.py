from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField
from product.models import *


class AddProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['title', 'body', 'url', 'image', 'price', 'catagory']


class UpvoteSerializer(serializers.ModelSerializer):
	class Meta:
		model=Product
		fields=['likes']


class ProductListSerializer(serializers.ModelSerializer):
	user=SerializerMethodField()
	catagory=SerializerMethodField()

	class Meta:
		model = Product
		fields = ['title', 'image', 'price', 'catagory', 'user', 'pub_date']

	def get_user(self, obj):
		user=str(obj.user.username)
		return user

	def get_catagory(self, obj):
		return str(obj.catagory.catagory)


class ProductDetailSerializer(serializers.ModelSerializer):
	user=SerializerMethodField()
	catagory=SerializerMethodField()
	likes=SerializerMethodField()
	count_like=SerializerMethodField()
	class Meta:
		model = Product
		fields = '__all__'

	def get_user(self, obj):
		user=str(obj.user.username)
		return user

	def get_likes(self, obj):
		return str(obj.likes.all)

	def get_catagory(self, obj):
		return str(obj.catagory.catagory)

	def get_count_like(self, obj):
		return obj.likes.count()


class AddCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['comment']
