from django.db import models
from open_problems.models import Contact
from .post_comment import Solution


class Like(models.Model):
    contact = models.ForeignKey(
        Contact, null=True, blank=True, on_delete=models.CASCADE
    )  # Temporary as we want users
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# Intermediary tables for now
class SolutionLike(Like):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["contact", "solution"]  # One like per solution per user
