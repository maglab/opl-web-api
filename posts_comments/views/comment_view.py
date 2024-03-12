from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from posts_comments.models.Post import Post
from posts_comments.models.comments import Comment
from posts_comments.serializers.comments_serializer import CommentsSerializer


class ListComments:
    ...

# Get comment for a particular post submission, only root comments, only active comments.
@api_view(["GET"])
def get_comments(request, id):
    submission = Post.objects.get(submission_id=id)  # Check if submission exists.
    if submission:
        comments = Comment.objects.filter(submission_id=id, parent=None, is_active=True)
        serializer = CommentsSerializer(comments, many=True)
        if comments:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Get particular comment and its children, only active.
@api_view(["GET"])
def get_single_comment(request, id):
    comment = Comment.objects.get(
        comment_id=id, is_active=True
    )  # Check is comment exists
    if comment:
        serializer = CommentsSerializer(comment)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def post_comment(request, post_id):
    try:
        submission = Post.objects.get(submission_id=post_id)
    except Post.DoesNotExist:
        return Response(
            {"error": "Submission not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = CommentsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(submission=submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
