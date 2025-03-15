```markdown
# LLM Service (AI Gateway)

This microservice serves as an AI gateway that routes function analysis requests to one of several LLM providers. Based on the environment variable `LLM_PROVIDER`, the service can forward requests to a remote provider (e.g., OpenAI, DeepSeek) or use a locally hosted LLM (via the Ollama package).

## Overview

- **Routing Logic:**  
  The service uses a Strategy Pattern to determine which LLM provider to use. Currently, only the local provider is fully implemented (using Ollama), while the others are placeholders.

- **API Endpoint:**  
  - `POST /analyze`: Receives a JSON payload with Python function code and returns suggestions (e.g., documentation improvements or code style advice) in a format compatible with the Code Analysis Service.

- **Environment Configuration:**  
  - `LLM_PROVIDER`: Determines the provider to use (e.g., `local`, `openai`, or `deepseek`).  
  - Optionally, you can set additional variables (e.g., `OLLAMA_HOST`) if you need to route requests to an externally hosted Ollama service.

## Technology & Design Choices

- **FastAPI:** Provides a fast, asynchronous API framework.
- **Ollama Package:** Integrates with a local LLM model (e.g., `"qwen2.5-coder:1.5b"`).
- **Strategy Pattern:** Decouples provider-specific logic, making it easy to add new LLM providers in the future.
- **Poetry:** Manages dependencies and virtual environments.
- **Docker:** Containerizes the microservice for reproducible deployments.

## Setup & Running the Service

### Local Setup

1. **Clone the Repository and Navigate to the LLM Service Directory:**

   ```bash
   git clone <repository_url>
   cd llm_service
   ```

2. **Configure Poetry to Use a Local Virtual Environment:**

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. **Install Dependencies:**

   ```bash
   poetry install
   ```

4. **Run the Service Locally:**

   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```

5. **Access the API Documentation:**

   Open your browser at [http://localhost:8000/docs](http://localhost:8000/docs) to view and interact with the Swagger UI.

### Docker Setup

1. **Build the Docker Image:**

   From the `llm_service` directory:

   ```bash
   docker build -t llm_service .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 8000:8000 llm_service
   ```


## API Endpoint

### POST `/analyze`

- **Description:**  
  Analyzes Python function code by routing the request to the selected LLM provider.

- **Request Example:**

  ```json
  {
    "function_code": "def add(a, b): return a + b"
  }
  ```

- **Response Example:**

  ```json
  {
    "suggestions": [
      "Consider adding type hints.",
      "Add a docstring for better documentation."
    ]
  }
  ```



- **Linting & Type Checking:**  
  This project uses Pylint, Mypy, and Ruff for code quality checks.
- **Nox:**  
  Automate quality and testing tasks using Nox. See the repository’s `noxfile.py` for details.
