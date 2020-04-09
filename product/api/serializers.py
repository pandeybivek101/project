from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, HyperlinkedIdentityField
from product.models import *
from django.shortcuts import get_object_or_404



class AddProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['title', 'body', 'url', 'image', 'price', 'catagory']


class UpvoteSerializer(serializers.ModelSerializer):
	class Meta:
		model=Product
		fields=['likes']



class ProductListSerializer(serializers.HyperlinkedModelSerializer):
	user=SerializerMethodField()
	count_like=SerializerMethodField()
	detail=serializers.HyperlinkedIdentityField(view_name='api_detailview')

	class Meta:
		model = Product
		fields = ['id', 'title', 'image', 'price', 'user', 'pub_date', 'count_like', 'detail']

	def get_user(self, obj):
		user=str(obj.user.username)
		return user

	def get_count_like(self, obj):
		return obj.likes.count()


class ProductDetailSerializer(serializers.ModelSerializer):
	user=SerializerMethodField()
	catagory=SerializerMethodField()
	likes=SerializerMethodField()
	count_like=SerializerMethodField()
	comment=SerializerMethodField()


	class Meta:
		model = Product
		fields = '__all__'

	def get_user(self, obj):
		user=str(obj.user.username)
		return user

	def get_likes(self, obj):
		data=obj.likes.all()
		user_list=[]
		for user in data:
			user_list.append(user.username)
		return user_list

	def get_catagory(self, obj):
		return str(obj.catagory.catagory)

	def get_count_like(self, obj):
		return obj.likes.count()

	def get_comment(self, obj):
		commentrecord={}
		comment=[]
		commentlist = obj.comment_set.all().order_by('-commented_date')
		for item in commentlist:
			commentrecord.update({
				'content':item.comment,
				'commented_by':item.user.username,
				'replies':Replies.objects.filter(comment=item).count(),
				'commented_date':item.commented_date,
				})
			comment.append(commentrecord.copy())
		return comment


class AddCommentSerializer(serializers.ModelSerializer):
	commented_by=SerializerMethodField()
	class Meta:
		model = Comment
		fields = ['comment', 'commented_date', 'commented_by']

	def get_commented_by(self, obj):
		return obj.user.username


class AddReplySerializer(serializers.ModelSerializer):
	class Meta:
		model = Replies
		fields = ['reply']
	

