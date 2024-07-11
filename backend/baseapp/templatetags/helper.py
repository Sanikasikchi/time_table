import hashlib
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core import serializers
from django.http import HttpResponseServerError
from django import forms
from django.db.models.query import QuerySet
from collections.abc import Iterable
import json
from DjangoDevelopment.config.environ import APP_ENV
from django.core.exceptions import *
# from backend.customer.models import Customer as Customers
from backend.cmspage.models import CMS_Page
# from backend.categories.models import Categories
from genericpath import exists
from django import template
from django.urls import resolve
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
register = template.Library()


@register.filter()
def low(value):
    return value.lower()


# @register.simple_tag
# def CustomersData():
#     return Customers.objects.all()


@register.simple_tag
def tableindex(value, page='0'):
    if isinstance(page, int):
        page = page-1
        return value+(page*10)
    else:
        return value

import decimal
def currencyInIndiaFormat(n):
  d = decimal.Decimal(str(n))
  if d.as_tuple().exponent < -2:
    s = str(n)
  else:
    s = '{0:.2f}'.format(n)
  l = len(s)
  i = l-1;
  res = ''
  flag = 0
  k = 0
  while i>=0:
    if flag==0:
      res = res + s[i]
      if s[i]=='.':
        flag = 1
    elif flag==1:
      k = k + 1
      res = res + s[i]
      if k==3 and i-1>=0:
        res = res + ','
        flag = 2
        k = 0
    else:
      k = k + 1
      res = res + s[i]
      if k==2 and i-1>=0:
        res = res + ','
        flag = 2
        k = 0
    i = i - 1

  return res[::-1]

@register.filter()
def price(value):
    return '£'+str(currencyInIndiaFormat(value))

@register.simple_tag
def table_showing_of(total_rows, rows_per_page=0, current_page=1):
    if current_page == 1:
        start = str(1)
        end = str(rows_per_page)
    else:
        current_page = current_page-1
        start = str(1+(10*current_page))
        end = str(rows_per_page+(10*current_page))
    return 'Showing '+start+' to '+end+' of '+str(total_rows)


@register.simple_tag(name='seo')
def seo(path=''):
    page = path.split("/")
    cms = None
    cat = None
    for item in page:
        if not len(item) == 0:
            try:
                cms = CMS_Page.objects.filter(slug=item.lower()).first()
                print(item.lower())
            except:
                pass
            break

            # try:
            #     cat = categories.objects.filter(slug=item.lower()).first()
            #     print(item.lower())
            # except:
            #     pass
            # break

    if cms is not None:
        return {
            'page_title': 'Django::'+cms.page_title,
            'title': cms.meta_title,
            'keywords': cms.meta_keyword,
            'descriptions': cms.meta_desc,
        }
    if cat is not None:
        return {
            'page_title': cat.name,
            'title': cat.meta_title,
            'keywords': cat.meta_keyword,
            'descriptions': cat.meta_desc,
        }
    else:
        return {
            'page_title': 'Django',
            'title': 'title',
            'keywords': 'keywords',
            'descriptions': 'descriptions',
        }


def error_handdler(error):
    if APP_ENV == 'prod':
        return HttpResponseServerError('<h1>Server Error (500)</h1>')
    else:
        try:
            raise error.__name__(error)
        except:
            raise SuspiciousOperation(error)


def p(data=''):
    try:
        print(data)
        if data:
            if isinstance(data, Iterable):
                if isinstance(data, str):
                    return_data = {'data': str(data)}
                    print('>>>>>>>>> String')
                elif isinstance(data, QuerySet):
                    return_data = json.loads(
                        serializers.serialize('json', data))
                    print('>>>>>>>>> QuerySet')
                else:
                    return_data = dict(data)
                    print('>>>>>>>>> dict')
            else:
                return_data = serializers.serialize('json', [data])
                print('>>>>>>>>> Not Iterable')

    except Exception as err:
        return_data = {'error': format(err)}

    return HttpResponse(json.dumps(return_data, sort_keys=True, indent=4), content_type="application/json")


class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        if value is not None:
            input_html = super().render(name, value, attrs=None, **kwargs)
            img_html = mark_safe(f'<br><img width=50 height=50 src="{value.url}"/><br>')
            return f'{input_html}{img_html}'
        else:
            input_html = super().render(name, value, attrs=None, **kwargs)
            return f'{input_html}'


NUM_COLORS = 10
# @register.filter


def avatar(name, id):
    print(name)
    color_ix = int(hashlib.md5(str(id).encode()).hexdigest(), 16) % NUM_COLORS
    context = {'color_ix': '#ff0000', 'letter': name}
    return render_to_string('avatar.svg', context)

# # accounts/templates/accounts/avatar.svg
# <svg version="1.1" xmlns="http://www.w3.org/2000/svg" class="avatar color-{{ color_ix }}">
#   <rect x="0" y="0" width="100%" height="100%"></rect>
#   <text x="50%" y="50%">{{ letter }}</text>
# </svg>


@register.simple_tag
def CMS_menu(parent_id=0):
    if parent_id == 0:
        cms = CMS_Page.objects.filter(level_id=0,
                                      is_footer__contains='Y',
                                      is_active__contains='Y').order_by('sort_order')
    else:
        cms = CMS_Page.objects.filter(parent_id=parent_id,
                                      is_footer__contains='Y',
                                      is_active__contains='Y').order_by('sort_order')

    if cms == None:
        return []

    return cms


def sort_order(MODEL):
    try:
        return int(MODEL.objects.all().order_by('sort_order').reverse()[0].sort_order)+1
    except:
        return 1


# @register.simple_tag
# def CAT_menu(parent_id=0):
#     if parent_id == 0:
#         cat = Categories.objects.filter(level_id=0,
#                                         is_menu__contains='Y',
#                                         is_active__contains='Y').order_by('sort_order')
#     else:
#         cat = Categories.objects.filter(parent_id=parent_id,
#                                         is_menu__contains='Y',
#                                         is_active__contains='Y').order_by('sort_order')

#     if cat == None:
#         return []

#     return cat

from DjangoDevelopment.config.environ import env, BASE_DIR
from django.templatetags.static import static
import os

def image_absolute_path(static_path):

    media = str(BASE_DIR)+'/'+str(static_path)
    staticImg = str(BASE_DIR)+'/'+str(static(static_path))

    if os.path.exists(media):
        path = str(static_path)
    elif os.path.exists(staticImg):
        path = str(static(static_path))
    else:
        path = static_path

    return path

import random
from django.template.defaultfilters import slugify
def unique_slugify(instance, slug):
    slug = slugify(slug)
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + '-' + str(random.randint(100000, 999999))
    return unique_slug