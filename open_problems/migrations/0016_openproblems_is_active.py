# Generated by Django 4.2.3 on 2023-08-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0015_rename_question_id_problemreference_problem_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="openproblems",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]