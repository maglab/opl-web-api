from django.test import TestCase
from open_problems.models.open_problems import OpenProblems
from open_problems.models.contacts_users import Contact
from open_problems.serializers.serializers import OpenProblemsSerializer


class OPSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample User instance for the ForeignKey relationship
        cls.john_doe = Contact.objects.create(first_name = "John", last_name ="Doe", email="john_doe@test.com")
        cls.jane_doe = Contact.objects.create(first_name = "Jane", last_name="Doe", email="jane_doe@test.com")

        # Create a sample OpenProblems instance
        cls.problem = OpenProblems.objects.create(
            title='Test Problem',
            description='Test description',
            contact=cls.john_doe,
            parent_problem=None,
            is_active=True
        )
        cls.child_problem = OpenProblems.objects.create(
            title="Test child problem",
            description = "Test description ",
            contact = cls.jane_doe,
            parent_problem = cls.problem,
            is_active = True
        )

    def test_serializer_with_children(self):
        serializer = OpenProblemsSerializer(instance=self.problem)
        serialized_data = serializer.data

        self.assertEqual(serialized_data['problem_id'], self.problem.problem_id)
        self.assertEqual(serialized_data['title'], self.problem.title)
        self.assertEqual(serialized_data['description'], self.problem.description)
        self.assertEqual(serialized_data['contact'], self.problem.contact.id)  # Use self.problem.contact.id
        self.assertIsNone(serialized_data['parent_problem'])  # No parent_problem for root problem
        self.assertEqual(len(serialized_data['children']), 1)  # No children for root problem

