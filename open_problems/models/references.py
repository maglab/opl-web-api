from django.db import models


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.author_id}: {self.author_name}"


class Journal(models.Model):
    journal_id = models.AutoField(primary_key=True)
    journal_name = models.CharField(max_length=100)

    class Meta:
        db_table_comment = "Contains the ids and names of article journals"

    def __str__(self) -> str:
        return f"{self.journal_id}: {self.journal_name}"


class RefType(models.Model):
    rtype_id = models.AutoField(primary_key=True)
    rtype_class = models.CharField(max_length=50)
    class_description = models.TextField()

    class Meta:
        db_table_comment = "A cyclic table that contains all types of references, \
                the self-joini relation is to indicate whether one reference type is a subcategory of another."

    def __str__(self) -> str:
        return f"{self.rtype_id}: {self.rtype_class}:"


class Reference(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=150
    )  # max_length changed from 100 to 150 by Hamid
    citation = models.TextField()
    doi = models.CharField(max_length=100, null=True, blank=True)
    relevance = models.PositiveSmallIntegerField(null=True, blank=True)
    publish_date = models.CharField(max_length=4)
    isbn = models.IntegerField(max_length=15, null=True, blank=True)
    journal_id = models.ForeignKey(
        Journal, on_delete=models.SET_NULL, null=True, blank=True
    )
    authors = models.ManyToManyField(Author, blank=True, null=True)
    link = models.CharField(
        max_length=200, null=True, blank=True
    )  # If given source is a Link

    class Meta:
        db_table_comment = "Contains all reference information"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"
