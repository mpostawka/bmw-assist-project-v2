from unittest.mock import AsyncMock, patch

import pytest

from assist.main import main


@pytest.mark.asyncio
async def test_main() -> None:
    with patch("assist.main.Gatherer") as mock_Gatherer, patch(
        "assist.main.Assistant", autospec=True
    ) as mock_assistant_class:

        mock_gatherer_instance = mock_Gatherer.return_value.__enter__.return_value
        mock_gatherer_instance.listen.side_effect = ["command1", "command2", "command3"]
        mock_assistant = mock_assistant_class.return_value
        mock_assistant.respond = AsyncMock()

        await main()

        assert mock_gatherer_instance.listen.call_count == 3
        assert mock_assistant.respond.call_count == 3
