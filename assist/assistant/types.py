import asyncio

from pydub import AudioSegment

TextQueue = asyncio.Queue[str | None]
AudioQueue = asyncio.Queue[AudioSegment | None]
