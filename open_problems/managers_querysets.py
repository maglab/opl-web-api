from django.db import models
from django.apps import apps
from django.db.models import OuterRef, Exists, Q


class OpenProblemQueryset(models.QuerySet):
    def root(self):
        return self.filter(parent=None)

    def latest(self):
        return self.order_by("-problem_id")

    def top(self):
        return self.order_by("-descendants_count")

    def answered(self):
        Solution = apps.get_model("posts_comments", "Solution")
        return (
            self.get_queryset()
            .annotate(
                has_solution=Exists(
                    Solution.objects.filter(open_problem=OuterRef("pk"))
                ),
            )
            .filter(has_solution=True)
        ).order_by("-problem_id")


class OpenProblemManager(models.Manager):
    def get_queryset(self):
        return OpenProblemQueryset(self.model, using=self._db)

    def root(self):
        return self.get_queryset().root()

    def latest(self):
        return self.get_queryset().latest()

    def top(self):
        return self.get_queryset().top()

    def answered(self):
        return self.get_queryset().answered()
