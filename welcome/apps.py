from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "polls"

class WelcomeConfig(AppConfig):
    name = 'welcome'
