# Generated by Django 5.0.3 on 2024-03-12 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts_comments', '0025_rename_submission_comment_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_id',
            new_name='id',
        ),
    ]
