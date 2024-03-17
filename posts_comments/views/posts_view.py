import json

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import serializers

from utils.Pagination import Pagination
from ..models import Solution, Discussion
from ..serializers import SolutionSerializer, DiscussionSerializer
from references.service import ReferenceService


# base url  /api/posts


class PostDetail(RetrieveUpdateDestroyAPIView):
    # Retrieve, Update and Destroy single post
    def get_queryset(self):
        post_type = self.request.query_params.get("post_type")
        if post_type == "solution":
            return Solution.objects.all()
        elif post_type == "discussion":
            return Discussion.objects.all()

    def get_serializer_class(self):
        post_type = self.request.query_params.get("post_type")
        if post_type == "solution":
            return SolutionSerializer
        elif post_type == "discussion":
            return DiscussionSerializer


class ListCreateDiscussion(ListAPIView):
    serializer_class = SolutionSerializer
    pagination_class = Pagination

    def get_queryset(self):
        open_problem_id = self.kwargs.get("id")
        discussion_objects = Discussion.objects.all()
        queryset = discussion_objects.filter(
            open_problem=open_problem_id, is_active=True
        )
        return queryset

    def perform_create(self, serializer):
        references_data = self.request.data.get("references", [])
        try:
            serializer.save()
            post = serializer.instance
            for reference in references_data:
                reference_service_object = ReferenceService(reference)
                reference_instance = reference_service_object.create_reference()
                post.references.add(reference_instance)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(detail=e.detail)


class ListCreateSolution(ListCreateAPIView):
    serializer_class = SolutionSerializer
    pagination_class = Pagination

    def get_queryset(self):
        open_problem_id = self.kwargs.get("id")
        solution_objects = Solution.objects.all()
        queryset = solution_objects.filter(open_problem=open_problem_id, is_active=True)
        return queryset

    def perform_create(self, serializer):
        references_data = self.request.data.get("references", [])
        try:
            serializer.save()
            post = serializer.instance
            for reference in references_data:
                reference_service_object = ReferenceService(reference)
                reference_instance = reference_service_object.create_reference()
                post.references.add(reference_instance)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(detail=e.detail)
