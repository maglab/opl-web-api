# Generated by Django 5.0.3 on 2024-03-06 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='authors',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='journal_id',
        ),
        migrations.DeleteModel(
            name='RefType',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Journal',
        ),
        migrations.DeleteModel(
            name='Reference',
        ),
    ]