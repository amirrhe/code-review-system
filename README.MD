```markdown
# Microservice-Based Code Review System

This repository contains two microservices that together implement a code review system using an LLM (Large Language Model):

1. **LLM Service (AI Gateway)**  
   Routes function analysis requests to an LLM provider (e.g., a local model via Ollama, or in the future OpenAI/DeepSeek).  
   - **Endpoint:** `POST /analyze`
   - **Functionality:** Receives Python function code and returns analysis suggestions.

2. **Code Analysis Service**  
   Handles repository processing and function analysis. It downloads a GitHub repository, extracts specified Python function code, and sends it to the LLM Service for analysis.  
   - **Endpoints:**  
     - `POST /analyze/start`: Starts a background job to clone a repository and returns a job ID.  
     - `POST /analyze/function`: Extracts a function from the cloned repo (using the job ID) and forwards it to the LLM Service.

The project uses FastAPI for building the APIs, Poetry for dependency management, and Docker for containerization. Nox is used for automating tests and code quality checks (linting, type checking, and formatting).

---

## Project Structure

```plaintext
.
├── code_analysis
│   ├── Dockerfile
│   ├── README.MD           # Code Analysis Service documentation
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py         # Entry point for the Code Analysis Service
│   │   └── routes
│   │       ├── __init__.py
│   │       └── analyze.py  # API endpoints and business logic
│   ├── poetry.lock
│   └── pyproject.toml
├── llm_service
│   ├── Dockerfile
│   ├── README.md           # LLM Service documentation
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py         # Entry point for the LLM Service
│   │   └── routes
│   │       ├── __init__.py
│   │       └── analyze.py  # API endpoints and provider logic using the Strategy Pattern
│   ├── poetry.lock
│   └── pyproject.toml
└── noxfile.py              # Nox sessions for tests, linting, formatting, etc.
```

---

## Overview & Design

- **Microservices Architecture:**  
  The project is split into two distinct services that communicate over HTTP. This design promotes separation of concerns and scalability.

- **LLM Service:**  
  Uses a Strategy Pattern to select an LLM provider based on the `LLM_PROVIDER` environment variable. The current implementation supports a local model via the Ollama package.

- **Code Analysis Service:**  
  Clones a GitHub repository asynchronously using GitPython and extracts Python function code using regex. It then calls the LLM Service for code analysis.

- **Service Communication:**  
  The Code Analysis Service sends requests to the LLM Service. In a Docker Compose setup, the Code Analysis Service uses the service name (e.g., `llm_service`) to reach the LLM Service.

- **Quality & Automation:**  
  The project employs Poetry for dependency management, Nox for task automation, and tools like Pylint, Mypy, and Ruff for code quality.

---

## Setup & Running Locally

### Prerequisites

- Python (3.10 recommended)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (for containerization)
- [Git](https://git-scm.com/)

### For Each Service

1. **Navigate to the Service Directory**

   - For the LLM Service:
     ```bash
     cd llm_service
     ```
   - For the Code Analysis Service:
     ```bash
     cd code_analysis
     ```

2. **Configure Poetry to Use a Local Virtual Environment**

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. **Install Dependencies**

   ```bash
   poetry install
   ```

4. **Run the Service with Uvicorn**

   - LLM Service (by default on port 8000):
     ```bash
     poetry run uvicorn app.main:app --reload --port 8000
     ```
   - Code Analysis Service (by default on port 8001):
     ```bash
     poetry run uvicorn app.main:app --reload --port 8001
     ```

5. **Interact with the API Documentation**

   - LLM Service: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Code Analysis Service: [http://localhost:8001/docs](http://localhost:8001/docs)

---


## Nox Automation

The `noxfile.py` in the repository root automates tasks such as linting, type checking, testing, and formatting for both services. Run a session with:

```bash
nox -s lint   # For linting (using ruff, pylint, etc.)
nox -s tests  # For running tests (if implemented)
nox -s format # For code formatting
```

---


## Code Quality

- **Linting & Type Checking:**  
  Use Pylint, Mypy, and Ruff:
  ```bash
  poetry run pylint <module_or_directory>
  poetry run mypy .
  poetry run ruff check .
  ```

- **Nox:**  
  Automate tasks with nox (see Nox sessions in `noxfile.py`).

---

