# Generated by Django 5.0.3 on 2024-03-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0025_alter_tagproblem_table_comment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
