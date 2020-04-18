#from .models import *
from .models import *
from django import forms

class AddProductForm(forms.ModelForm):
	title=forms.CharField(widget=forms.TextInput(
		attrs={'class':'single-input', 
		'placeholder':"Title",
		'name':'title'
		}), 
	required=True, max_length=30)
	body=forms.CharField(widget=forms.TextInput(
		attrs={'class':'single-textarea', 
		'placeholder':"Description",
		'name':'body'
		}), 
	required=True, max_length=30)
	brand=forms.CharField(widget=forms.TextInput(
		attrs={'class':'single-input', 
		'placeholder':"Brand",
		'name':'brand'
		}), 
	required=True, max_length=30)
	model=forms.CharField(widget=forms.TextInput(
		attrs={'class':'single-input', 
		'placeholder':"model",
		'name':'model'
		}), 
	required=True, max_length=30)
	bought_date=forms.DateField(widget=forms.TextInput(
		attrs={'class':'single-input', 
		'placeholder':"Bought Date",
		'name':'bought_date',
		'type':'date',
		}),
	required=True)
	price=forms.CharField(widget=forms.TextInput(
		attrs={'class':'single-input', 
		'placeholder':"Expected Price",
		'name':'price'
		}), 
	required=True)
	show_contact=forms.BooleanField(widget=forms.TextInput(
		attrs={ 
		'name':'show_contact',
		'label':'show contact',
		'id':'primary-switch',
		'type':'checkbox',
		'checked':True,
		}), required=False)
	show_location=forms.BooleanField(widget=forms.TextInput(
		attrs={ 
		'name':'show_location',
		'id':'confirm-switch',
		'type':'checkbox',
		'checked':True,
		}), required=False)
	class Meta:
		model = Product
		fields = ['title', 'body', 'brand', 'model',  'price', 
		'catagory','bought_date', 'image',
		'image2','image3', 'image4', 'image5', 'image6', 'show_contact','show_location']


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