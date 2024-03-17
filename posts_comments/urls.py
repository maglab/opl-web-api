from django.urls import path

from posts_comments.views.comment_view import post_comment, ListComments, CommentDetail
from posts_comments.views.posts_view import (
    ListCreateSolution,
    ListCreateDiscussion,
    PostDetail,
)
from posts_comments.views.verify_references_view import (
    verify_reference,
    verify_references,
)

# url /api/posts/
urlpatterns = [
    path(
        "solutions/<int:id>",
        ListCreateSolution.as_view(),
    ),
    path(
        "discussions/<int:id>",
        ListCreateDiscussion.as_view(),
    ),
    path("get/<int:id>", PostDetail.as_view()),
    path("get/<int:id>/comments", ListComments.as_view()),
    path("get/<int:post_id>/<int:comment_id>", CommentDetail.as_view()),
    path("post/<int:post_id>/comments/submit", post_comment),
    path("verify-reference", verify_reference),  # Will delete later
    path("verify-references", verify_references),  # Will delete later
]
