from django.test import TestCase
from open_problems.models.open_problems import OpenProblems
from open_problems.models.contacts_users import Contact


class OpenProblemsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample contact instance for the ForeignKey relationship
        cls.contact = Contact.objects.create(first_name="John", last_name="Doe", email="test@test.com")

        # Create a sample OpenProblems instance
        cls.problem = OpenProblems.objects.create(
            title='Test Problem',
            description='Test description',
            contact=cls.contact,
            parent_problem=None,
            is_active=True
        )

    def test_problem_str_representation(self):
        self.assertEqual(
            str(self.problem),
            f'{self.problem.problem_id}: {self.problem.title}'
        )

    # Add more tests for specific model behaviors, relationships, etc.
