# Generated by Django 4.2.4 on 2023-09-18 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("open_problems", "0025_alter_openproblems_options_and_more"),
        ("annotations", "0009_alter_subjectproblem_table_comment_and_more"),
    ]

    operations = [
        migrations.AlterModelTableComment(
            name="subject",
            table_comment="A subject annotation describing the topic of the open problem",
        ),
        migrations.AlterField(
            model_name="subject",
            name="description",
            field=models.TextField(blank=True, db_column="description", null=True),
        ),
        migrations.AlterField(
            model_name="subject",
            name="id",
            field=models.AutoField(db_column="", primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="subject",
            name="title",
            field=models.CharField(
                blank=True, db_column="title", max_length=40, null=True
            ),
        ),
        migrations.AlterField(
            model_name="subjectreferences",
            name="ref",
            field=models.OneToOneField(
                db_column="reference_id",
                on_delete=django.db.models.deletion.DO_NOTHING,
                primary_key=True,
                serialize=False,
                to="open_problems.reference",
            ),
        ),
        migrations.AlterField(
            model_name="subjectreferences",
            name="subject",
            field=models.ForeignKey(
                db_column="subject_id",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="annotations.subject",
            ),
        ),
        migrations.AlterModelTable(
            name="subject",
            table="Subject",
        ),
    ]
