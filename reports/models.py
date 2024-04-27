from django.db import models
from users.models import Contact


# Create your models here.
class AbstractReport(models.Model):
    CHOICE_MAPPING = []
    id = models.AutoField(primary_key=True)
    subject = models.IntegerField(choices=CHOICE_MAPPING)
    detail = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class GeneralReport(AbstractReport):
    SUGGESTION = 1
    BUG = 2
    COMMENT = 3
    OTHER = 4
    CHOICE_MAPPING = [
        (SUGGESTION, "suggestion"),
        (BUG, "bug"),
        (COMMENT, "comment"),
        (OTHER, "other"),
    ]
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True)
    organisation = models.CharField(max_length=100, blank=True)


class OpenProblemReport(AbstractReport):
    DUPLICATE = 1
    CONTENT = 2
    OTHER = 3
    CHOICE_MAPPING = [(DUPLICATE, "duplicate"), (CONTENT, "content"), (OTHER, "other")]
