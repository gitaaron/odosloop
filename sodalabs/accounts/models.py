from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Musiphile(User):
    '''
    Extends built-in django user to ensure email is supplied and is unique
    '''
    musiphile_email = models.EmailField('e-mail address', max_length=255, blank=False,null=False, unique=True)

admin.site.register(Musiphile)
