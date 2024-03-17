from django.db import models
from references.models import Reference
from open_problems.models import OpenProblem, Contact


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    full_text = models.TextField(null=True)
    open_problem = models.ForeignKey(OpenProblem, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    affiliation = models.CharField(max_length=50, null=True, blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    references = models.ManyToManyField(Reference, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Solution(Post):
    # objects line here since it isn't automatically set for some reason
    objects = models.Manager()


class Discussion(Post): ...


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Solution, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, blank=True, related_name="children"
    )
    full_text = models.TextField(blank=False, null=False)
    alias = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}:{self.full_text}"
