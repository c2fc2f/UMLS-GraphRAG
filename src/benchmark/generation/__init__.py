"""
This module exposes the public interface for the generator components,
including:

- BasicGeneratorExtra: A pipeline-based generator combining a retriever and a
    generator LLM.
"""

from .basic_generator import BasicGeneratorExtra

__all__: list[str] = ["BasicGeneratorExtra"]
