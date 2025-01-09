from django.urls import path

from .views import ListCategoriesView, RetrieveCategoryView

urlpatterns = [
    path("", ListCategoriesView.as_view()),
    path("<int:pk>", RetrieveCategoryView.as_view()),
]
