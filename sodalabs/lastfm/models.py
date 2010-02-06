from django.db import models

# Create your models here.
class Track(models.Model):
    name = models.CharField(max_length=300)
    artist = models.CharField(max_length=300)
    search = models.CharField(max_length=300)
