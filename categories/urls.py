from django.urls import path

from .views import ListCategoriesView

urlpatterns = [path("", ListCategoriesView.as_view())]
