from django.db import models
from django.template.defaultfilters import slugify
import random
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


YES_NO = (('Y', 'Y'), ('N', 'N'))

class Subject(models.Model):
    
    name = models.CharField(max_length=200, null=True)
    description = RichTextUploadingField(null=True, blank=True)
    is_active = models.CharField(max_length=20, null=True, choices=YES_NO, default="Y")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'subject'
        verbose_name_plural = 'subject'
        db_table = "subject"
