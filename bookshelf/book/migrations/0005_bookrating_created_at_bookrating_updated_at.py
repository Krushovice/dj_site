# Generated by Django 5.1.2 on 2024-11-04 02:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0004_remove_book_isbn"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookrating",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bookrating",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]