from django.db import models

from posts_comments.models.Post import Post


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    submission = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True, related_name="children"
    )
    full_text = models.TextField(blank=False, null=False)
    alias = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.comment_id}:{self.full_text}"
