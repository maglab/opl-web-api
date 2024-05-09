from django.db import models


class Compound(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    chembl_id = models.CharField(max_length=20, blank=True)
    pubchem_id = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        db_table_comment = "Table for all compounds"

    def __str__(self):
        return f"{self.id}:{self.name}"


class Species(models.Model):
    id = models.AutoField(primary_key=True)
    genus = models.CharField(max_length=50, blank=True, null=True)
    species = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    ncbi_tax_id = models.CharField(max_length=20, blank=True)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If the object is being created and full_name is not set
        if not self.pk and not self.full_name:
            self.full_name = f"{self.genus} {self.species}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.genus} {self.species}"


class Gene(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gene_symbol = models.CharField(max_length=10, unique=True)
    entrez_id = models.CharField(max_length=20, blank=True)
    species = models.ForeignKey(
        Species, blank=True, null=True, on_delete=models.SET_NULL
    )
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.gene_symbol}: {self.name}"

    class Meta:
        unique_together = (
            ("gene_symbol", "species"),
        )  # Gene symbols span across species.


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
