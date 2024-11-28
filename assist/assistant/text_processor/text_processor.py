import asyncio
from abc import ABC, abstractmethod


class TextProcessor(ABC):
    @abstractmethod
    async def ask(self, prompt: str, text_queue: asyncio.Queue[str | None]) -> None:
        """
        Send a prompt to the model and handle the streamed response.

        Args:
            prompt (str): The input text prompt.
            text_queue (asyncio.Queue[str | None]): A queue to handle the streamed response.
        """
        pass
