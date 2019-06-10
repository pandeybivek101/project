from .models import *
from django import forms

class AddProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'body', 'url', 'image', 'price', 'catagory']

