from django.db import models

from references.models import Reference
from .annotations import AnnotationsProblems


class Tag(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    title = models.CharField(
        max_length=40, blank=True, null=True
    )  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="children",
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"


class TagProblem(AnnotationsProblems):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.tag}: {self.open_problem} "
