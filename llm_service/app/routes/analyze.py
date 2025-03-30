"""
Module: analyze
This module defines the API endpoint for analyzing function code using
different LLM providers. It uses a Strategy Pattern to decouple provider-specific logic.
"""

import os
from abc import ABC, abstractmethod

from fastapi import APIRouter, HTTPException
from ollama import generate
from pydantic import BaseModel

router = APIRouter()


class FunctionCode(BaseModel):
    """
    Pydantic model for function code input.
    """

    function_code: str


class BaseLLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    def analyze(self, function_code: str) -> dict:
        """
        Analyze the given function code and return suggestions.
        """
        ...


class LocalLLMProvider(BaseLLMProvider):
    """
    Local LLM provider using the Ollama package.
    """

    def analyze(self, function_code: str) -> dict:
        try:
            result = generate("qwen2.5-coder:1.5b", function_code)
            return {"suggestions": [result["response"]]}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Local LLM error: {str(e)}"
            ) from e


class OpenAILLMProvider(BaseLLMProvider):
    """
    Stub implementation for the OpenAI LLM provider.
    """

    def analyze(self, function_code: str) -> dict:
        raise HTTPException(status_code=501, detail="OpenAI provider not implemented.")


class DeepSeekLLMProvider(BaseLLMProvider):
    """
    Stub implementation for the DeepSeek LLM provider.
    """

    def analyze(self, function_code: str) -> dict:
        raise HTTPException(
            status_code=501, detail="DeepSeek provider not implemented."
        )


class LLMProviderFactory:
    """
    Factory class to return the appropriate LLM provider based on the provider name.
    """

    @staticmethod
    def get_provider(provider_name: str) -> BaseLLMProvider:
        if provider_name == "local":
            return LocalLLMProvider()
        if provider_name == "openai":
            return OpenAILLMProvider()
        if provider_name == "deepseek":
            return DeepSeekLLMProvider()
        raise HTTPException(status_code=400, detail="Unsupported LLM_PROVIDER value")


@router.post("/analyze")
def analyze_function(data: FunctionCode):
    """
    Analyze the function code using the selected LLM provider.
    """
    provider_name = os.getenv("LLM_PROVIDER", "local").lower()
    provider = LLMProviderFactory.get_provider(provider_name)
    return provider.analyze(data.function_code)
