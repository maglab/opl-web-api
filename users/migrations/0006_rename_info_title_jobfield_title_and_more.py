# Generated by Django 5.0.3 on 2024-05-02 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_rename_info_id_jobfield_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="jobfield",
            old_name="info_title",
            new_name="title",
        ),
        migrations.RenameField(
            model_name="organisation",
            old_name="info_title",
            new_name="title",
        ),
    ]
