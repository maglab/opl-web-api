# Generated by Django 5.0.3 on 2024-03-15 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0042_remove_relatedproblem_qr_id_and_more"),
        ("posts_comments", "0029_rename_post_solution"),
        ("references", "0006_rename_author_id_author_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="solution",
            name="submitted_references",
        ),
        migrations.AddField(
            model_name="solution",
            name="references",
            field=models.ManyToManyField(
                blank=True, null=True, to="references.reference"
            ),
        ),
        migrations.CreateModel(
            name="Discussion",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("full_text", models.TextField(null=True)),
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                ("affiliation", models.CharField(blank=True, max_length=50, null=True)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="open_problems.contact",
                    ),
                ),
                (
                    "open_problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.openproblem",
                    ),
                ),
                (
                    "references",
                    models.ManyToManyField(
                        blank=True, null=True, to="references.reference"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SolutionLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("liked_at", models.DateTimeField(auto_now_add=True)),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.contact",
                    ),
                ),
                (
                    "solution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="posts_comments.solution",
                    ),
                ),
            ],
            options={
                "unique_together": {("contact", "solution")},
            },
        ),
    ]