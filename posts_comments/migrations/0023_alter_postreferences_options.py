# Generated by Django 4.2.4 on 2024-02-01 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0022_rename_submissionreferences_postreferences"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="postreferences",
            options={"verbose_name": "User Post and Linked References"},
        ),
    ]