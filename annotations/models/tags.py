from django.db import models

from references.models import Reference


class Tag(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    title = models.CharField(
        max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
