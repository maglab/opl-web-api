from django.db import models


# Create your models here.
class AbstractReport(models.Model):
    CHOICE_MAPPING = []
    id = models.AutoField()
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


class OpenProblemReport(AbstractReport):
    DUPLICATE = 1
    CONTENT = 2
    OTHER = 3
    CHOICE_MAPPING = [(DUPLICATE, "duplicate"), (CONTENT, "content"), (OTHER, "other")]
