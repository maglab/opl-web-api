# Generated by Django 4.2.4 on 2024-02-12 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0024_rename_submission_id_postreferences_post_id"),
        ("annotations", "0017_rename_species_id_species_id"),
        ("open_problems", "0028_alter_reference_table_comment"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="OpenProblems",
            new_name="OpenProblem",
        ),
    ]
