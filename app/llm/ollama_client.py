import os

import requests
from dotenv import load_dotenv

from app.logger import logger


load_dotenv()


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL_NAME = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


def generate_response(prompt: str) -> str:
    """Send a prompt to the locally running Ollama model."""

    logger.info(
        "Sending request to Ollama model: %s",
        MODEL_NAME
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        logger.info(
            "Ollama response received successfully"
        )

        return result["response"]

    except requests.RequestException as error:

        logger.error(
            "Ollama request failed: %s",
            error
        )

        raise