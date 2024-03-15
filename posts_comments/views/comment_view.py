from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts_comments.models import Solution
from posts_comments.models import Comment
from posts_comments.serializers.comments_serializer import CommentSerializer
from utils.Pagination import Pagination


class ListComments(ListCreateAPIView):
    queryset = Comment.objects.filter(is_active=True)
    serializer_class = CommentSerializer
    pagination_class = Pagination

    def get_queryset(self):
        post_id = self.kwargs.get("id")
        queryset = Comment.objects.all()
        if post_id:
            queryset = queryset.filter(post=post_id, is_active=True)
        return queryset

    def post(self, request, *args, **kwargs): ...


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(["POST"])
def post_comment(request, post_id):
    ## Keep this one for now until i figure out how we handle the references.
    try:
        submission = Solution.objects.get(submission_id=post_id)
    except Solution.DoesNotExist:
        return Response(
            {"error": "Submission not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(submission=submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
