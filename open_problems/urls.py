from django.urls import path

from .views.open_problems_views import RetrieveProblems, RetrieveSingleProblem
from .views.references_views import get_references
from .views.submitted_problems_views import SubmitOpenProblem
from .views.utils import test_view
from .views.utils import verify_token

urlpatterns = [
    path(
        "", RetrieveProblems.as_view()
    ),  # From here we build the parameters after the sorting eg "latest?subject=1"
    # Single problem
    path("<int:id>", RetrieveSingleProblem.as_view()),
    # User submitted problem view
    path("submit", SubmitOpenProblem.as_view()),
    # Verify token for recaptcha
    path("verify-token", verify_token),
    # Get references for a problem
    path("<int:id>/references", get_references),
    path("test-auth", test_view),
]
