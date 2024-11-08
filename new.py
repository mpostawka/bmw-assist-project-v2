import asyncio
from openai import AsyncStream

class VoiceStream:
    pass

async def button() -> str:
    pass

async def read_voice() -> VoiceStream:
    pass

async def parse_voice_stream(voice_stream: VoiceStream) -> str:
    pass

async def ask_gpt(text: str) -> AsyncStream:
    pass

async def speak(text_stream: AsyncStream) -> None:
    pass


async def main():
    button_status = await button()
    if button_status == "pressed":
        voice_stream = await read_voice()
        text = await parse_voice_stream(voice_stream)
        response_stream = await ask_gpt(text)
        await speak(response_stream)
    