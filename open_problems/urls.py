from django.urls import path

from .views.open_problems_views import RetrieveProblems, RetrieveSingleProblem
from .views.references_views import ListReferencesView
from .views.submitted_problems_views import SubmitOpenProblemView
from .views.utils import test_view
from .views.utils import verify_token

urlpatterns = [
    path("", RetrieveProblems.as_view()),
    # Single problem
    path("<int:id>", RetrieveSingleProblem.as_view()),
    # User submitted problem view
    path("submit", SubmitOpenProblemView.as_view()),
    # Verify token for recaptcha
    path("verify-token", verify_token),
    # Get references for a problem
    path("<int:pk>/references", ListReferencesView.as_view()),
    path("test-auth", test_view),
]
