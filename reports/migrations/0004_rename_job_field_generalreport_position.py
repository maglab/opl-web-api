# Generated by Django 5.0.3 on 2024-04-26 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0003_remove_generalreport_contact_generalreport_email_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="generalreport",
            old_name="job_field",
            new_name="position",
        ),
    ]