from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class Catagory(models.Model):
	catagory = models.CharField(max_length=100)

	def __str__(self):
		return self.catagory

class SubCatagory(models.Model):
	sub_catagory=models.CharField(max_length=100)
	catagory=models.ForeignKey(Catagory, on_delete=models.CASCADE)

	def __str__(self):
		return self.sub_catagory

class Product(models.Model):
	title=models.CharField(max_length=300)
	pub_date=models.DateTimeField(auto_now_add = True)
	image=models.ImageField(upload_to='image/', blank=True, null=True)
	image2=models.ImageField(upload_to='image/', blank=True, null=True)
	image3=models.ImageField(upload_to='image/', blank=True, null=True)
	image4=models.ImageField(upload_to='image/', blank=True, null=True)
	image5=models.ImageField(upload_to='image/', blank=True, null=True)
	image6=models.ImageField(upload_to='image/', blank=True, null=True)
	bought_date=models.DateField(null=True, blank=True)
	brand=models.CharField(max_length=300, blank=True, null=True)
	model=models.CharField(max_length=300, blank=True, null=True)
	body=models.TextField()
	url=models.URLField(blank=True, null=True)
	catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
	sub_catagory = models.ForeignKey(SubCatagory, on_delete=models.CASCADE, blank=True, null=True)
	price = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,related_name="likes",blank=True)
	views=models.ManyToManyField(User,related_name="views",blank=True)
	sold=models.BooleanField(default=False)
	pro_lat=models.FloatField(max_length=300, blank=True, null=True)
	pro_lng=models.FloatField(max_length=300, blank=True, null=True)
	show_contact=models.BooleanField()
	show_location=models.BooleanField()


	def __str__(self):
		return self.title

	def summary(self):
		return self.body[:100]

	def pub_date_pretty(self):
		return self.pub_date.strftime['%b %e, %Y']

	def total_like(self):
		return self.likes.count()


class Comment(models.Model):
	comment = models.CharField(max_length=300)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	commented_date = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return "{} {}".format(self.user, self.product)

class Replies(models.Model):
	reply = models.CharField(max_length=100)
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	replied_user = models.ForeignKey(User, on_delete=models.CASCADE)
	replied_date = models.DateTimeField(auto_now_add = True)

	class Meta:
		ordering = ["-replied_date"]

	def __str__(self):
		return "{} {}".format(self.comment.id, self.replied_user)

class Message(models.Model):
	message = models.TextField()
	message_user = models.ForeignKey(User, on_delete=models.CASCADE)
	message_date = models.DateTimeField(auto_now_add = True)



