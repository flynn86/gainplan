# Generated by Django 5.1 on 2024-10-29 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("welcome", "0002_alter_workoutplan_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="progress",
            name="exercise",
        ),
        migrations.AddField(
            model_name="workoutplan",
            name="calories_burned",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Exercise",
        ),
        migrations.DeleteModel(
            name="Progress",
        ),
    ]
