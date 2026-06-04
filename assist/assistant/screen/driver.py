import ctypes
from pathlib import Path

_lib = ctypes.CDLL(str(Path(__file__).with_name("libscreen.so")))


class Pixel:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def on(self) -> None:
        _lib.screen_write(self.x, self.y, 255)

    def off(self) -> None:
        _lib.screen_write(self.x, self.y, 0)


class Screen:
    def __enter__(self) -> "Screen":
        _lib.screen_open()
        return self

    def __exit__(self, *_: object) -> None:
        _lib.screen_close()

    def pixel(self, x: int, y: int) -> Pixel:
        return Pixel(x, y)

    def clear(self) -> None:
        _lib.screen_clear()
