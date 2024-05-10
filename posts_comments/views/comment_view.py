from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from posts_comments.models import CommentSolution, CommentDiscussion
from posts_comments.serializers import (
    CommentSolutionSerializer,
    CommentDiscussionSerializer,
)
from core.utils.Pagination import Pagination


class ListCreateComments(ListCreateAPIView):
    pagination_class = Pagination

    def get_serializer_class(self):
        post_type = self.kwargs.get("post_type")
        if post_type == "solutions":
            return CommentSolutionSerializer
        elif post_type == "discussions":
            return CommentDiscussionSerializer
        else:
            raise NotFound("Invalid post type.")

    def get_queryset(self):
        post_id = self.kwargs.get("id")
        post_type = self.kwargs.get("post_type")
        if post_type is None:
            raise NotFound("Post type is required")
        if post_id is None:
            raise NotFound("Post id is required")

        if post_type == "solutions":
            model_class = CommentSolution
        elif post_type == "discussions":
            model_class = CommentDiscussion
        else:
            raise NotFound("Invalid post type")

        try:
            queryset = model_class.objects.filter(post=post_id, is_active=True)
        except model_class.DoesNotExist:
            raise NotFound("No such resource found")

        return queryset


class CommentDetail(RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        post_type = self.kwargs.get("post_type")
        if post_type == "solutions":
            return CommentSolutionSerializer
        elif post_type == "discussions":
            return CommentDiscussionSerializer
        else:
            raise NotFound("Invalid post type.")

    def get_queryset(self):
        post_type = self.kwargs.get("post_type")
        if post_type == "solutions":
            model_class = CommentSolution.objects.all()
        elif post_type == "discussions":
            model_class = CommentDiscussion.objects.all()
        else:
            raise NotFound("Invalid post type")
        return model_class.objects.all()
