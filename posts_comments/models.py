from django.db import models
from open_problems.models import OpenProblem
from users.models import UserProfile
from references.models import Reference


class Like(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    full_text = models.TextField(null=True)
    open_problem = models.ForeignKey(OpenProblem, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)  # Temporary
    last_name = models.CharField(max_length=50, null=True, blank=True)  # Temporary
    alias = models.CharField(
        max_length=100, null=True, blank=True
    )  # Temporary - will be user
    affiliation = models.CharField(max_length=50, null=True, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.created_at}"

    class Meta:
        abstract = True


class Solution(Post):
    open_problem = models.ForeignKey(
        OpenProblem, on_delete=models.CASCADE, related_name="solution"
    )


class Discussion(Post):
    open_problem = models.ForeignKey(
        OpenProblem, on_delete=models.CASCADE, related_name="discussion"
    )


class CommentSolution(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Solution, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True, related_name="children"
    )
    full_text = models.TextField(blank=False, null=False)
    alias = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}:{self.full_text}"


class CommentDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Solution, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True, related_name="children"
    )
    full_text = models.TextField(blank=False, null=False)
    alias = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}:{self.full_text}"


# Intermediary tables for now
class SolutionLike(Like):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "solution"]  # One like per solution per user
