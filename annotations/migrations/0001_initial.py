# Generated by Django 4.2.2 on 2023-07-16 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("open_problems", "0006_rename_question_id_openproblems_problem_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Species",
            fields=[
                ("species_id", models.AutoField(primary_key=True, serialize=False)),
                ("genus", models.CharField(max_length=50, null=True)),
                ("species", models.CharField(max_length=50, null=True)),
            ],
            options={
                "db_table": "Species",
            },
        ),
        migrations.CreateModel(
            name="Theory",
            fields=[
                (
                    "theory_id",
                    models.AutoField(
                        db_column="Theory_id", primary_key=True, serialize=False
                    ),
                ),
                (
                    "theorytitle",
                    models.CharField(
                        blank=True, db_column="TheoryTitle", max_length=40, null=True
                    ),
                ),
                (
                    "theorydesc",
                    models.TextField(blank=True, db_column="TheoryDesc", null=True),
                ),
                (
                    "parent_t_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="annotations.theory",
                    ),
                ),
            ],
            options={
                "db_table": "Theory",
                "db_table_comment": "A theory annotation describing and categorisingthe open problem",
            },
        ),
        migrations.CreateModel(
            name="TheoryProblem",
            fields=[
                ("annotation_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "open_problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="open_problems.openproblems",
                    ),
                ),
                (
                    "theory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="annotations.theory",
                    ),
                ),
            ],
            options={
                "db_table_comment": "Relation table for each theory and open problem",
            },
        ),
        migrations.CreateModel(
            name="SpeciesProblems",
            fields=[
                ("annotation_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "open_problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="open_problems.openproblems",
                    ),
                ),
                (
                    "species",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="annotations.species",
                    ),
                ),
            ],
            options={
                "db_table_comment": "Relation table for each species and open problem",
            },
        ),
        migrations.CreateModel(
            name="TheoryReferences",
            fields=[
                (
                    "ref",
                    models.OneToOneField(
                        db_column="Ref_id",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="open_problems.reference",
                    ),
                ),
                (
                    "theory",
                    models.ForeignKey(
                        db_column="Theory_id",
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="annotations.theory",
                    ),
                ),
            ],
            options={
                "db_table": "theory_reference",
                "unique_together": {("ref", "theory")},
            },
        ),
    ]
