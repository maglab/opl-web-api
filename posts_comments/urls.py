from django.urls import path

from posts_comments.views.comment_view import (
    ListCreateComments,
    CommentDetail,
)
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
    path("<str:post_type>/<int:id>", PostDetail.as_view()),
    path(
        "<int:id>/<str:post_type>/comments", ListCreateComments.as_view()
    ),  # Post and List
    path("<str:post_type>/comments/<int:id>", CommentDetail.as_view()),
    path("verify-reference", verify_reference),  # Will delete later
    path("verify-references", verify_references),  # Will delete later
]
