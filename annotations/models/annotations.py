from django.db import models

from open_problems.models.open_problems import OpenProblems


# Abstract table that will link a problem to all annotations
class AnnotationsProblems(models.Model):

    annotation_id = models.AutoField(primary_key=True)
    open_problem = models.ForeignKey(OpenProblems, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
