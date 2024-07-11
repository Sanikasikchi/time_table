from django.db import models
from django.template.defaultfilters import slugify
import random
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from backend.teacher.models import Teacher
from backend.classes.models import *


YES_NO = (('Y', 'Y'), ('N', 'N'))
PERIOD = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'))


class Timetable(models.Model):
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)
    schedule_classes = models.ForeignKey(classes_timetable_period, null=True, on_delete=models.CASCADE)
    
    description = RichTextUploadingField(null=True, blank=True)
    is_accepted = models.CharField(max_length=20, null=True, choices=YES_NO, default="N")
    is_moved = models.CharField(max_length=20, null=True, choices=YES_NO, default="N")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.schedule_classes)

    class Meta:
        verbose_name = 'timetable'
        verbose_name_plural = 'timetable'
        db_table = "timetable"
