# Med-KAG

This project aims to create **Graphygie**, a Python library designed to simplify the creation of **GraphRAG** pipelines.  
It was developed as part of the [KGConversationalAI project](https://github.com/Gabriel382/KGConversationalAI), which focuses on assisting doctors by creating a **3D assistant** capable of answering their medical questions.

The graph used here is extracted from the dataset published in the following paper:
📎 [BioPropaPhen and BioPropaPhenKG - Zenodo](https://zenodo.org/records/10911980)

---

## 📦 Project Overview

Graph-RAG is a method of retrieving information from a **knowledge graph** to augment the context of a language model, rather than retrieving text passages. This repository uses a Neo4j database containing the UMLS knowledge graph, which includes medical concepts and their relationships.

> ⚠️ The database includes **location-related data**, but these are **not used** in this project.

---

## 🧰 Features

* Uses the UMLS Neo4j graph dump provided by the original GraphRAG publication.
* Provides a `setup.sh` script to download, import, and migrate the Neo4j database.
* Launches a local Neo4j instance using Docker Compose.
* Modular and type-annotated Python codebase.
* Interface-based architecture for flexibility and clarity.

---

## 📁 Repository Structure

```
.
├── docker-compose.yml                      # Docker service configuration for Neo4j
├── flake.nix / flake.lock                  # Nix environment definitions
├── pyproject.toml                          # Python project configuration and dependencies
├── setup.sh                                # Script to download, load and migrate Neo4j dump
├── uv.lock                                 # UV package manager lock file
├── src/
│   ├── examples/                           # Example implementations
│   │   └── basic/                          # Basic GraphRAG example
│   │       ├── main.py                     # Example entry point
│   │       ├── resources/
│   │       │   └── prompt/                 # Prompt templates
│   │       │       ├── generator_system.md
│   │       │       ├── retrieval_system.md
│   │       │       └── user.md
│   │       └── util/                       # Example utility functions
│   │           ├── cleaner.py
│   │           ├── compose.py
│   │           ├── generator_system_prompt.py
│   │           ├── read_to_string.py
│   │           ├── unwrap.py
│   │           └── user_prompt.py
│   └── graphygie/                          # Core Graphygie library
│       ├── generation/                     # Response generation
│       │   └── basic_generator.py          # Generator using retriever + LLM
│       ├── llm/                            # LLM integrations
│       │   ├── chat.py                     # Chat interface
│       │   ├── llm.py                      # Base LLM class
│       │   ├── ollama.py                   # Ollama integration
│       │   └── openai.py                   # OpenAI integration
│       └── retrieval/                      # Graph and database retrieval logic
│           ├── database/
│           │   ├── database.py             # Database interface
│           │   └── neo4j.py                # Neo4j implementation
│           └── graph.py                    # Graph retrieval logic
├── LICENSE
└── README.md                               # You're here!
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/culxttes/UMLS-GraphRAG.git
cd UMLS-GraphRAG
```

### 2. Prepare the Neo4j Graph Database

Run the setup script (only once):

```bash
chmod +x setup.sh
./setup.sh
```

This will:

* Download the Neo4j dump file from [Zenodo](https://zenodo.org/records/10911980)
* Load it into the proper `data/` directory
* Run necessary migrations

> 🔧 The database is not turn-key out of the box — it must be set up manually using this script.

### 3. Launch the Neo4j Server

```bash
docker compose up -d neo4j
```

This will start a local Neo4j server accessible at `bolt://localhost:7687` with default credentials (`neo4j/<empty password>`).

### 4. Install Python Dependencies

```bash
uv sync --extra examples
```

> This will create a virtual environment and install all dependencies from `pyproject.toml`

### 5. Run the Application

```bash
uv run graphygie-basic
```

---

## ❗ Important Notes

* **No tests** are currently included.
* Graphygie is intended to be extended for projects like **KGConversationalAI**.
* This project does **not** currently use vector stores — all context is retrieved from the graph.
* Make sure the Neo4j container is running before executing Python code.

---

## 📄 License

This project is licensed under the GPLv3 License.
UMLS data and graph dumps are property of the U.S. National Library of Medicine (NLM). Usage must comply with their licensing terms.
