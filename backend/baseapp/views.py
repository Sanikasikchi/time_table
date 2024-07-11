import time
import random
from django.conf import settings
from django.core.mail import send_mail
from logging import exception
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.urls import reverse
from backend.baseapp.decorators import *
from .forms import *
from .templatetags import helper
from backend.subject.models import Subject
from backend.classes.models import Classes
from backend.teacher.models import Teacher
from backend.timetable.models import Timetable
import logging

logger = logging.getLogger(__name__)


@unauthenticated_admin
def DjangoLogin(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            print(122)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "administrator"))
            else:
                messages.info(request, "Username OR password is incorrect")

        data = {}
        return render(request, "includes/login.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@unauthenticated_admin
def adminforgotpassword(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            user = User.objects.filter(email__contains=email)[:1]

            if user is not None:
                request.session["forgot_pass_email"] = email
                request.session["forgot_pass_otp"] = random.randint(
                    100000, 999999)
                request.session["forgot_pass_otp"] = random.randint(100000, 999999)
                request.session["forgot_pass_time"] = time.time()
                send_mail(
                    subject="Django | OTP",
                    message="forgot password",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.session["forgot_pass_email"]],
                    html_message=str(request.session["forgot_pass_otp"])
                    + " is your OTP to reset password. Valid for 10 mins.",
                )
                messages.info(request, "OTP sent on your email.")
                return redirect("/administrator/otp")
            else:
                messages.info(request, "No User found.")
        data = {}
        return render(request, "includes/forgotpassword.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@unauthenticated_admin
def sendOTP(request, typ=0):
    if request.session.get("forgot_pass_otp") is None:
        messages.info(request, "Something went wrong, Try Again.")
        return redirect("/administrator/forgot-password")

    if typ == 0:
        if request.session.get("forgot_pass_time") is not None:
            timeDiff = (time.time() - request.session["forgot_pass_time"]) / 60
            if timeDiff < 1:
                messages.info(
                    request, "Wait for sometime, before requesting again for otp."
                )
                return redirect("/administrator/otp")

    request.session["forgot_pass_otp"] = random.randint(100000, 999999)
    request.session["forgot_pass_time"] = time.time()
    send_mail(
        subject="Django | OTP",
        message="forgot password",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.session["forgot_pass_email"]],
        html_message=str(request.session["forgot_pass_otp"])
        + " is your OTP to reset password. Valid for 10 mins.",
    )
    messages.info(request, "OTP sent on your email.")
    return redirect("/administrator/otp")


@unauthenticated_admin
def adminotp(request):
    try:
        if request.method == "POST":
            timeDiff = (time.time() - request.session["forgot_pass_time"]) / 60
            if timeDiff > 10:
                messages.info(request, "OTP Expired.")
                return redirect("/administrator/forgot-password")

            if request.session.get("forgot_pass_otp") is not None:
                if int(request.session["forgot_pass_otp"]) == int(request.POST["otp"]):
                    return redirect("/administrator/reset-password")
                else:
                    messages.info(request, "Incorrect OTP.")
            else:
                messages.info(request, "Something went wrong, Try Again.")
                return redirect("/administrator/forgot-password")

        data = {}
        return render(request, "includes/otp.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@unauthenticated_admin
def adminresetpassword(request):
    try:
        if request.method == "POST":
            if request.POST["password"] != request.POST["confirm_password"]:
                messages.info(request, "Passwords do not match.")
            else:
                user = User.objects.get(
                    email__exact=request.session["forgot_pass_email"]
                )
                if user is not None:
                    user.set_password(request.POST["password"])
                    user.save()

                    del request.session["forgot_pass_email"]
                    del request.session["forgot_pass_otp"]
                    del request.session["forgot_pass_time"]

                    messages.success(request, "Password updated.")
                    return redirect("/administrator/login")
                else:
                    messages.info(request, "Something went wrong, Try Again.")
                    return redirect("/administrator/forgot-password")
        data = {}
        return render(request, "includes/reset-password.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


def logoutUser(request):
    try:
        logout(request)
        return redirect("adminlogin")
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


@admin_only
def index(request):

    try:
        data = {
            "subjects": Subject.objects.count(),
            "classes": Classes.objects.count(),
            "teachers": Teacher.objects.count(),
            "conducted": Timetable.objects.filter(is_accepted="Y").count(),
        }
        return render(request, "includes/dashboard.html", data)
    except Exception as err:
        logger.error(format(err))
        return helper.error_handdler(err)


def sessiontest(request):
    # Set a session value
    request.session["my_car"] = "mini"

    # Delete a session value
    # del request.session['my_car']

    # Get a session value
    if request.session.get("my_car") is not None:
        return HttpResponse(request.session["my_car"])
    else:
        return HttpResponse("Session is Empty")


def slug(request, the_slug):
    try:
        data = {"cmsData": CMS_Page.objects.get(slug=the_slug.lower())}
        return render(request, "common/cms.html", data)
    except:
        return redirect("administrator")
    # except Exception as err:
    #     return HttpResponse(format(err))
