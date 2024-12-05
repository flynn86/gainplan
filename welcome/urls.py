from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='welcome'),
    path('home/', views.home, name='home'),
    path('my_workouts/', views.my_workouts, name='my_workouts'),
    path('update/<int:id>/', views.update_workout, name='update_workout'),
    path('login/', auth_views.LoginView.as_view(template_name='welcome/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('delete_workout/<int:id>/', views.delete_workout, name='delete_workout'),
    path('reports/', views.reports, name='reports'),
]
