import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def gpt_answer(content):
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    return stream

async def main():
    stream = await gpt_answer("Say something 100x times")
    print(stream)
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
    print("", flush=True)


asyncio.run(main())