"""
This module defines the Neo4j class, a concrete implementation of the Database
interface that connects to a Neo4j graph database and formats query results as
readable text.
"""

from graphygie.retrieval.database import Database
from neo4j import Driver, GraphDatabase, Query, Result
from neo4j.graph import Graph
from typing import Optional, cast


class Neo4jExtra(Database):
    """
    A Neo4j database implementation of the Database interface.

    Connects to a Neo4j instance and runs Cypher queries,
    returning the results in a human-readable format.
    """

    def __init__(self, uri: str, username: str, password: str, database: str) -> None:
        """
        Initializes the Neo4j driver.

        Parameters:
        - uri (str): The URI of the Neo4j server
            (e.g., "bolt://localhost:7687").
        - username (str): Username for authentication.
        - password (str): Password for authentication.
        - database (str): The name of the Neo4j database to connect to.
        """

        self.driver: Driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database: str = database
        self._info = None

    @property
    def info(self) -> Optional[dict[str, int]]:
        """Returns statistics from the last query"""
        return self._info

    def query(self, query: str) -> str:
        try:
            self.driver.verify_connectivity()
            with self.driver.session(database=self.database) as session:
                result: Result = session.run(cast(Query, query))

                graph: Graph = result.graph()

                self._info = {
                    "error": 0,
                    "nodes": len(graph.nodes),
                    "edges": len(graph.relationships),
                }

                node_labels: dict[int, str] = {}
                for node in graph.nodes:
                    name = node.get("name") or node.get("title") or f"Node_{node.id}"
                    node_labels[node.id] = name

                textual_rels: list[str] = []
                for rel in graph.relationships:
                    if rel.start_node is None:
                        start = "<empty>"
                    else:
                        start = node_labels[rel.start_node.id]
                    if rel.end_node is None:
                        end = "<empty>"
                    else:
                        end = node_labels[rel.end_node.id]
                    rel_type = rel.type
                    textual_rels.append(f"{start} -[{rel_type}]-> {end}.")

                return "\n".join(textual_rels)
        except:
            self._info = {"error": 1, "nodes": 0, "edges": 0}
            return ""

    def __del__(self) -> None:
        """
        Closes the Neo4j driver connection when the object is deleted.
        """
        self.driver.close()
