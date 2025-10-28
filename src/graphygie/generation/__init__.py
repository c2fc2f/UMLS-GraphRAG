"""
This module exposes the public interface for the generator components,
including:

- BasicGenerator: A pipeline-based generator combining a retriever and a
    generator LLM.
"""

from .basic_generator import BasicGenerator

__all__: list[str] = ["BasicGenerator"]
