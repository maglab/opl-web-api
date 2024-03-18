from django.db import models

from .annotations import AnnotationsProblems


class Compound(models.Model):
    id = models.AutoField(primary_key=True)
    compound_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table_comment = "Table for all compounds"

    def __str__(self):
        return f"{self.id: {self.compound_name}}"


class CompoundProblem(AnnotationsProblems):
    compound = models.ForeignKey(Compound, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.compound.compound_name} : {self.open_problem}"
