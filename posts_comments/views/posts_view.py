import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import serializers
from rest_framework.response import Response

from utils.Pagination import Pagination
from ..models import Solution
from references.models import Reference
from ..serializers.submissions_serializer import (
    SolutionSerializer,
)
from references.serializers import ReferenceSerializer
from references.service import ReferenceService


# base url  /api/posts


# Create your views here.
class ListPosts(ListCreateAPIView):
    # List all posts or all posts for given open problem id.
    serializer_class = SolutionSerializer
    pagination_class = Pagination

    def get_queryset(self):
        open_problem_id = self.kwargs.get("id")  # Extract id from url
        queryset = Solution.objects.all()
        if open_problem_id:
            queryset = queryset.filter(open_problem=open_problem_id, is_active=True)
        return queryset


class PostDetail(RetrieveUpdateDestroyAPIView):
    # Retrieve, Update and Destroy single post
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class SubmitPost(CreateAPIView):
    serializer_class = SolutionSerializer

    def perform_create(self, serializer):
        references_data = self.request.data.get("references", [])
        try:
            serializer.save()
            post = serializer.instance
            for reference in references_data:
                reference_instance = Reference.objects.filter(
                    title=reference.title, year=reference.year
                ).first()
                if reference_instance:
                    post.references.add(reference_instance)
                else:
                    reference_service = ReferenceService(reference_data=reference)
                    new_reference_data = reference_service.create_reference()
                    reference_serializer = ReferenceSerializer(new_reference_data)
                    reference_serializer.is_valid(raise_exception=True)
                    reference_instance = reference_serializer.save()
                post.references.add(reference_instance)

        except serializers.ValidationError as e:
            raise serializers.ValidationError(detail=e.detail)
