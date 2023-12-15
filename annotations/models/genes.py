from django.db import models

from .annotations import AnnotationsProblems
from .species import Species


class Gene(models.Model):
    id = models.AutoField(primary_key=True)
    gene_name = models.CharField(max_length=50, unique=True)
    gene_symbol = models.CharField(max_length=10, unique=True)
    species = models.ForeignKey(
        Species, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return f"{self.gene_symbol}: {self.gene_name}"

    class Meta:
        db_table = "Genes"
        db_table_comment = "Table for all genes"


class GeneProblem(AnnotationsProblems):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.gene}: {self.open_problem_id} "

    class Meta:
        db_table_comment = "Relation table for each gene and open problem"
