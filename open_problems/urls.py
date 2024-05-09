from django.urls import path

from .views import (
    ListProblemsView,
    RetrieveProblemView,
    SubmitOpenProblemView,
)

urlpatterns = [
    path("", ListProblemsView.as_view(), name="list"),
    # Single problem
    path("<int:pk>", RetrieveProblemView.as_view(), name="retrieve"),
    # User submitted problem view
    path("submit", SubmitOpenProblemView.as_view(), name="submit"),
    # Get references for a problem
]
