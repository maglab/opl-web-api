# Generated by Django 4.2.2 on 2023-07-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="submission",
            managers=[],
        ),
        migrations.AlterField(
            model_name="submission",
            name="references",
            field=models.TextField(blank=True, null=True),
        ),
    ]
