# Generated by Django 5.1 on 2024-10-13 16:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("sets", models.IntegerField()),
                ("reps", models.IntegerField()),
                ("weight", models.FloatField()),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Progress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("sets_completed", models.IntegerField()),
                ("reps_completed", models.IntegerField()),
                ("weight_lifted", models.FloatField()),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="welcome.exercise",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkoutPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("target_muscles", models.CharField(max_length=200)),
                ("days_per_week", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="exercise",
            name="workout_plan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="welcome.workoutplan"
            ),
        ),
    ]
