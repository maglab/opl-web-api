from django.db import models
from django.apps import apps
from django.db.models import OuterRef, Exists, Q


class OpenProblemQueryset(models.QuerySet):

    def alphabetical(self):
        return self.order_by("title")

    def latest(self):
        return self.filter(is_active=True).order_by("-problem_id")

    def answered(self):
        solution = apps.get_model("posts_comments", "Solution")
        return (
            self.annotate(
                has_solution=Exists(
                    solution.objects.filter(open_problem=OuterRef("pk")).filter(
                        is_active=True
                    )
                ),
            )
            .filter(has_solution=True)
            .filter(is_active=True)
            .order_by("-problem_id")
        )


class OpenProblemManager(models.Manager):
    def get_queryset(self):
        return OpenProblemQueryset(self.model, using=self._db)

    def alphabetical(self):
        return self.get_queryset().alphabetical()

    def latest(self):
        return self.get_queryset().latest()

    def answered(self):
        return self.get_queryset().answered()
