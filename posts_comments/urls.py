from django.urls import path

from posts_comments.views.comment_view import post_comment, ListComments, CommentDetail
from posts_comments.views.posts_view import (
    ListPosts,
    PostDetail,
)
from posts_comments.views.verify_references_view import (
    verify_reference,
    verify_references,
)

# url /api/posts/
urlpatterns = [
    path("all", ListPosts.as_view()),
    path("<int:id>/", ListPosts.as_view(), name="list-submissions-by-open-problem"),
    # path("<int:id>/submit", SubmitPost.as_view()),
    path("get/<int:id>", PostDetail.as_view()),
    path("get/<int:id>/comments", ListComments.as_view()),
    path("get/<int:post_id>/<int:comment_id>", CommentDetail.as_view()),
    path("post/<int:post_id>/comment/submit", post_comment),
    path("verify-reference", verify_reference),
    path("verify-references", verify_references),
]
