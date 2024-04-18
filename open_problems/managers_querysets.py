from django.db import models
from django.db.models import OuterRef, Exists, Q


class OpenProblemManager(models.Manager):
    def root(self):
        return self.filter(parent=None)

    def latest(self):
        return self.order_by("problem_id")

    def top(self):
        return self.order_by("-descendants_count")

    def answered(self):
        return self.annotate(
            has_solution=Exists(self.solution_set.filter(open_problem=OuterRef("pk"))),
            has_discussion=Exists(
                self.discussion_set.filter(open_problem=OuterRef("pk"))
            ),
        ).filter(Q(has_solution=True) | Q(has_discussion=True))
