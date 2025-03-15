```markdown
# Code Analysis Service

This microservice handles repository processing and function analysis. It downloads a GitHub repository asynchronously, extracts specified Python function code, and forwards the extracted code to an LLM Service for further analysis. The service is built using FastAPI and leverages GitPython, BackgroundTasks, and Pydantic.

## Overview

- **Repository Cloning:**  
  Uses GitPython to clone a GitHub repository asynchronously.  
- **Function Extraction:**  
  Extracts a function (based on a simple regex) from the downloaded repository.
- **LLM Integration:**  
  Forwards the extracted function code to an LLM Service (e.g., OpenAI, DeepSeek, or a local LLM using Ollama) for analysis.
- **API Endpoints:**
  - `POST /analyze/start`: Starts a background job to clone a repository and returns a job ID.
  - `POST /analyze/function`: Extracts a function from the repository (using the provided job ID) and sends it to the LLM Service for analysis.

## Technology & Design Choices

- **FastAPI:** Provides an asynchronous, high-performance API framework.
- **GitPython:** Facilitates cloning of Git repositories.
- **BackgroundTasks:** Allows repository downloads to run asynchronously.
- **Pydantic:** Validates and serializes input and output data.
- **Docker & Docker Compose:** Containerizes the microservice and allows seamless communication between services.
- **Poetry:** Manages dependencies and virtual environments.

## Setup & Running the Service

### Local Setup

1. **Clone the Repository and Navigate to the Code Analysis Service Directory:**

   ```bash
   git clone <repository_url>
   cd code_analysis
   ```

2. **Configure Poetry for a Local Virtual Environment:**

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. **Install Dependencies:**

   ```bash
   poetry install
   ```

4. **Run the Service Locally:**

   ```bash
   poetry run uvicorn app.main:app --reload --port 8001
   ```

5. **Access the API Docs:**

   Open your browser at [http://localhost:8001/docs](http://localhost:8001/docs) to interact with the API using Swagger UI.

### Docker Setup

1. **Build the Docker Image:**

   From the `code_analysis` directory:

   ```bash
   docker build -t code_analysis_service .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -p 8001:8001 code_analysis_service
   ```


## API Endpoints

### POST `/analyze/start`

Starts a background job to download a GitHub repository.

- **Request:**

  ```json
  {
    "repo_url": "https://github.com/example/repo"
  }
  ```

- **Response:**

  ```json
  {
    "job_id": "abc123"
  }
  ```

### POST `/analyze/function`

Extracts a function from the downloaded repository and sends it to the LLM Service for analysis.

- **Request:**

  ```json
  {
    "job_id": "abc123",
    "function_name": "module_name.function"
  }
  ```

- **Response:**

  ```json
  {
    "suggestions": [
      "Consider adding type hints.",
      "Add a docstring for better documentation."
    ]
  }
  ```

## Testing

- **Interactive Testing:**  
  Use [Swagger UI](http://localhost:8001/docs) to test endpoints interactively.


## Code Quality

This project uses several tools for code quality:

- **Pylint, Mypy, and Ruff:**  
  For linting, type checking, and formatting.
- **Nox:**  
  For automating quality checks and testing tasks.

