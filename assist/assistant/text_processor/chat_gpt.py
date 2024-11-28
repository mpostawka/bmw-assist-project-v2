

from openai import AsyncOpenAI


class ChatGPT():
    def __init__(self):
        self.client = AsyncOpenAI()

    async def ask(self, prompt, text_queue):
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        buffer = ''
        async for chunk in response:
            content = chunk.choices[0].delta.content or ""
            if content:
                buffer += content
                # Check if buffer contains a sentence terminator
                while any(p in buffer for p in '.!?'):
                    # Split at the first sentence terminator
                    for i, c in enumerate(buffer):
                        if c in '.!?':
                            sentence = buffer[:i+1].strip()
                            buffer = buffer[i+1:].strip()
                            await text_queue.put(sentence)
                            break
        # Put any remaining text in the buffer
        if buffer:
            await text_queue.put(buffer)
        # Signal completion
        await text_queue.put(None)