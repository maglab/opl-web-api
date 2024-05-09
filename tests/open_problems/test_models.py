import pytest
from rest_framework.exceptions import ValidationError


class TestSubmitProblemModel:
    @pytest.mark.django_db
    def test_validation_email_required(self, create_submitted_problem):
        # Case where email is empty and notify_user is True
        submitted_problem = create_submitted_problem(email="", notify_user=True)
        with pytest.raises(ValidationError) as e:
            submitted_problem.full_clean()

    @pytest.mark.django_db
    def test_validation_email_not_required(self, create_submitted_problem):
        # Case where email is not empty and notify_user is True
        submitted_problem = create_submitted_problem(
            email="test@example.com", notify_user=True
        )
        # No exception should be raised
        submitted_problem.full_clean()
