from django.urls import path, include
from rest_framework import routers
from backend import api_views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
