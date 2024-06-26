# Generated by Django 5.0.3 on 2024-03-17 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0032_remove_submittedreferences_submission_id_and_more"),
        ("references", "0008_remove_reference_link_alter_reference_authors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discussion",
            name="references",
            field=models.ManyToManyField(blank=True, to="references.reference"),
        ),
        migrations.AlterField(
            model_name="solution",
            name="references",
            field=models.ManyToManyField(blank=True, to="references.reference"),
        ),
    ]
