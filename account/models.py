from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Profile(models.Model):
	image = models.ImageField(default ='Screenshot_156.png', upload_to='static/')
	contact = models.CharField(max_length=100, blank=True, null=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username
		

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user = instance)


@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



