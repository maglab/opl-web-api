from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class Journal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table_comment = "Contains the ids and names of article journals"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"


class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=150
    )  # max_length changed from 100 to 150 by Hamid
    citation = models.TextField()
    doi = models.CharField(max_length=100, null=True, blank=True)
    relevance = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.CharField(max_length=4)
    isbn = models.IntegerField(null=True, blank=True)
    journal_id = models.ForeignKey(
        Journal, on_delete=models.SET_NULL, null=True, blank=True
    )
    authors = models.ManyToManyField(Author, blank=True)

    class Meta:
        db_table_comment = "Contains all reference information"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
