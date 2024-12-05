from django.db import models
from django.contrib.auth.models import User

class WorkoutPlan(models.Model):
    MUSCLE_GROUPS = [
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('biceps', 'Biceps'),
        ('triceps', 'Triceps'),
        ('legs', 'Legs'),
        ('shoulders', 'Shoulders'),
        ('core', 'Core'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200)
    target_muscles = models.CharField(max_length=20, choices=MUSCLE_GROUPS)
    days_per_week = models.IntegerField()
    calories_burned = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_workout_name')
        ]
        indexes = [
            models.Index(fields=['user', 'target_muscles'], name='user_target_muscle_idx'),
        ]

class MuscleGroupExercises(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    back_exercises = models.IntegerField(default=0)
    chest_exercises = models.IntegerField(default=0)
    biceps_exercises = models.IntegerField(default=0)
    triceps_exercises = models.IntegerField(default=0)
    legs_exercises = models.IntegerField(default=0)
    shoulders_exercises = models.IntegerField(default=0)
    core_exercises = models.IntegerField(default=0)