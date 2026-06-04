from types import TracebackType
from typing import cast

from speech_recognition import AudioData, Microphone, Recognizer, RequestError, UnknownValueError


async def gather_command() -> str:
    return "Tell me something about the world war 2"


class Gatherer:
    def __init__(self, device_index: int | None = None):
        self.recognizer = Recognizer()
        self.microphone = Microphone(device_index=device_index)

    def __enter__(self) -> "Gatherer":
        self.microphone.__enter__()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.microphone.__exit__(exc_type, exc_value, traceback)

    def listen(self) -> str:
        print("Listening...")
        audio = self.recognizer.listen(self.microphone)

        try:
            print("Recognizing...")
            text = cast(str, self.recognizer.recognize_google(audio, language='pl-PL'))
            print(f"User said: {text}\n")

        except Exception as e:
            print("Say that again please...")
            return "None"
        return text
