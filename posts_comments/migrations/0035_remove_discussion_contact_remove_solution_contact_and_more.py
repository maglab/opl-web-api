# Generated by Django 5.0.3 on 2024-03-17 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0034_alter_discussion_open_problem_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="discussion",
            name="contact",
        ),
        migrations.RemoveField(
            model_name="solution",
            name="contact",
        ),
        migrations.AddField(
            model_name="discussion",
            name="alias",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="solution",
            name="alias",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="alias",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
