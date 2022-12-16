from django.db import models

class User(models.Model):
	username = models.CharField(max_length=200)
	photo = models.CharField(max_length=500)

class Bunk(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_set")
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_set")
	time = models.DateTimeField('bunk time')