"""
This module defines the Graph retriever class, which combines a language model
(LLM) and a graph database to answer chat-based queries.

The LLM generates a query from the chat history, which is then executed on the
database.
"""

from graphygie.llm import LLM
from graphygie.llm.chat import Chat
from .database import Database
import logging


class Graph(LLM):
    """
    A graph-based retriever that uses an LLM to generate a query from a chat
    history, then executes that query against a graph database.

    Attributes:
    - _llm (LLM): The language model used to generate queries.
    - _database (Database): The graph database used to retrieve information.
    """

    def __init__(self, llm: LLM, database: Database) -> None:
        """
        Initializes the Graph retriever with a language model and a database.

        Parameters:
        - llm (LLM): The language model used to interpret the chat history.
        - database (Database): The database queried with the generated output.
        """
        self._llm: LLM = llm
        self._database: Database = database

    def chat(self, chat: Chat = list()) -> str:
        logger: logging.Logger = logging.getLogger(__name__)

        query: str = self._llm.chat(chat)

        logger.info(query)

        result: str = self._database.query(query)

        return result
