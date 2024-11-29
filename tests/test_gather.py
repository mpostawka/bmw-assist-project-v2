import pytest

from assist.gather import gather_command


@pytest.mark.asyncio
async def test_gather_command() -> None:
    command = await gather_command()
    assert command == "Tell me something about the world war 2"
