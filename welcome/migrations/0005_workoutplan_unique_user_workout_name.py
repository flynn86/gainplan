# Generated by Django 5.1 on 2024-12-04 17:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("welcome", "0004_musclegroupexercises"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="workoutplan",
            constraint=models.UniqueConstraint(
                fields=("user", "name"), name="unique_user_workout_name"
            ),
        ),
    ]
