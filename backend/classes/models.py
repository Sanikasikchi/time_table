from django.db import models
from django.template.defaultfilters import slugify
import random
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from backend.subject.models import Subject

YES_NO = (('Y', 'Y'), ('N', 'N'))
SECTION = (('A', 'A'), ('B', 'B'))
DAY = (('MON', 'MON'), ('TUE', 'TUE'), ('WED', 'WED'),
       ('THUR', 'THUR'), ('FRI', 'FRI'))
PERIOD = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
          ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'))


class Classes(models.Model):

    name = models.CharField(max_length=200, null=True)
    student_count = models.IntegerField(null=True)
    description = RichTextUploadingField(null=True, blank=True)
    section = models.CharField(
        max_length=20, null=True, choices=SECTION, default="A")
    is_active = models.CharField(
        max_length=20, null=True, choices=YES_NO, default="Y")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Classes'
        verbose_name_plural = 'classes'
        db_table = "classes"


class classes_timetable(models.Model):

    classes = models.ForeignKey(Classes, null=True, on_delete=models.CASCADE)
    day = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.classes

    class Meta:
        verbose_name = 'classes_timetable'
        verbose_name_plural = 'classes_timetable'
        db_table = "classes_timetable"


class classes_timetable_period(models.Model):

    classes = models.ForeignKey(Classes, null=True, on_delete=models.CASCADE)
    # day = models.ForeignKey(classes_timetable, null=True, on_delete=models.SET_NULL)
    day = models.CharField(max_length=200, null=True)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)
    period = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.classes)+' '+str(self.classes.section)+' : '+str(self.subject)+' ('+str(self.day)+')'+' Period - '+str(self.period)
        return str(self.period)+' - '+str(self.sub)

    class Meta:
        verbose_name = 'classes_timetable_period'
        verbose_name_plural = 'classes_timetable_period'
        db_table = "classes_timetable_period"
