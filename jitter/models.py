from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class JitterbunkUser(models.Model):
	photo = models.ImageField(upload_to="photos")
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        JitterbunkUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.jitterbunkuser.save()


class Bunk(models.Model):
	from_user = models.ForeignKey(JitterbunkUser, on_delete=models.SET_NULL, related_name="bunks_sent", null=True)
	to_user = models.ForeignKey(JitterbunkUser, on_delete=models.SET_NULL, related_name="bunks_recieved", null=True)
	time = models.DateTimeField('bunk time')

	def __str__(self):
		return self.from_user.username + " -> " + self.to_user.username
