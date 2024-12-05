from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import WorkoutPlan, MuscleGroupExercises
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Avg, Count, Sum, F


@login_required
def index(request):
    return render(request, 'welcome/index.html')

@login_required
def home(request):
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        target_muscles = request.POST.get('target_muscles')
        days_per_week = request.POST.get('days_per_week')
        calories_burned = request.POST.get('calories_burned')

        if name and target_muscles and days_per_week and calories_burned:
            try:
                WorkoutPlan.objects.create(
                    user=request.user,
                    name=name,
                    target_muscles=target_muscles,
                    days_per_week=days_per_week,
                    calories_burned=calories_burned
                )

                increase_muscle_group_count(request.user, target_muscles)
                return redirect('home')
            except IntegrityError:
                error_message = f"Adding workout failed, workout with the name '{name}' already exists."

    workout_plans = WorkoutPlan.objects.filter(user=request.user)
    muscle_groups = WorkoutPlan.MUSCLE_GROUPS

    return render(request, 'welcome/home.html', {'workout_plans': workout_plans, 'error_message': error_message, 'muscle_groups': muscle_groups})

@login_required
def my_workouts(request):
    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM welcome_workoutplan WHERE user_id = %s
        """, [user_id])
        rows = cursor.fetchall()
    
    workout_plans = []
    for row in rows:
        workout_plans.append({
            'id': row[0],
            'name': row[1],
            'target_muscles': row[2],
            'days_per_week': row[3],
            'calories_burned': row[5],
            'user_id': row[4],
        })

    return render(request, 'welcome/my_workouts.html', {'workout_plans': workout_plans})

@login_required
def update_workout(request, id):
    workout = get_object_or_404(WorkoutPlan, id=id)
    old_target_muscles = workout.target_muscles
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        target_muscles = request.POST.get('target_muscles')
        days_per_week = request.POST.get('days_per_week')
        calories_burned = request.POST.get('calories_burned')

        if name != workout.name:
            workout.name = name

        workout.target_muscles = target_muscles
        workout.days_per_week = days_per_week
        workout.calories_burned = calories_burned

        try:
            workout.save()
            if old_target_muscles != target_muscles:
                decrease_muscle_group_count(request.user, old_target_muscles)
                increase_muscle_group_count(request.user, target_muscles)
            return redirect('my_workouts')
        except IntegrityError:
            error_message = f"A workout with the name '{name}' already exists for this user."

    return render(request, 'welcome/update_workout.html', {'workout': workout, 'error_message': error_message,})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'welcome/index.html')
    else:
        form = UserCreationForm()
    return render(request, 'welcome/register.html', {'form': form})

@login_required
def delete_workout(request, id):
    workout = get_object_or_404(WorkoutPlan, id=id)
    target_muscles = workout.target_muscles
    decrease_muscle_group_count(request.user, target_muscles)
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM welcome_workoutplan WHERE id = %s", [id])
    return redirect('my_workouts')

def increase_muscle_group_count(user, target_muscles):
    muscle_counts, created = MuscleGroupExercises.objects.get_or_create(user=user)

    if target_muscles == 'back':
        muscle_counts.back_exercises += 1
    elif target_muscles == 'chest':
        muscle_counts.chest_exercises += 1
    elif target_muscles == 'biceps':
        muscle_counts.biceps_exercises += 1
    elif target_muscles == 'triceps':
        muscle_counts.triceps_exercises += 1
    elif target_muscles == 'legs':
        muscle_counts.legs_exercises += 1
    elif target_muscles == 'shoulders':
        muscle_counts.shoulders_exercises += 1
    elif target_muscles == 'core':
        muscle_counts.core_exercises += 1

    muscle_counts.save()

def decrease_muscle_group_count(user, target_muscles):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            UPDATE welcome_musclegroupexercises
            SET {target_muscles}_exercises = {target_muscles}_exercises - 1
            WHERE user_id = %s
            """,
            [user.id]
        )

@login_required
def reports(request):
    selected_group = request.GET.get('muscle_group')
    stats = None
    workouts = None

    if selected_group:
        workouts = WorkoutPlan.objects.filter(user=request.user, target_muscles=selected_group)

        total_workouts = workouts.count()
        avg_calories_burned = workouts.aggregate(Avg('calories_burned'))['calories_burned__avg'] or 0
        avg_days_per_week = workouts.aggregate(Avg('days_per_week'))['days_per_week__avg'] or 0
        total_calories_per_week = workouts.aggregate(
            total_calories=Sum(F('calories_burned') * F('days_per_week'))
        )['total_calories'] or 0

        stats = {
            'total_workouts': total_workouts,
            'avg_calories_burned': round(avg_calories_burned, 2),
            'avg_days_per_week': round(avg_days_per_week, 2),
            'total_calories_per_week': total_calories_per_week
        }

    muscle_groups = WorkoutPlan.MUSCLE_GROUPS

    return render(request, 'welcome/reports.html', {'stats': stats, 'workouts': workouts, 'selected_group': selected_group, 'muscle_groups': muscle_groups})