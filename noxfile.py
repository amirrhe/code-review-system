import nox

PYTHON_VERSIONS = ["3.10"]

CODE_ANALYSIS_PATH = "code_analysis"
LLM_SERVICE_PATH = "llm_service"


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """
    Run linting (using ruff and pylint) for both microservices.
    """
    session.run("poetry", "run", "ruff", "check", CODE_ANALYSIS_PATH)
    session.run("poetry", "run", "ruff", "check", LLM_SERVICE_PATH)
    session.run("poetry", "run", "mypy", CODE_ANALYSIS_PATH)
    session.run("poetry", "run", "mypy", LLM_SERVICE_PATH)
    session.run("poetry", "run", "pylint", f"{CODE_ANALYSIS_PATH}/app")
    session.run("poetry", "run", "pylint", f"{LLM_SERVICE_PATH}/app")


@nox.session(python=PYTHON_VERSIONS)
def format(session):
    """
    Run code formatter (using ruff's format command) for both microservices.
    """
    session.run("poetry", "run", "ruff", "format", CODE_ANALYSIS_PATH)
    session.run("poetry", "run", "ruff", "format", LLM_SERVICE_PATH)
