from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts_comments.models import Comment
from posts_comments.serializers import CommentSerializer
from utils.Pagination import Pagination


class ListCreateComments(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = Pagination

    def get_queryset(self):
        post_id = self.kwargs.get("id")
        queryset = Comment.objects.all()
        if post_id:
            queryset = queryset.filter(post=post_id, is_active=True)
        return queryset


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
