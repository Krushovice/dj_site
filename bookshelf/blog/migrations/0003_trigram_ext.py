# Generated by Django 5.1.2 on 2024-10-28 07:12
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_comment"),
    ]

    operations = [
        TrigramExtension(),
    ]
