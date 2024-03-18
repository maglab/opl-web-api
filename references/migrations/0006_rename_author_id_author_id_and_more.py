# Generated by Django 5.0.3 on 2024-03-14 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("references", "0005_reference"),
    ]

    operations = [
        migrations.RenameField(
            model_name="author",
            old_name="author_id",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="author",
            old_name="author_name",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="journal",
            old_name="journal_id",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="journal",
            old_name="journal_name",
            new_name="name",
        ),
    ]
