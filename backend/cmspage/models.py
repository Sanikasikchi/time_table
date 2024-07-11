from django.db import models
from django.template.defaultfilters import slugify
import random
from ckeditor.fields import RichTextField
# from ckeditor_uploader import RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + '-' + str(random.randint(100000, 999999))
    return unique_slug


YES_NO = (('Y', 'Y'), ('N', 'N'))
LEVEL = ((0, 0), (1, 1), (2, 2))

class CMS_Page(models.Model):
    
    parent_id = models.ForeignKey(
        'self', null=True, on_delete=models.CASCADE, blank=True,limit_choices_to = {"level_id": 0})
    level_id = models.IntegerField(null=True, choices=LEVEL, default=0)
    page_title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    meta_title = models.CharField(max_length=200, null=True)
    meta_keyword = models.CharField(max_length=200, null=True)
    meta_desc = models.CharField(max_length=200, null=True)
    # short_description = models.TextField(null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    short_description = RichTextUploadingField(null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    is_header = models.CharField(
        max_length=20, null=True, choices=YES_NO, default="N")
    is_footer = models.CharField(
        max_length=20, null=True, choices=YES_NO, default="N")
    is_active = models.CharField(
        max_length=20, null=True, choices=YES_NO, default="Y")
    sort_order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.page_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.page_title))
        super(CMS_Page, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'CMS Page'
        verbose_name_plural = 'CMS Pages'
        db_table = "cms_page"
