# Generated by Django 5.0.3 on 2025-01-08 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0052_openproblem_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="openproblem",
            name="title",
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name="submittedopenproblem",
            name="title",
            field=models.CharField(max_length=300),
        ),
    ]
