# Generated by Django 4.2.4 on 2024-02-22 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0025_alter_openproblems_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "reason",
                    models.CharField(
                        choices=[("duplicate", "Duplicate"), ("other", "Other")],
                        max_length=50,
                    ),
                ),
                ("information", models.TextField(blank=True, max_length=500)),
                (
                    "duplicate",
                    models.ManyToManyField(
                        blank=True,
                        related_name="duplicates",
                        to="open_problems.openproblems",
                    ),
                ),
                (
                    "open_problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.openproblems",
                    ),
                ),
            ],
        ),
    ]