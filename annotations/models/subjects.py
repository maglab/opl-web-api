from django.db import models

from open_problems.models import Reference
from .annotations import AnnotationsProblems


# Theory models to attach for a particular open problem.
class Subject(models.Model):
    id = models.AutoField(db_column="", primary_key=True)  # Field name made lowercase.
    title = models.CharField(
        db_column="title", max_length=40, blank=True, null=True
    )  # Field name made lowercase.
    description = models.TextField(
        db_column="description", blank=True, null=True
    )  # Field name made lowercase.
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="children",
        blank=True,
    )

    # end of edit by Hamid
    class Meta:
        db_table = "Subject"
        db_table_comment = (
            "A subject annotation describing the topic of the open problem"
        )

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"


class SubjectProblem(AnnotationsProblems):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.subject}: {self.open_problem} "

    class Meta:
        db_table_comment = "Relation table for each subject and open problem"


class SubjectReference(models.Model):
    # Field name made lowercase. The composite primary key (Ref_id, Theory_id) found, that is not supported.
    # The first column is selected.
    ref = models.OneToOneField(
        Reference, models.DO_NOTHING, db_column="reference_id", primary_key=True
    )
    # Field name made lowercase.
    subject = models.ForeignKey(
        Subject, models.DO_NOTHING, db_column="subject_id", null=True
    )

    class Meta:
        db_table = "subject_reference"
        unique_together = ("ref", "subject")
