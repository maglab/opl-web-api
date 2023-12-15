from django.db import models

from .annotations import AnnotationsProblems


class Species(models.Model):
    species_id = models.AutoField(primary_key=True)
    genus = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.genus} {self.species}"

    class Meta:
        db_table = "Species"


class SpeciesProblem(AnnotationsProblems):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.species}: {self.open_problem.open_problem_id} "

    class Meta:
        db_table_comment = "Relation table for each species and open problem"
