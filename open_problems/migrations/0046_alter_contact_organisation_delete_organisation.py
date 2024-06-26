# Generated by Django 5.0.3 on 2024-04-17 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0045_remove_submittedopenproblem_tags_and_more"),
        ("users", "0002_organisation"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name="Organisation",
                ),
                migrations.AlterField(
                    model_name="contact",
                    name="organisation",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.organisation",
                    ),
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name="Organisation", table="users_organisation"
                )
            ],
        ),
    ]
