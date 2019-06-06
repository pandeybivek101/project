from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
	title=models.CharField(max_length=300)
	pub_date=models.DateTimeField(auto_now_add = True)
	image=models.ImageField(upload_to='static/')
	likes=models.IntegerField(default=1)
	body=models.TextField()
	url=models.CharField(max_length=40)
	price = models.CharField(max_length=10 ,default='1000')
	user=models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def summary(self):
		return self.body[:100]

	def pub_date_pretty(self):
		return self.pub_date.strftime['%b %e, %Y']
