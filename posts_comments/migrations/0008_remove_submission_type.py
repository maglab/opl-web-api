# Generated by Django 4.2.2 on 2023-07-12 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0007_comments"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="submission",
            name="type",
        ),
    ]
