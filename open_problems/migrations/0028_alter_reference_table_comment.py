# Generated by Django 4.2.4 on 2024-02-01 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0027_rename_full_citation_reference_citation"),
    ]

    operations = [
        migrations.AlterModelTableComment(
            name="reference",
            table_comment="Contains all reference information",
        ),
    ]
