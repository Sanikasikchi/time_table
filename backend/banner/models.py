from django.db import models

import os
import uuid
import random
from ckeditor_uploader.fields import RichTextUploadingField
 
def user_directory_path(instance, filename):
    path = "banners/"
    extension = "." + filename.split('.')[-1]
    stringId = str(uuid.uuid4())
    randInt = str(random.randint(10, 99))
    filename_reformat = stringId + randInt + extension
    return os.path.join(path, filename_reformat)
YES_NO = (('Y', 'Y'), ('N', 'N'))
 

class Banner(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, default='no_image_available.png')
    # description = models.TextField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    sort_order = models.IntegerField(default=1)
    is_active = models.CharField(max_length=20, null=True, choices=YES_NO, default="Y")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = 'banners'
        db_table = "banner"
 