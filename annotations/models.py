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


class Species(models.Model):
    id = models.AutoField(primary_key=True)
    genus = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=50, null=True)

    @property
    def name(self):
        return f"{self.genus} {self.species}"

    def __str__(self):
        return f"{self.genus} {self.species}"


class SpeciesProblem(AnnotationsProblems):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.species}: {self.open_problem.title} "

    class Meta:
        db_table_comment = "Relation table for each species and open problem"


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
        db_table_comment = "Table for all genes"


class GeneProblem(AnnotationsProblems):
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.gene}: {self.open_problem.title} "


class Tag(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    title = models.CharField(
        max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
