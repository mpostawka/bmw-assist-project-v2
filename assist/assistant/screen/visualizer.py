import asyncio

from pydub import AudioSegment

from .driver import Screen


class Visualizer:
    OFFSETS = (4, 0, 4)
    WINDOW_MS = 50

    def __init__(self, screen: Screen) -> None:
        self.screen = screen

    def render(self, fill: float) -> None:
        for x, offset in enumerate(self.OFFSETS):
            for height in range(10):
                lit = (height + offset) / 10 < fill
                for y in (9 - height, 10 + height):
                    self.screen.pixel(x, y).on() if lit else self.screen.pixel(x, y).off()

    async def show(self, segment: AudioSegment) -> None:
        for start in range(0, len(segment), self.WINDOW_MS):
            window = segment[start : start + self.WINDOW_MS]
            self.render(window.max / window.max_possible_amplitude)
            await asyncio.sleep(self.WINDOW_MS / 1000)
        self.screen.clear()
