# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import pytest
import mock

import settings
settings.JIRA_URL = "https://jira.example.org"

from jira_link_telegram_bot import extract_jira_issues

@mock.patch('jira_link_telegram_bot.get_jira_issue_caption', mock.MagicMock(return_value='Description'))
@pytest.mark.parametrize('message, expected_result', [
    ('https://jira.example.org/browse/ITS-1418', [('ITS-1418', 'https://jira.example.org/browse/ITS-1418', 'Description')]),
    ('https://jira.example.org/browse/ITS-1418 https://jira.example.org/browse/ITS-1419', [
        ('ITS-1418', 'https://jira.example.org/browse/ITS-1418', 'Description'),
        ('ITS-1419', 'https://jira.example.org/browse/ITS-1419', 'Description')
    ])
])
def test_extract_jira_issues(message, expected_result):
    result = extract_jira_issues(None, message)
    assert result == expected_result
