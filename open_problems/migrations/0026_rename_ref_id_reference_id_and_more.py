# Generated by Django 4.2.4 on 2024-02-01 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0025_alter_openproblems_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reference",
            old_name="ref_id",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="reference",
            old_name="ref_title",
            new_name="title",
        ),
    ]
