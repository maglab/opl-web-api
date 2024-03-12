from django.urls import path

from posts_comments.views.comment_view import (
    get_comments,
    get_single_comment,
    post_comment,
)
from posts_comments.views.posts_view import (
    get_posts_counts,
    get_references,
    ListPosts,
    PostDetail,
    SubmitPost,
)
from posts_comments.views.verify_references_view import (
    verify_reference,
    verify_references,
)

# url /api/posts/
urlpatterns = [
    path("all", ListPosts.as_view()),
    path("<int:id>/", ListPosts.as_view(), name="list-submissions-by-open-problem"),
    path("<int:id>/counts", get_posts_counts),
    path("<int:id>/submit", SubmitPost.as_view()),
    path("get/<int:id>", PostDetail.as_view()),
    path("get/<int:id>/comments", get_comments),
    path("get/<int:post_id>/<int:comment_id>", get_single_comment),
    path("post/<int:post_id>/comment/submit", post_comment),
    path("verify-reference", verify_reference),
    path("verify-references", verify_references),
    path(
        "get/<int:id>/submission/reference", get_references
    ),  # get references for a particular solution submision
]
