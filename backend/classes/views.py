import json
from backend.baseapp.templatetags import helper
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import *
from backend.subject.models import Subject

from .models import Classes
from .models import classes_timetable
from .models import classes_timetable_period
from backend.baseapp.decorators import *

from django import forms
import django_tables2 as tables
import itertools
from django.utils.html import format_html
import logging
logger = logging.getLogger(__name__)

MODEL = Classes
ROUTE_NAME_PREFIX = 'classes'
MODULE_NAME = 'Classes'


class Table(tables.Table):
    name = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/edit/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">{{record.name}}</a>')
    timetable = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/timetable/day/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">TimeTable</a>')
    created_at = tables.DateTimeColumn(format='d M Y')
    active = tables.Column(verbose_name='Active',orderable=False, empty_values=())

    def render_active(self, value, record):

            if record.is_active == 'Y':
                # If the value is True (i.e., the record is active), render an active image
                return format_html('<img src="/static/backend/images/active.png" alt="Active" height="20" width="20">')
            else:
                # If the value is False (i.e., the record is inactive), render an inactive image
                return format_html('<img src="/static/backend/images/deactive.png" alt="Inactive" height="20" width="20">')
    class Meta:
        model = MODEL
        attrs = {
            "class": "table table-striped table-bordered DataTable",
            "tbody": {
                "id": "groups"
            }
        }
        # row_attrs = {"data-lookup": lambda record: record.sort_order, "data-pid": lambda record: record.id}
        orderable = False
        empty_text = "No Data Available"
        # fields = "__all__"
        fields = ('name', 'timetable', 'section', 'student_count', 'active')


class Form(forms.ModelForm):

    class Meta:
        model = MODEL
        fields = ["name", 'section', "student_count", "description"]

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
            _object = MODEL.objects.filter(name__icontains=search)
        else:
            _object = MODEL.objects.all()
        data = {
            'table': Table(_object.order_by('-created_at')).paginate(page=request.GET.get("page", 1), per_page=10),
            'ModuleName': MODULE_NAME+'',
            'AddUrl': ROUTE_NAME_PREFIX+'_add',
            'Search': '' if search == None else search,
            'Active_deactive': True,
            'Delete': True,
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
                class_ = form.save()
                
                for day in ('MON', 'TUE', 'WED', 'THUR', 'FRI'):
                    timetable_day = classes_timetable()
                    timetable_day.classes = class_
                    timetable_day.day = day
                    timetable_day.save()

                    period = 0
                    for sub in Subject.objects.all()[:8]:
                        period += 1
                        timetable_period = classes_timetable_period()
                        timetable_period.classes = class_
                        # timetable_period.day = classes_timetable.objects.get(id=int(day_.id))
                        timetable_period.day = day
                        timetable_period.subject = sub
                        timetable_period.period = period
                        timetable_period.save()

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

        # for day in ('MON', 'TUE', 'WED', 'THUR', 'FRI'):
        #     day_ = classes_timetable.objects.update_or_create(
        #         classes=_object,
        #         day=day,
        #         defaults={'classes': _object, 'day': day},
        #     )

            # period = 0
            # for sub in Subject.objects.all()[1:8]:
            #     period += 1
            #     day_ = classes_timetable_period.objects.update_or_create(
            #         classes=_object,
            #         day=day_,
            #         sub=sub,
            #         period=period,
            #         defaults={'classes': _object, 'day': day_, 'sub': sub, 'period': period},
            #     )

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
        messages.success(request, msg)
    except:
        messages.error(request, 'Something went wrong !!')

    return redirect(request.POST.get('prev'))


class Table_TT_day(tables.Table):
    day = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/timetable/day/{{ record.classes_id }}/{{ record.day }}" class="entity_id" dataId="{{ record.id }}">{{record.day}}</a>')

    created_at = tables.DateTimeColumn(format='d M Y')

    class Meta:
        model = MODEL
        attrs = {
            "class": "table table-striped table-bordered DataTable",
            "tbody": {
                "id": "groups"
            }
        }
        # row_attrs = {"data-lookup": lambda record: record.sort_order, "data-pid": lambda record: record.id}
        orderable = False
        empty_text = "No Data Available"
        # fields = "__all__"
        fields = ('day', 'created_at')


@admin_only
def timetable_day(request, pk):

    try:
        _object = classes_timetable.objects.filter(classes=pk)
        data = {
            'table': Table_TT_day(_object.order_by('created_at')).paginate(page=request.GET.get("page", 1), per_page=10),
            'ModuleName': 'Timetable (day) -  ' + str(MODEL.objects.get(id=pk)),
            # 'Delete': True,
            'BackUrl': ROUTE_NAME_PREFIX+'',
        }
        return render(request, "common/table.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


class Table_TT_period(tables.Table):
    subject = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/timetable/day/{{ record.classes_id }}/{{ record.day }}/edit/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">{{record.subject}}</a>')

    created_at = tables.DateTimeColumn(format='d M Y')

    class Meta:
        model = classes_timetable_period
        attrs = {
            "class": "table table-striped table-bordered DataTable",
            "tbody": {
                "id": "groups"
            }
        }
        # row_attrs = {"data-lookup": lambda record: record.sort_order, "data-pid": lambda record: record.id}
        orderable = False
        empty_text = "No Data Available"
        # fields = "__all__"
        fields = ('subject', 'period', 'created_at')


@admin_only
def timetable_period(request, pk, day):
    try:
        _object = classes_timetable_period.objects.filter(classes=pk, day__contains=day)
        data = {
            'table': Table_TT_period(_object.order_by('period')).paginate(page=request.GET.get("page", 1), per_page=10),
            'ModuleName': 'Timetable ('+str(day)+') - ' + str(MODEL.objects.get(id=pk)),
            # 'Delete': True,
            'BackUrl': 'timetable_period_add',
            'BackUrl_Q': str(pk),
            'AddUrl': 'timetable_period_add',
            'AddUrl_Q': str(pk)+'/'+str(day)+'/add',
        }
        return render(request, "common/table.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


class Form_tt_period(forms.ModelForm):

    class Meta:
        model = classes_timetable_period
        fields = ['subject', "period"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'title': str(self.fields[field].required),
            })


def timetable_period_add_f(request, pk, day):
    try:
        form = Form_tt_period()
        if request.method == "POST":
            form = Form_tt_period(request.POST, request.FILES)
            if form.is_valid():
                form.instance.classes_id = pk
                form.instance.day = day
                form.save()
                messages.success(request, 'Saved successfully')
                return redirect('/administrator/classes/timetable/day/'+str(pk)+'/'+str(day))
            else:
                messages.error(request, 'The given data was invalid')

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Add',
            'BackUrl': 'timetable_period_add',
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))
    
def timetable_period_edit(request, pk, day,p2id):
    try:
        _object = classes_timetable_period.objects.get(id=p2id)
        form = Form_tt_period(instance=_object)
        if request.method == "POST":
            form = Form_tt_period(request.POST, request.FILES,
                        instance=_object)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated successfully')
                return redirect('/administrator/classes/timetable/day/'+str(pk)+'/'+str(day))

        data = {
            'form': form,
            'ModuleName': MODULE_NAME+' Update',
            'BackUrl': 'timetable_period_add',
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))
