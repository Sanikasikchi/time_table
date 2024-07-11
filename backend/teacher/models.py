from django.db import models
from django.template.defaultfilters import slugify
import random
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from backend.subject.models import Subject
from backend.classes.models import *

YES_NO = (('Y', 'Y'), ('N', 'N'))


class Teacher(models.Model):

    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    phoneNo = models.CharField(max_length=200, blank=True, null=True)
    prn = models.CharField(max_length=200, blank=True, null=True)
    classes = models.ManyToManyField(Classes)
    subject = models.ManyToManyField(Subject)
    description = RichTextUploadingField(null=True, blank=True)
    is_active = models.CharField(max_length=20, null=True, choices=YES_NO, default="Y")
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True
        try:
            if SessionStore.get('_auth_user_backend') == 'backend.teacher.backend.TeacherBackend':
                return True
        except Exception as err:
            return False

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        db_table = "teacher"
