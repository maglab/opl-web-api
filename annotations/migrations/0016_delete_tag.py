# Generated by Django 4.2.4 on 2024-02-05 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("annotations", "0015_tag"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Tag",
        ),
    ]