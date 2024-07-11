import json
from backend.baseapp.templatetags import helper
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import *

from .models import CMS_Page
from backend.baseapp.decorators import *

from django import forms
import django_tables2 as tables
import itertools
from django.utils.html import format_html
import logging
logger = logging.getLogger(__name__)

MODEL = CMS_Page
ROUTE_NAME_PREFIX = 'cmspage'
MODULE_NAME = 'CMS Page'


class Table(tables.Table):
    page_title = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/edit/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">{{record.page_title}}</a>')
    sub_pages = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/list/{{ record.id }}">View</a>')
    is_menu = tables.TemplateColumn('{{ record.is_header }}')
    created_at = tables.DateTimeColumn(format='d M Y')

    class Meta:
        model = MODEL
        attrs = {
            "class": "table table-striped table-bordered DataTable",
            "tbody": {
                "id": "groups"
            }
        }
        row_attrs = {"data-lookup": lambda record: record.sort_order, "data-pid": lambda record: record.id}
        orderable = False
        empty_text = "No Data Available"
        # fields = "__all__"
        fields = ('page_title', 'slug', 'sub_pages', 'is_menu', 'is_footer',
                  'is_active', 'sort_order')


class Table2(tables.Table):
    page_title = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/edit2/{{ record.parent_id_id }}/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">{{record.page_title}}</a>')

    class Meta:
        model = MODEL
        attrs = {
            "class": "table table-striped table-bordered DataTable",
            "tbody": {
                "id": "groups"
            }
        }
        row_attrs = {"data-lookup": lambda record: record.sort_order, "data-pid": lambda record: record.id}
        orderable = False
        empty_text = "No Data Available"
        # fields = "__all__"
        fields = ('page_title', 'slug', 'is_header', 'is_footer',
                  'is_active', 'sort_order')


class Form(forms.ModelForm):

    class Meta:
        model = MODEL
        fields = [
            # "parent_id",
            "page_title","slug", "meta_title", "meta_keyword",
            "meta_desc", "short_description", "description"]
        # exclude = ['level_id', 'slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'title': str(self.fields[field].required),
            })
            self.fields['description'].widget.attrs.update({
                'id': 'description'
            })
            self.fields['short_description'].widget.attrs.update({
                'id': 'description2'
            })


# class Form2(forms.ModelForm):
#     # parent_id = forms.ChoiceField(required=True,choices=MODEL.objects.filter(parent_id__isnull=True))
#     class Meta:
#         model = MODEL
#         fields = [
#             "parent_id",
#             "page_title", "meta_title", "meta_keyword",
#             "meta_desc", "short_description", "description"]
#         # exclude = ['level_id', 'slug']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields['description'].widget.attrs.update({
#                 'id': 'description'
#             })
#             self.fields['short_description'].widget.attrs.update({
#                 'id': 'description2'
#             })


@admin_only
def list(request):
    search = request.GET.get("search")
    try:
        if not search == None:
            _object = MODEL.objects.filter(
                page_title__icontains=search) | MODEL.objects.filter(slug__contains=search)
        else:
            _object = MODEL.objects.filter(parent_id__isnull=True)
        data = {
            'table': Table(_object.order_by('sort_order')).paginate(page=request.GET.get("page", 1), per_page=10),
            'ModuleName': MODULE_NAME+'',
            'AddUrl': ROUTE_NAME_PREFIX+'_add',
            # 'ExportUrl': True,
            # 'ImportUrl': True,
            'Search': '' if search == None else search,
            'Active_deactive': True,
            'Delete': True,
            'Is_Menu': True,
            'Is_Footer': True,
            'sortable': True
        }
        return render(request, "common/table.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@admin_only
def add(request):
    try:
        form = Form()
        form.fields['slug'].disabled  = True
        if request.method == "POST":
            form = Form(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Saved successfully')
                return redirect(ROUTE_NAME_PREFIX)
            else:
                messages.error(request, 'The given data was invalid')

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Add',
            'BackUrl': ROUTE_NAME_PREFIX,
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
                return redirect(ROUTE_NAME_PREFIX)

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Update',
            'BackUrl': ROUTE_NAME_PREFIX,
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))


@admin_only
def sublist(request, pk):
    search = request.GET.get("search")
    try:
        if not search == None:
            _object = MODEL.objects.filter(
                page_title__contains=search) | MODEL.objects.filter(slug__contains=search)
        else:
            _object = MODEL.objects.all()
        data = {
            'table': Table2(CMS_Page.objects.filter(parent_id=pk).order_by('sort_order')),
            'ModuleName': MODULE_NAME+'',
            'AddUrl': ROUTE_NAME_PREFIX+'_add2',
            'AddUrl_Q': str(pk),
            # 'ExportUrl': True,
            # 'ImportUrl': True,
            'Search': '' if search == None else search,
            'Active_deactive': True,
            'Delete': True,
            'Is_Menu': True,
            'Is_Footer': True,
            'sortable': True
        }
        return render(request, "common/table.html", data)
    except Exception as err:
        logger.error(format(err))
        return HttpResponse(format(err))


@admin_only
def add2(request, parent=0):
    try:
        form = Form()
        form.fields['slug'].disabled  = True
        # form.fields['parent_id'].initial = parent

        if request.method == "POST":
            form = Form(request.POST, request.FILES)
            if form.is_valid():
                form.instance.parent_id = MODEL.objects.get(id=parent)
                form.instance.level_id = 1
                form.instance.sort_order = helper.sort_order(MODEL=MODEL)
                form.save()
                messages.success(request, 'Saved successfully')
                return redirect('/administrator/'+ROUTE_NAME_PREFIX+'/list/'+parent)
            else:
                messages.error(request, 'The given data was invalid')

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Add',
            'BackUrl': ROUTE_NAME_PREFIX,
            'BackUrl_Q': parent,
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))


@admin_only
def edit2(request, parent, pk):
    try:
        _object = MODEL.objects.get(id=pk)
        form = Form(instance=_object)
        if request.method == "POST":
            form = Form(request.POST, request.FILES,
                        instance=_object)
            if form.is_valid():
                form.instance.parent_id = MODEL.objects.get(id=parent)
                form.instance.level_id = 1
                form.instance.sort_order = helper.sort_order(MODEL=MODEL)
                form.save()
                messages.success(request, 'Updated successfully')
                # return redirect(ROUTE_NAME_PREFIX)
                return redirect('/administrator/'+ROUTE_NAME_PREFIX+'/list/'+str(parent))

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Update',
            'BackUrl': ROUTE_NAME_PREFIX,
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
        elif request.POST.get('operationFlag') == 'setHeader':
            _object.update(is_header='Y')
            msg = 'successfully set as header.'
            pass
        elif request.POST.get('operationFlag') == 'Unset from Header':
            _object.update(is_header='N')
            msg = 'successfully unset from header.'
            pass
        elif request.POST.get('operationFlag') == 'Set As Fotter':
            _object.update(is_footer='Y')
            msg = 'successfully set as header.'
            pass
        elif request.POST.get('operationFlag') == 'Unset from Fotter':
            _object.update(is_footer='N')
            msg = 'successfully set as header.'
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

    return redirect(request.POST.get('prev'))
