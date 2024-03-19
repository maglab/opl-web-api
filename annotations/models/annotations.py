from django.db import models


class Annotation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        abstract = True


class AnnotationsProblems(models.Model):
    annotation = models.AutoField(primary_key=True)
    open_problem = models.ForeignKey(
        "open_problems.OpenProblem", on_delete=models.DO_NOTHING
    )

    class Meta:
        abstract = True
