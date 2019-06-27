from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Catagory(models.Model):
	catagory = models.CharField(max_length=100)

	def __str__(self):
		return self.catagory

class Product(models.Model):
	title=models.CharField(max_length=300)
	pub_date=models.DateTimeField(auto_now_add = True)
	image=models.ImageField(upload_to='static/')
	body=models.TextField()
	url=models.URLField()
	catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
	price = models.CharField(max_length=10)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,related_name="likes",blank=True)


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

	def __str__(self):
		return "{} {}".format(self.comment.id, self.replied_user)



