# Generated by Django 5.0.3 on 2024-04-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0038_species_ncbi_tax_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gene",
            name="gene_name",
            field=models.CharField(max_length=100),
        ),
    ]
