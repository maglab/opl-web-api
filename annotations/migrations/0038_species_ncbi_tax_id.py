# Generated by Django 5.0.3 on 2024-04-18 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0037_alter_species_full_name_alter_species_genus_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="species",
            name="ncbi_tax_id",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]