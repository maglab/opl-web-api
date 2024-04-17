from django.urls import path

from .views import (
    RetrieveProblems,
    RetrieveSingleProblem,
    ListReferencesView,
    SubmitOpenProblemView,
)


urlpatterns = [
    path("", RetrieveProblems.as_view()),
    # Single problem
    path("<int:id>", RetrieveSingleProblem.as_view()),
    # User submitted problem view
    path("submit", SubmitOpenProblemView.as_view()),
    # Get references for a problem
    path("<int:pk>/references", ListReferencesView.as_view()),
]
