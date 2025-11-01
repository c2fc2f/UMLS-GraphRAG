"""
This module exposes the public interface for the database layer, including:

- Neo4jExtra: Concrete implementation of the Database interface using Neo4j.
"""

from .neo4j import Neo4jExtra

__all__: list[str] = ["Neo4jExtra"]
