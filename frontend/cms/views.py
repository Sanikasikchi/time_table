from django.views.generic import RedirectView
from logging import exception
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render,reverse
from django.http import HttpResponseServerError

from frontend.baseappf.decorators import *
from backend.baseapp.templatetags import helper
from backend.cmspage.models import CMS_Page
import logging
logger = logging.getLogger(__name__)

# from frontend.product_listing.views import slug as cat_slug
 

def slug(request, the_slug):
    try:
        data = {
            'cmsData': CMS_Page.objects.get(slug=the_slug.lower())
        }
        if the_slug.lower() == 'company':
            return render(request, "company.html", data)
            pass

        return render(request, "cms.html", data)
    # except Exception as err:
    #     return helper.error_handdler(err)
    except:
        return cat_slug(request=request, the_slug=the_slug)
