# Generated by Django 4.2.2 on 2023-07-12 11:27

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "open_problems",
            "0003_remove_researchsubmission_contact_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("submission_id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("type", models.CharField()),
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
                    "open_problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="open_problems.openproblems",
                    ),
                ),
            ],
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
