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
	comment = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.title

	def summary(self):
		return self.body[:100]

	def pub_date_pretty(self):
		return self.pub_date.strftime['%b %e, %Y']

	def total_like(self):
		return self.likes.count()
