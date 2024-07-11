import json
from backend.baseapp.templatetags import helper
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import *

from .models import Timetable
from backend.classes.models import classes_timetable_period
from backend.teacher.models import Teacher

from backend.baseapp.decorators import *

from django import forms
import django_tables2 as tables
import itertools
from django.utils.html import format_html
import logging
logger = logging.getLogger(__name__)

MODEL = Timetable
ROUTE_NAME_PREFIX = 'timetable'
MODULE_NAME = 'Timetable'


class Table(tables.Table):
    schedule_classes = tables.TemplateColumn(
        '<a href="/administrator/'+ROUTE_NAME_PREFIX+'/edit/{{ record.id }}" class="entity_id" dataId="{{ record.id }}">{{record.schedule_classes}}</a>')
    created_at = tables.DateTimeColumn(format='d M Y')
    accepted = tables.Column(verbose_name='Active',orderable=False, empty_values=())

    def render_accepted(self, value, record):

            if record.is_accepted == 'Y':
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
        fields = ('schedule_classes', 'teacher', 'accepted')


class DateInput(forms.DateInput):
    input_type = 'date'


class Form(forms.ModelForm):

    class Meta:
        model = MODEL
        fields = ["schedule_class","teacher","is_accepted", "description"]
        # widgets = {
        #     'schedule_date': DateInput(),
        # }

    schedule_class = forms.ModelMultipleChoiceField(
                queryset=classes_timetable_period.objects.all(),
                widget=forms.SelectMultiple
            )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'title': str(self.fields[field].required),
            })
            self.fields['description'].widget.attrs.update({
                'id': 'description'
            })

class Form2(forms.ModelForm):

    class Meta:
        model = MODEL
        fields = ["schedule_classes", "teacher","is_accepted", "description"]
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
            # 'Active_deactive': True,
            'Delete': True,
        }
        return render(request, "common/table.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)

from django.conf import settings
from django.core.mail import send_mail
from backend.sitesettings.models import Sitesetting
@admin_only
def add(request):
    try:
        form = Form()
        if request.method == "POST":
            form = Form(request.POST, request.FILES)
            if form.is_valid(): 
                subject = str ('')
                teacher=Teacher.objects.get(id=request.POST.get('teacher'))
                for x in request.POST.getlist('schedule_class'):
                    schedule_classes = classes_timetable_period.objects.get(id=x)
                    subject += str(schedule_classes)
                    subject += str (', ')
                    MODEL.objects.get_or_create(
                        schedule_classes=schedule_classes,
                        teacher=teacher,
                        is_accepted=request.POST.get('is_accepted'),
                        description=request.POST.get('description'),
                        defaults={
                                    'schedule_classes':classes_timetable_period.objects.get(id=x),
                                    'teacher':Teacher.objects.get(id=request.POST.get('teacher')),
                                    'is_accepted':'N',
                            },
                        )
                    pass

                send_mail(
                    subject="Django | Sheduled Class Alloted",
                    message="Sheduled Class Alloted",
                    from_email=Sitesetting.objects.get(key="admin_email"),
                    recipient_list=[teacher.email],
                    html_message="Sheduled Class Alloted. <b>" +
                    str(subject[:-2])+"</b>"
                )
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
        form = Form2(instance=_object)
        if request.method == "POST":
            form = Form2(request.POST, request.FILES, instance=_object)
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
