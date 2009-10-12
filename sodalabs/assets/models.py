from django.db import models
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from sodalabs import settings

fs = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url=settings.UPLOAD_URL)

# Create your models here.
class Asset(models.Model):
    file = models.ImageField(upload_to='site_assets', storage=fs)

    def __unicode__(self):
        return 'Asset : %s' % self.file.url

admin.site.register(Asset)
