from abc import ABC, abstractmethod

from assistant.types import TextQueue


class TextProcessor(ABC):
    @abstractmethod
    async def ask(self, prompt: str, text_queue: TextQueue) -> None:
        """
        Send a prompt to the model and handle the streamed response.

        Args:
            prompt (str): The input text prompt.
            text_queue (TextQueue): A queue to handle the streamed response.
        """
        pass
