from django.urls import path
from django.conf.urls import include


from backend.baseapp import views as baseapp
from backend.sitesettings import views as sitesetting
from backend.cmspage import views as cmspage
from backend.banner import views as banner
from backend.sitesettings import views as sitesetting

from backend.teacher import views as teacher
from backend.subject import views as subject
from backend.classes import views as classes
from backend.timetable import views as timetable

urlpatterns = [
    path('login', baseapp.DjangoLogin, name='adminlogin'),
    path('forgot-password', baseapp.adminforgotpassword, name="adminforgotpassword"),
    path('otp', baseapp.adminotp, name="adminotp"),
    path('reset-password', baseapp.adminresetpassword, name="adminresetpassword"),
    path('resend-otp', baseapp.sendOTP, name="adminresendOTP"),
    path('logout/', baseapp.logoutUser, name="adminlogout"),
    # path('register/', baseapp.registerPage, name="register"),

    # sitesetting
    path('sitesetting', sitesetting.form, name='sitesetting'),

    path('session', baseapp.sessiontest, name='session'),
    path('', baseapp.index, name='administrator'),

    # banners
    path('banner/list', banner.list, name="banner_list"),
    path('banner/add', banner.add, name="banner_add"),
    path('banner/edit/<int:pk>', banner.edit, name="banner_edit"),
    path('banner/change-status', banner.operations, name="banner_operation"),

    # cms
    path('cmspage/list', cmspage.list, name="cmspage"),
    path('cmspage/add/', cmspage.add, name="cmspage_add"),
    path('cmspage/edit/<int:pk>', cmspage.edit, name="cmspage_edit"),

    path('cmspage/list/<int:pk>', cmspage.sublist, name="cmspage_sublist"),
    path('cmspage/add2', cmspage.add2, name="cmspage_add2"),
    path('cmspage/add2/<str:parent>', cmspage.add2, name="cmspage_add2"),
    path('cmspage/edit2/<int:parent>/<str:pk>', cmspage.edit2, name="cmspage_edit2"),
    path('cmspage/change-status', cmspage.operations, name="cmspage_operation"),
    path('cmspage/list/change-status', cmspage.operations, name="cmspage_operation"),

    # teacher
    path('teacher/list', teacher.list, name="teacher"),
    path('teacher/add/', teacher.add, name="teacher_add"),
    path('teacher/edit/<int:pk>', teacher.edit, name="teacher_edit"),
    path('teacher/change-status', teacher.operations, name="teacher_operation"),

    # subject
    path('subject/list', subject.list, name="subject"),
    path('subject/add/', subject.add, name="subject_add"),
    path('subject/edit/<int:pk>', subject.edit, name="subject_edit"),
    path('subject/change-status', subject.operations, name="subject_operation"),
    
    # classes
    path('classes/list', classes.list, name="classes"),
    path('classes/add/', classes.add, name="classes_add"),
    path('classes/edit/<int:pk>', classes.edit, name="classes_edit"),
    path('classes/change-status', classes.operations, name="classes_operation"),

    path('classes/timetable/day/<int:pk>', classes.timetable_day, name="timetable_day"),
    path('classes/timetable/day/<int:pk>/<str:day>', classes.timetable_period, name="timetable_day"),
    path('classes/timetable/day/', classes.timetable_period_add_f, name="timetable_period_add"),
    path('classes/timetable/day/<int:pk>/<str:day>/add', classes.timetable_period_add_f, name="timetable_period_add2"),
    path('classes/timetable/day/<int:pk>/<str:day>/edit/<int:p2id>', classes.timetable_period_edit, name="timetable_period_edit"),
    
    # timetable
    path('timetable/list', timetable.list, name="timetable"),
    path('timetable/add/', timetable.add, name="timetable_add"),
    path('timetable/edit/<int:pk>', timetable.edit, name="timetable_edit"),
    path('timetable/change-status', timetable.operations, name="timetable_operation"),
    
    
]
