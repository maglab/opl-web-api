# Generated by Django 4.2.4 on 2024-02-13 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("references", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reference",
            old_name="publish_date",
            new_name="year",
        ),
    ]
