# Generated by Django 4.2.2 on 2023-07-17 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0009_alter_reference_authors_alter_reference_isbn_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reference",
            name="publish_date",
            field=models.CharField(max_length=4),
        ),
    ]