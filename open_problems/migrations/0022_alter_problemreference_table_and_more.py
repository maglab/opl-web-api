# Generated by Django 4.2.4 on 2023-09-08 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("open_problems", "0021_alter_reftype_table_comment"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="problemreference",
            table="ProblemReferences",
        ),
        migrations.AlterModelTable(
            name="problemrelation",
            table="ProblemRelation",
        ),
        migrations.AlterModelTable(
            name="submittedproblems",
            table="SubmittedProblems",
        ),
    ]
