# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import pytest
import mock

from jira_link_telegram_bot import compose_message

@pytest.mark.parametrize('message, expected_result', [
    ([('ITS-1418', 'https://jira.example.org/browse/ITS-1418', 'Write a bot')], '[ITS-1418](https://jira.example.org/browse/ITS-1418) "Write a bot"')
])
def test_compose_message(message, expected_result):
    result = compose_message(message)
    assert result == expected_result
