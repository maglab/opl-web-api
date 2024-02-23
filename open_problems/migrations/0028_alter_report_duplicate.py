# Generated by Django 4.2.4 on 2024-02-23 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0027_alter_report_duplicate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="duplicate",
            field=models.ManyToManyField(
                blank=True, related_name="duplicates", to="open_problems.openproblems"
            ),
        ),
    ]