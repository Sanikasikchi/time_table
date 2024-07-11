from django.conf import settings
from django.core.mail import send_mail
from django import forms

# from backend.customer.backend import CustomerBackend
from django.contrib.auth.hashers import make_password, check_password
from django.templatetags.static import static
from DjangoDevelopment.config.environ import env, BASE_DIR
from django.contrib.staticfiles import finders

# from backend.customer.models import Customer
from logging import exception
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render

from .decorators import *
from .forms import *
from backend.baseapp.templatetags import helper
from backend.timetable.models import Timetable
from backend.banner.models import Banner
from backend.teacher.models import Teacher
from backend.classes.models import *
import logging

logger = logging.getLogger(__name__)


@unauthenticated_user
def DjangoLogin(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "home"))
            else:
                messages.info(request, "Username OR password is incorrect")

        data = {}
        return render(request, "login.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


# @unauthenticated_user
# def registerPage(request):
#     try:
#         form = Form()
#         if request.method == "POST":
#             form = Form(request.POST)
#             if form.is_valid():
#                 form.instance.password = make_password(request.POST.get("password"))
#                 user = form.save()
#                 email = form.cleaned_data.get("email")

#                 messages.success(request, "Account was created for " + email)

#                 return redirect("login")

#         context = {"form": form}
#         return render(request, "register.html", context)
#     except Exception as err:
#         logger.error(format(err))
#         return helper.error_handdler(err)


def logoutUser(request):
    try:
        logout(request)
        return redirect("login")
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@authenticated_user
def index(request):
    try:
        # data = {
        #     "banner": Banner.objects.filter(is_active__contains="Y").order_by(
        #         "sort_order"
        #     ),
        #     "cmsData": CMS_Page.objects.get(slug="home", is_active__contains="Y"),
        # }
        # return render(request, "includesf/home.html", data)
        # return render(request, "includesf/admin.html")
        return redirect('TeacherEntry')
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


class Form(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ["name", "classes", "subject", "phoneNo", "email", "prn"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'title': str(self.fields[field].required),
            })

# @login_required(login_url='login')


def teacherEntry(request):
    try:
        _object = request.user
        # _object = Teacher.objects.get(id=pk)
        form = Form(instance=_object)
        if request.method == "POST":
            form = Form(request.POST, request.FILES, instance=_object)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated successfully')
                return redirect('TeacherEntry')

        data = {
            'form': form,
        }
        return render(request, "teacher_entry.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


def manageClasses(request):
    try:
        # dept = Teacher.objects.get(id=request.user.id).classes.only(
        #     'id').values_list('pk', flat=True)
        # subs = Teacher.objects.get(id=request.user.id).subject.only(
        #     'id').values_list('pk', flat=True)
        tt = Timetable.objects.filter(teacher=request.user, is_moved='N').values_list('schedule_classes', flat=True)
        print(list(tt))
        classes = classes_timetable_period.objects.filter(
            # classes__in=list(dept),
            # subject__in=list(subs),
        ).filter(id__in=list(tt)).order_by('created_at')

        data = {
            'classes': classes,
        }
        return render(request, "manage_classes.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)

from backend.sitesettings.models import Sitesetting

def conductClasses(request, tt_id):
    try:
        tt = Timetable.objects.filter(teacher=request.user,schedule_classes=classes_timetable_period.objects.get(id=tt_id),is_moved='N')
        send_mail(
            subject="Django | Sheduled Class Accepted",
            message="Sheduled Class Accepted",
            from_email=request.user.email,
            recipient_list=[Sitesetting.objects.get(key="admin_email").value, request.user.email],
            html_message="Sheduled Class Accepted. <b>" +
            str(tt[0].schedule_classes)+"</b>"
        )
        tt.update(is_accepted='Y',is_moved='Y')

        return redirect(request.GET.get("next", "ManageClasses"))
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


def cancelClasses(request, tt_id):
    try:
        tt = Timetable.objects.filter(teacher=request.user,schedule_classes=classes_timetable_period.objects.get(id=tt_id),is_moved='N')
        send_mail(
            subject="Django | Sheduled Class Cancelled",
            message="Sheduled Class Cancelled",
            from_email=request.user.email,
            recipient_list=[Sitesetting.objects.get(key="admin_email").value, request.user.email],
            html_message="Sheduled Class Cancelled. <b>" +
            str(tt[0].schedule_classes) + "</b>"
        )
        tt.update(is_accepted='N',is_moved='Y')

        return redirect(request.GET.get("next", "ManageClasses"))
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


def historyClasses(request):
    try:
        data = {
            'classes': Timetable.objects.filter(teacher=request.user, is_accepted="Y",is_moved="Y"),
            'classes_n': Timetable.objects.filter(teacher=request.user, is_accepted="N",is_moved="Y"),
        }
        return render(request, "class_history.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)
