from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, serialize=True, default=None)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        related_name="children",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name_plural = "Categories"

    def get_sorted_open_problems(self):
        return self.open_problems.all().order_by("title")

    def __str__(self):
        return self.title
