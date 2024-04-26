from django.db import models
from references.models import Reference
from annotations.models import Tag, Species, Compound, Gene
from .managers_querysets import OpenProblemManager
from users.models import Contact


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

    def __str__(self) -> str:
        return f"{self.title} : {self.email}"

    class Meta:
        db_table = "submitted_open_problem"
        db_table_comment = (
            "These are the submitted questions from users that will undergo review"
        )
        verbose_name = "Submitted Problem"
