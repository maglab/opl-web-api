from django.db import models
from rest_framework.exceptions import ValidationError

from references.models import Reference
from annotations.models import Tag, Species, Compound, Gene
from .managers_querysets import OpenProblemManager
from users.models import Contact
from categories.models import Category


class OpenProblemAbstract(models.Model):
    problem_id = models.AutoField(primary_key=True, serialize=True, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    contact = models.ForeignKey(
        Contact, null=True, on_delete=models.SET_NULL, blank=True
    )  # Non authenticated
    references = models.ManyToManyField(Reference, blank=True)
    tags = models.ManyToManyField(to=Tag, blank=True)
    species = models.ManyToManyField(to=Species, blank=True)
    compounds = models.ManyToManyField(to=Compound, blank=True)
    genes = models.ManyToManyField(to=Gene, blank=True)

    # custom manager here
    objects = OpenProblemManager()

    class Meta:
        abstract = True
        ordering = ["problem_id"]

    def list_children(self):
        return ", ".join([str(child) for child in self.children.all()])


class OpenProblem(OpenProblemAbstract):
    parent_problem = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    descendants_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    categories = models.ManyToManyField(to=Category, blank=True)

    @classmethod
    def update_descendants_count(cls):
        all_instances = cls.objects.all()
        for instance in all_instances:
            instance.descendants_count = instance.get_descendants()
            instance.save()

    class Meta:
        db_table_comment = "These are the current open problems that we have accepted from the submitted questions"
        verbose_name = "Open Problem"

    def __str__(self):
        return f"{self.problem_id}: {self.title}"


class SubmittedOpenProblem(OpenProblemAbstract):
    parent_problem = models.ForeignKey(
        OpenProblem, null=True, blank=True, on_delete=models.SET_NULL
    )
    references = models.ManyToManyField(Reference, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    job_field = models.CharField(max_length=100, blank=True)
    organisation = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(to=Tag, blank=True)
    species = models.ManyToManyField(to=Species, blank=True)
    compounds = models.ManyToManyField(to=Compound, blank=True)
    genes = models.ManyToManyField(to=Gene, blank=True)
    notify_user = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} : {self.email}"

    def clean(self):
        if not self.email and self.notify_user:
            raise ValidationError("Cannot notify contact without an email")

    class Meta:
        verbose_name = "Submitted Problem"
