# Generated by Django 5.0.3 on 2024-03-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0028_remove_tag_open_problems"),
        ("open_problems", "0043_alter_openproblem_table"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submittedopenproblem",
            name="species",
        ),
        migrations.AddField(
            model_name="openproblem",
            name="tags",
            field=models.ManyToManyField(to="annotations.tag"),
        ),
        migrations.AddField(
            model_name="submittedopenproblem",
            name="tags",
            field=models.ManyToManyField(blank=True, to="annotations.tag"),
        ),
    ]