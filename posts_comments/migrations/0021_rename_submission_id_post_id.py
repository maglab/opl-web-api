# Generated by Django 4.2.4 on 2024-02-01 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0020_rename_submission_post"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="submission_id",
            new_name="id",
        ),
    ]
