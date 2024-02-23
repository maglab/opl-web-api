from django.db import models

from .open_problems import OpenProblems


class Report(models.Model):
    DUPLICATE = "duplicate"
    OTHER = "other"
    REASON_CHOICES = [(DUPLICATE, "Duplicate"), (OTHER, "Other")]
    id = models.AutoField(primary_key=True)
    open_problem = models.ForeignKey(OpenProblems, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    information = models.TextField(max_length=500, blank=True)
    duplicate = models.ForeignKey(
        OpenProblems,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="duplicate_problem",
    )

    def __str__(self):
        return f"{self.open_problem.title}"
