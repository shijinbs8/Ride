# Generated by Django 4.2.3 on 2024-12-04 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apps", "0002_alter_ride_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="current_location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
