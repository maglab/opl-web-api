from django.urls import path
from .views import convert_reference

urlpatterns = [path("convert", convert_reference)]
