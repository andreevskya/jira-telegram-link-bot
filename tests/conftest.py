# -*- coding: utf-8 -*-
import sys, importlib

sys.path.append('../')

import jira_link_telegram_bot
import pytest
import settings

@pytest.fixture(autouse=True)
def before_and_after_test():
    print("\n".join(sys.modules))
    settings.JIRA_URL = "https://jira.example.org"
    if 'jira_link_telegram_bot' in sys.modules:
        importlib.reload(jira_link_telegram_bot)
