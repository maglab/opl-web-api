from django.db import models
from references.models import Reference


class JobInformation(models.Model):
    info_id = models.AutoField(primary_key=True)
    info_title = models.CharField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Organisation(JobInformation):
    def __str__(self) -> str:
        return f"{self.info_title}"


class JobField(JobInformation):
    def __str__(self) -> str:
        return f"{self.info_title}"


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    job_field = models.ForeignKey(
        JobField, on_delete=models.SET_NULL, null=True, blank=True
    )
    organisation = models.ForeignKey(
        Organisation, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table_comment = "This table contains the contact details of the person who submitted the question"

    def __str__(self):
        return f"{self.first_name} {self.last_name} : {self.email}"


class OpenProblemAbstract(models.Model):
    problem_id = models.AutoField(primary_key=True, serialize=True, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    contact = models.ForeignKey(
        Contact, null=True, on_delete=models.SET_NULL, blank=True
    )  # Non authenticated
    references = models.ManyToManyField(Reference, blank=True)

    class Meta:
        abstract = True


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
    # tags = models.ManyToManyField(Tag, through=TagProblem)

    def get_descendants(self):
        count = 0
        children = OpenProblem.objects.filter(parent_problem=self)

        for child in children:
            count += 1  # Count the immediate child
            count += child.get_descendants()

        return count

    def get_ordered_children_descending(self):
        children = OpenProblem.objects.filter(parent_problem=self).order_by(
            "-descendants_count"
        )
        return children

    @classmethod
    def update_descendants_count(cls):
        all_instances = cls.objects.all()
        for instance in all_instances:
            instance.descendants_count = instance.get_descendants()
            instance.save()

    class Meta:
        db_table = "open_problem"
        db_table_comment = "These are the current open problems that we have accepted from the submitted questions"
        verbose_name = "Open Problem"

    def __str__(self):
        return f"{self.problem_id}: {self.title}"


class SubmittedOpenProblem(OpenProblemAbstract):
    parent_problem = models.ForeignKey(
        OpenProblem, null=True, blank=True, on_delete=models.SET_NULL
    )
    species = models.CharField(max_length=50, null=True, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    job_field = models.CharField(max_length=100, blank=True)
    organisation = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.title} : {self.email}"

    class Meta:
        db_table = "submitted_open_problem"
        db_table_comment = (
            "These are the submitted questions from users that will undergo review"
        )
        verbose_name = "Submitted Problem"
