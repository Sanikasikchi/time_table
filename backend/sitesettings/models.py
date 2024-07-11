from django.db import models

# Create your models here.


class Sitesetting(models.Model):
    key = models.CharField(max_length=200, null=False,  unique=True)
    value = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'sitesetting'
        verbose_name_plural = 'sitesettings'
        db_table = "sitesetting"
