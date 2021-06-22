# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import pytest
import mock

import settings
settings.JIRA_URL = "https://jira.example.org"

from jira_link_telegram_bot import extract_jira_issues

def mock_get_jira_link_and_caption(jira, tag):
    return ('https://jira.example.org/browse/%s' % tag, 'Description')

@mock.patch('jira_link_telegram_bot.get_jira_issue_link_and_caption', mock.MagicMock(side_effect=mock_get_jira_link_and_caption))
@pytest.mark.parametrize('message, expected_result', [
    ('https://jira.example.org/browse/ITS-1418', [('ITS-1418', 'https://jira.example.org/browse/ITS-1418', 'Description')]),
    ('https://jira.example.org/browse/ITS-1418 https://jira.example.org/browse/ITS-1419', [
        ('ITS-1418', 'https://jira.example.org/browse/ITS-1418', 'Description'),
        ('ITS-1419', 'https://jira.example.org/browse/ITS-1419', 'Description')
    ]),
    ('Text without any link in it', []),
    ('Text and link https://jira.example.org/browse/ABC-123', [('ABC-123', 'https://jira.example.org/browse/ABC-123', 'Description')]),
    ('Unknown jira https://jira.unknown.org/browse/ABC-145', []),
    ('Http ignored http://jira.example.org/browse/IT-123', []),
    ('Almost correct link https://jira.example.org/notbrowse/IT-456', []),
    ('(ITS-789) https://jira.example.org/browse/ITS-789', [('ITS-789', 'https://jira.example.org/browse/ITS-789', 'Description')]),
    ('ITS-789 dupe ITS-789 dupe https://jira.example.org/browse/ITS-789', [('ITS-789', 'https://jira.example.org/browse/ITS-789', 'Description')]),
    ('ITS-123', [('ITS-123', 'https://jira.example.org/browse/ITS-123', 'Description')]),
    ('Ends with ITS-0', [('ITS-0', 'https://jira.example.org/browse/ITS-0', 'Description')]),
    ('Issue ITS-1 in the middle', [('ITS-1', 'https://jira.example.org/browse/ITS-1', 'Description')]),
    ('Issue ITS-2\nITS-3 newline', [
        ('ITS-2', 'https://jira.example.org/browse/ITS-2', 'Description'),
        ('ITS-3', 'https://jira.example.org/browse/ITS-3', 'Description')
    ])
    
])
def test_extract_jira_issues(message, expected_result):
    result = extract_jira_issues(None, message)
    assert result == expected_result
