"""
Module: analyze
This module implements the Code Analysis Service endpoints.
It handles asynchronous Git repository cloning and function extraction,
and communicates with the LLM Service for function analysis.
"""

import os
import uuid
import tempfile
import re
import logging
from typing import Dict

import git
import requests
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

router = APIRouter()
logging.basicConfig(level=logging.INFO)

# In-memory store for job_id -> repository path.
JOBS: Dict[str, str] = {}


class RepoInput(BaseModel):
    """Input model for starting analysis (repository URL)."""

    repo_url: str


class FunctionAnalysisInput(BaseModel):
    """Input model for function analysis with job ID and function name."""

    job_id: str
    function_name: str


def download_repo(repo_url: str, job_id: str) -> None:
    """
    Downloads a Git repository to a temporary location.

    Args:
        repo_url (str): The URL of the repository.
        job_id (str): Unique identifier for the job.

    Raises:
        Exception: If cloning the repository fails.
    """
    repo_path = os.path.join(tempfile.gettempdir(), job_id)
    try:
        git.Repo.clone_from(repo_url, repo_path)
        JOBS[job_id] = repo_path
        logging.info("Repository cloned for job %s at %s", job_id, repo_path)
    except Exception as e:
        logging.error("Failed to clone repository for job %s: %s", job_id, str(e))
        JOBS.pop(job_id, None)
        raise Exception(f"Failed to clone repo: {str(e)}") from e


@router.post("/analyze/start")
def start_analysis(
    data: RepoInput, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """
    Starts a background job to download a GitHub repository.
    Returns a job_id for later reference.

    Args:
        data (RepoInput): The input containing the repository URL.
        background_tasks (BackgroundTasks): FastAPI background task manager.

    Returns:
        dict: A dictionary containing the job_id.
    """
    job_id = str(uuid.uuid4())
    background_tasks.add_task(download_repo, data.repo_url, job_id)
    return {"job_id": job_id}


def extract_function_code(repo_path: str, function_name: str) -> str:
    """
    Extracts the function code from a repository.

    Assumes function_name is in the format "module_name.function".

    Args:
        repo_path (str): Path to the cloned repository.
        function_name (str): The target function in "module_name.function" format.

    Returns:
        str: The extracted function code.

    Raises:
        HTTPException: If the module or function cannot be found.
    """
    try:
        module_name, func_name = function_name.split(".")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="function_name must be in the format 'module_name.function'",
        )

    file_path = os.path.join(repo_path, f"{module_name}.py")
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Module file {module_name}.py not found in repository.",
        )

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = rf"def\s+{func_name}\s*\(.*?\):(?:\n\s+.*)+"
    match = re.search(pattern, content)
    if not match:
        raise HTTPException(
            status_code=404,
            detail=f"Function {func_name} not found in {module_name}.py",
        )
    return match.group(0)


@router.post("/analyze/function")
def analyze_function(data: FunctionAnalysisInput) -> dict:
    """
    Analyzes a function from a previously downloaded repository.
    Extracts the function code and sends it to the LLM Service for analysis.

    Args:
        data (FunctionAnalysisInput): Input containing job_id and function name.

    Returns:
        dict: The LLM Service response containing suggestions.
    """
    job_id = data.job_id
    if job_id not in JOBS:
        raise HTTPException(
            status_code=404, detail="Invalid job_id or job not completed yet."
        )
    repo_path = JOBS[job_id]

    try:
        function_code = extract_function_code(repo_path, data.function_name)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error extracting function code: {str(e)}"
        ) from e

    llm_service_url = os.getenv("LLM_SERVICE_URL", "http://localhost:8000/analyze")
    try:
        response = requests.post(
            llm_service_url,
            json={"function_code": function_code},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calling LLM Service: {str(e)}"
        ) from e
