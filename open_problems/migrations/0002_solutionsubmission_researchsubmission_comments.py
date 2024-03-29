# Generated by Django 4.2.2 on 2023-07-11 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SolutionSubmission",
            fields=[
                ("submission_id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("full_text", models.TextField(null=True)),
                ("references", models.TextField(blank=True, max_length=200, null=True)),
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
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="open_problems.solutionsubmission",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.openproblems",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ResearchSubmission",
            fields=[
                ("submission_id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("full_text", models.TextField(null=True)),
                ("references", models.TextField(blank=True, max_length=200, null=True)),
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
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="open_problems.researchsubmission",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.openproblems",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Comments",
            fields=[
                ("comment_id", models.AutoField(primary_key=True, serialize=False)),
                ("full_text", models.TextField()),
                (
                    "parent",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.comments",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.openproblems",
                    ),
                ),
            ],
        ),
    ]
