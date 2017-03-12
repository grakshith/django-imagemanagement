from __future__ import unicode_literals
import uuid
from django.db import models

# Create your models here.

class Image(models.Model):
	def __str__(self):
		return str(self.name)
	name=models.CharField(max_length=50)
	image=models.ImageField(upload_to='images')
	old_size=models.IntegerField(default=0)
	new_size=models.IntegerField(default=0)

class AccessKey(models.Model):
	def __str__(self):
		return str(self.accessKey)+' - '+self.name
	name=models.CharField(max_length=50)
	accessKey=models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)