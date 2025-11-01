from neo4j import GraphDatabase
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.embeddings import OllamaEmbeddings
from dotenv import load_dotenv

import logging
import os


def unwrap(value: str | None) -> str:
    if value is None:
        raise ValueError("called `unwrap()` on a `None` value")
    return value


def main() -> None:
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO, format="{levelname}:{name}:\n{message}", style="{"
    )

    # Connect to Neo4j database
    driver = GraphDatabase.driver(
        unwrap(os.getenv("NEO4J_URI")),
        auth=(unwrap(os.getenv("NEO4J_USERNAME"), unwrap(os.getenv("NEO4J_PASSWORD")))),
    )

    # 2. Retriever
    # Create Embedder object, needed to convert the user question (text) to a
    # vector
    embedder = OllamaEmbeddings(
        host=unwrap(os.getenv("OLLAMA_URI")), model="embeddinggemma:latest"
    )

    # Initialize the retriever
    retriever = VectorRetriever(
        driver,
        unwrap(os.getenv("NEO4J_INDEX")),
        embedder,
        neo4j_database=os.getenv("NEO4J_DATABASE"),
    )

    # 3. LLM
    # Note: the OPENAI_API_KEY must be in the env vars
    llm = OpenAILLM(
        host=unwrap(os.getenv("OPENROUTER_URI")),
        api_key=unwrap(os.getenv("OPENROUTER_TOKEN")),
        model_name="qwen/qwen3-235b-a22b:free",
        model_params={"temperature": 0},
    )

    # Initialize the RAG pipeline
    rag = GraphRAG(retriever=retriever, llm=llm)

    # Query the graph
    query_text = "What are the main cognitive and behavioral changes associated with Frontal Lobe Syndrome?"
    response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
    print(response.answer)


if __name__ == "__main__":
    main()
