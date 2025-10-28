"""
This module defines the abstract interface for a Database.
"""

from abc import ABC, abstractmethod


class Database(ABC):
    """
    Abstract base class for database access.
    """

    @abstractmethod
    def query(self, query: str) -> str:
        """
        Executes a query string against the database.

        Parameters:
        - query (str): The query to execute.

        Returns:
        - str: The result of the query.
        """
        ...
