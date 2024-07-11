from django.core.files.storage import FileSystemStorage
from collections.abc import Iterable
import logging
from backend.baseapp.templatetags import helper
import io
from dataclasses import field
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import django_tables2 as tables
from django import forms
from django.utils.html import format_html
import itertools
from django.http import HttpResponse
import json
from .models import *
from backend.baseapp.decorators import *

from import_export import fields, resources, widgets
from tablib import Dataset
from datetime import datetime
from django.utils import formats
date_joined = datetime.now()
formatted_datetime = formats.date_format(date_joined, "SHORT_DATETIME_FORMAT")

logger = logging.getLogger(__name__)

attrsForTable = {
    "class": "table table-striped table-bordered DataTable",
    "tbody": {
        "id": "groups"
    }
}

MODEL = Banner
ROUTE_NAME_PREFIX = 'banner'
MODULE_NAME = 'Banner'


class Table(tables.Table):
    title = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/edit/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">{{record.title}}</a>')
    image = tables.TemplateColumn('#')
    created_at = tables.DateTimeColumn(format ='d M Y')

    def render_image(self, value):
        if value:
            return format_html('<img src="/media/{}" width=50 height=50 />', value)
        else:
            return format_html('<img src="/media/no_image_available.png"  width=50 height=50 />')

    class Meta:
        model = MODEL
        attrs = attrsForTable
        orderable = False
        row_attrs = {"data-lookup": lambda record: record.sort_order, "data-pid": lambda record: record.id}
        empty_text = "No Data Available"
        # fields = "__all__"
        fields = ('title', 'image',
                  'is_active','sort_order')  # fields to display


class Form(forms.ModelForm):

    # image = forms.ImageField(required=False)
    # is_active = forms.CharField(required=False)
    image = forms.ImageField(widget=helper.ImagePreviewWidget)

    class Meta:
        model = MODEL
        fields = "__all__"
        exclude = ['is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'title': str(self.fields[field].required),
            }) 
            self.fields['description'].widget.attrs.update({
                'id': 'description'
            })


@admin_only
def list(request):
    search = request.GET.get("search")
    try:
        if not search == None:
            _object = MODEL.objects.filter(
                page_title__icontains=search) | MODEL.objects.filter(slug__contains=search)
        else:
            _object = MODEL.objects.all()
        data = {
            'table': Table(_object.order_by('sort_order')).paginate(page=request.GET.get("page", 1), per_page=10),
            'ModuleName': MODULE_NAME+'',
            'AddUrl': ROUTE_NAME_PREFIX+'_add',
            # 'ExportUrl': True,
            # 'ImportUrl': True,
            'Search': '' if search == None else search,
            'Active_deactive': True,
            'Delete': True,
            'sortable': True
            # 'Is_Menu': True,
            # 'Is_Footer': True,
        }
        return render(request, "common/table.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@admin_only
def add(request):
    try:
        form = Form()
        if request.method == "POST":
            form = Form(request.POST, request.FILES)
            if form.is_valid():
                form.instance.sort_order = helper.sort_order(MODEL=MODEL)
                form.save()
                messages.success(request, 'Saved successfully')
                return redirect(ROUTE_NAME_PREFIX+'_list')
            else:
                messages.error(request, 'The given data was invalid')
 
        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Add',
            'BackUrl': ROUTE_NAME_PREFIX+'_list',
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))


@admin_only
def edit(request, pk):
    try:
        _object = MODEL.objects.get(id=pk)
        form = Form(instance=_object)
        if request.method == "POST":
            form = Form(request.POST, request.FILES,
                        instance=_object)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated successfully')
                return redirect(ROUTE_NAME_PREFIX+'_list')

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Update',
            'BackUrl': ROUTE_NAME_PREFIX+'_list',
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))


@admin_only
def operations(request):
    try:
        msg = ''
        _object = MODEL.objects.filter(id__in=request.POST.getlist('chk[]'))
        if request.POST.get('operationFlag') == 'active':
            _object.update(is_active='Y')
            msg = 'successfully activated.'
            pass
        elif request.POST.get('operationFlag') == 'deactive':
            _object.update(is_active='N')
            msg = 'successfully de-activated.'
            pass
        elif request.POST.get('operationFlag') == 'delete':
            _object.delete()
            msg = 'successfully deleted.'
        elif request.POST.get('operationFlag') == 'Sorting':
            ordered_ids = json.loads(request.POST.get('post_sort_id'))
            for x in ordered_ids:
                MODEL.objects.filter(id=ordered_ids[x]).update(sort_order=int(x))
            msg = 'successfully sorted.'

        messages.success(request, msg)
    except:
        messages.error(request, 'Something went wrong !!')

    return redirect(ROUTE_NAME_PREFIX+'_list')
