"""
This module defines the BasicGenerator class, which combines a retriever and a
generator LLM to process a chat sequence and produce responses in a structured
pipeline.
"""

import logging
from graphygie.llm import LLM
from graphygie.llm.chat import Chat
from typing import Callable


class BasicGenerator(LLM):
    """
    A pipeline-based generator that uses two LLMs:
    - A retriever LLM to fetch or infer relevant context.
    - A generator LLM to produce the final response.
    """

    def __init__(
        self,
        retriever: LLM,
        generator: LLM,
        chat: Chat,
        maker: Callable[[Chat, str], Chat],
    ) -> None:
        """
        Initializes the BasicGenerator pipeline.

        Parameters:
        - retriever (LLM): The LLM used to retrieve context or information.
        - generator (LLM): The LLM used to generate the final response.
        - chat (Chat): The initial chat history.
        - maker (Callable[[Chat, str], Chat]): A function that merges the
            existing chat
          with the retrieved result to build the input for the generator.
        """
        self._retriever = retriever
        self._generator = generator
        self._chat = chat
        self._maker = maker

    def chat(self, chat: Chat = list()) -> str:
        logger: logging.Logger = logging.getLogger(__name__)

        result: str = self._retriever.chat(chat)
        chat = self._maker(self._chat, result) + chat

        logger.info(result)

        return self._generator.chat(chat)
