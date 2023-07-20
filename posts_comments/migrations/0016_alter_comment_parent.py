# Generated by Django 4.2.2 on 2023-07-20 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("posts_comments", "0015_rename_comments_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="posts_comments.comment",
            ),
        ),
    ]
