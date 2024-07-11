from backend.baseapp.templatetags import helper
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import *
from backend.baseapp.decorators import *

from .models import *

from django import forms
import django_tables2 as tables
import itertools
from django.utils.html import format_html
import logging
logger = logging.getLogger(__name__)

MODEL = Sitesetting
ROUTE_NAME_PREFIX = 'sitesetting'
MODULE_NAME = 'Site Settings'


class Form(forms.ModelForm):

    # site_heading = forms.CharField(max_length=200)
    admin_email = forms.EmailField(max_length=200)
    # site_address = forms.CharField(max_length=200)
    # mobile_no = forms.CharField(max_length=200)

    

    class Meta:
        model = MODEL
        fields = []

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields['description'].widget.attrs.update({
    #             'id': 'description'
    #         })
    #         self.fields['short_description'].widget.attrs.update({
    #             'id': 'description2'
    #         })



@admin_only
def form(request):
    try:
        initial = {}
        for item in MODEL.objects.all():
            initial[item.key] = item.value

        form = Form(initial=initial)
        if request.method == "POST":

            form = Form(request.POST, request.FILES)
            if form.is_valid():
                for item in request.POST:
                    print(item)
                    MODEL.objects.update_or_create(
                        key=item,
                        defaults={
                            'key': item,
                            'value': request.POST.get(item),
                        },
                    )

                messages.success(request, 'Saved successfully')
                return redirect(ROUTE_NAME_PREFIX)
            else:
                messages.error(request, 'The given data was invalid')

        data = {
            'form': form,
            'ModuleName': MODULE_NAME,
            # 'BackUrl': ROUTE_NAME_PREFIX,
        }
        return render(request, "common/form.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
        return HttpResponse(format(err))
