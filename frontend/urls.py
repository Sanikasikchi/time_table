from django.urls import path
from django.conf.urls import include

from frontend.baseappf import views as baseapp
from frontend.cms import views as cms

# from frontend.seller import views as seller
# from frontend.seller_product_listing import views as seller_product_listing
# from frontend.product_listing import views as product_listing

urlpatterns = [
    path("login", baseapp.DjangoLogin, name="login"),
    path("logout", baseapp.logoutUser, name="logout"),
    # path("register/", baseapp.registerPage, name="register"),
    # path("session", baseapp.sessiontest, name="session"),
    # path("<slug:the_slug>/", cms.slug, name="cms"),
    # path('<slug:slug>/', product_listing.slug, name='cat_page'),
    path("home", baseapp.index, name="index"),
    path("", baseapp.index, name="index"),
    path("teacher-entry/", baseapp.teacherEntry, name="TeacherEntry"),
    path("manage-classes", baseapp.manageClasses, name="ManageClasses"),

    path("classes/conduct/<slug:tt_id>", baseapp.conductClasses, name="ManageClasses"),
    path("classes/cancel/<slug:tt_id>", baseapp.cancelClasses, name="cancelClasses"),

    path("classes-history", baseapp.historyClasses, name="historyClasses"),

]
