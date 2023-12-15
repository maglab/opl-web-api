from django.db import models

from .annotations import AnnotationsProblems
from .species import Species


class Proteins(models.Model):
    protein_id = models.AutoField(primary_key=True)
    protein_name = models.CharField(max_length=50, unique=True)
    species = models.ForeignKey(Species, blank=True, null=True)

    class Meta:
        db_table = "Proteins"
        db_comment = "Table containg all submitted proteins"


class ProteinsProblems(AnnotationsProblems):
    protein = models.ForeignKey(Proteins, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.protein.protein_id}: {self.open_problem.open_problem_id} "

    class Meta:
        db_table_comment = "Relation table for each protein and open problem"
