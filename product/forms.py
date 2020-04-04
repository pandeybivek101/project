from .models import *
from django import forms


class AddProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'body', 'url', 'image', 'price', 'catagory']

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']


class ReplyForm(forms.ModelForm):
	class Meta:
		model = Replies
		fields = ['reply']


class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields=['message']