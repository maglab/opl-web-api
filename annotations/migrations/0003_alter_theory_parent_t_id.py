# Generated by Django 4.2.2 on 2023-07-17 11:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0002_gene_geneproblem"),
    ]

    operations = [
        migrations.AlterField(
            model_name="theory",
            name="parent_t_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="annotations.theory",
            ),
        ),
    ]
