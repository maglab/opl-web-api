from django.db import models

from open_problems.models.contacts_users import Contact
from open_problems.models.open_problems import OpenProblems
from open_problems.models.references import Reference


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    full_text = models.TextField(null=True)
    open_problem = models.ForeignKey(OpenProblems, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    affiliation = models.CharField(max_length=50, null=True, blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    submitted_references = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(
        default=False
    )  # When submission is reviewed we set this to true to display on the web page.
    # Are contacts required to submit ??

    # objects line here since it isn't automatically set for some reason
    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.id}: {self.full_text}"


# Models for references
class PostReferences(models.Model):  # Model for reviewed references
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    reference_id = models.ForeignKey(Reference, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Post and Linked References"


class SubmittedReferences(models.Model):  # Model for submitted references
    """References that are submitted from a user with their solution submission"""

    reference_id = models.AutoField(primary_key=True)
    submission_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=15)
    ref = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Submitted Reference"

    def __str__(self) -> str:
        return f"{self.type}: {self.ref} for {self.submission_id.full_text}"
