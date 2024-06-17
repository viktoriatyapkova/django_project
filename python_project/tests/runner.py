"""Module with runner tests."""

from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """
    Prepare the database by creating the 'online' schema if it does not exist.

    Args:
        self: The database connection object.
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS online;')


class PostgresSchemaRunner(DiscoverRunner):
    """
    Custom test runner for managing PostgreSQL schema preparation.

    Attributes:
        setup_databases: Override of the base method to prepare databases for testing.

    Methods:
        setup_databases(): Setup method that prepares databases for testing.
    """

    def setup_databases(self, **kwargs: Any) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """
        Prepare databases for testing.

        Args:
            kwargs: Additional keyword arguments.

        Returns:
            A list of tuples containing the BaseDatabaseWrapper.
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
