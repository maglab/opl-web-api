# Generated by Django 5.0.3 on 2024-04-24 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0039_alter_gene_gene_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="verified",
            field=models.BooleanField(default=False),
        ),
    ]
