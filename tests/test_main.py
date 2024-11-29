from unittest.mock import AsyncMock, patch

import pytest

from assist.main import main


@pytest.mark.asyncio
async def test_main() -> None:
    with patch("assist.main.gather_command", new_callable=AsyncMock) as mock_gather_command, patch(
        "assist.main.Assistant", autospec=True
    ) as mock_assistant_class:

        mock_gather_command.side_effect = ["command1", "command2", "command3"]
        mock_assistant = mock_assistant_class.return_value
        mock_assistant.respond = AsyncMock()

        await main()

        assert mock_gather_command.call_count == 3
        assert mock_assistant.respond.call_count == 3
