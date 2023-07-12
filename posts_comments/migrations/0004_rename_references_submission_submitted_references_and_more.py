# Generated by Django 4.2.2 on 2023-07-12 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0003_remove_researchsubmission_contact_and_more"),
        ("posts_comments", "0003_remove_submission_date_submission_created_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="submission",
            old_name="references",
            new_name="submitted_references",
        ),
        migrations.AddField(
            model_name="submission",
            name="reviewed_references",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="open_problems.reference",
            ),
        ),
    ]
