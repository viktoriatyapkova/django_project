"""Module for app."""

from django.apps import AppConfig


class PythonProjectAppConfig(AppConfig):
    """
    Configuration class for the python_project_app app.

    Attributes:
        default_auto_field (str): The default auto-field for the app.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "python_project_app"
