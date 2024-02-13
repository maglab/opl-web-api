import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response

from open_problems.models.open_problems import OpenProblem
from references.models import Reference
from utils.Pagination import Pagination
from utils.create_reference import create_reference, create_journal_instance
from ..models.Post import Post, PostReferences
from ..serializers.submissions_serializer import (
    PostReferencesSerializer,
    PostSerializer,
)


# base url  /api/posts

# Create your views here.
class ListPosts(ListCreateAPIView):
    # List all posts or all posts for given open problem id.
    serializer_class = PostSerializer
    pagination_class = Pagination

    def get_queryset(self):
        open_problem_id = self.kwargs.get("id")  # Extract id from url
        queryset = Post.objects.all()
        if open_problem_id:
            queryset = queryset.filter(open_problem=open_problem_id, is_active=True)
        return queryset


class PostDetail(RetrieveUpdateDestroyAPIView):
    # Retrieve, Update and Destroy single post
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# @api_view(["POST"])
# def submit_post(request, id):  # Submit post for an open problem.
#     if request.method == "POST":
#         serializer = PostSerializer(data=request.data)
#         open_problem = OpenProblems.objects.filter(problem_id=id).exists()
#
#         if serializer.is_valid(raise_exception=True) & open_problem:
#             serializer.save()
#             # After saving parse the submitted serializer
#             reference_data = request.data["submitted_references"]
#             if reference_data:
#                 submission_id = serializer["submission_id"].value
#                 reference_list = parse_submitted_references(
#                     reference_data, submission_id
#                 )
#                 submitted_references_serializer = SubmittedReferencesSerializer(
#                     data=reference_list, many=True
#                 )
#                 if submitted_references_serializer.is_valid():
#                     submitted_references_serializer.save()
#                 else:
#                     print(submitted_references_serializer.errors)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)


class SubmitPost(CreateAPIView):
    serializer_class = PostSerializer

    @staticmethod
    def collect_references(references: list) -> list:
        """
        Iterate through dictionary of DOIs and PMIDs and create an array of Reference model instances from them.

        Args:
            references (list): List of dictionaries containing reference information
        Returns:
            List of Reference model instances
        """
        reference_instances = []
        for reference in references:
            ref_type = reference["type"]
            ref_value = reference["ref"]
            reference_dictionary = create_reference(ref_type=ref_type, value=ref_value)
            # Check for existing entry
            if reference_dictionary:
                reference_exists = Reference.objects.filter(
                    title=reference_dictionary["title"]
                ).first()
                if reference_exists:
                    reference = reference_exists
                else:
                    reference_data = create_journal_instance(
                        reference_dict=reference_dictionary
                    )

                    reference = Reference.objects.create(
                        **reference_data,
                    )
                reference_instances.append(reference)
        return reference_instances

    def create(self, request, *args, **kwargs):
        open_problem_id = self.kwargs.get("id")
        try:
            open_problem = OpenProblem.objects.get(problem_id=open_problem_id)
        except OpenProblem.DoesNotExist:
            return Response(
                {"detail": "Open problem not found."}, status=status.HTTP_404_NOT_FOUND
            )
        # Create the Post instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        # Then get the references instances, save and link them to the post in the intermediary table
        # references submitted as stringified JSON
        submitted_references = json.loads(request.data["submitted_references"])
        flattened_list = [value for value in submitted_references.values()]
        reference_instances = self.collect_references(flattened_list)
        for reference in reference_instances:
            saved_reference = reference.save()
            PostReferences.objects.create(post_id=post, reference_id=saved_reference)


@api_view(["GET"])  # This will be moved to a References module
def get_references(request, id):
    """Get references for a particular solution submission"""
    references = PostReferences.objects.filter(submission_id=id)
    if references:
        serializer = PostReferencesSerializer(references, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])  # Retrieve the number of posts for a given open problem
def get_posts_counts(request, id):
    # This might be redundant because the pagination class returns the counts
    submissions_for_open_problem = Post.objects.filter(
        open_problem=id, is_active=True
    ).count()
    return Response({"post_counts": submissions_for_open_problem})
