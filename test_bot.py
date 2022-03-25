import json
import pytest
import bot


@pytest.fixture
def lab():
    test_lab_url = "https://test.net"
    return bot.Lab(test_lab_url)


@pytest.fixture
def test_bot(lab):
    test_bot_name = "Test"
    test_msg_help = "@bot /help"
    return bot.Bot(test_bot_name, lab, test_msg_help)


def test_bot_help(test_bot):
    assert test_bot.respond() == "Hi! I'm Test bot. Supported commands: /status /reset"


def test_bot_not_implemented(test_bot):
    test_bot.msg = "@bot /command"
    assert test_bot.respond() == "Command not implemented."


def test_bot_lab_reset(test_bot):
    test_bot.msg = "@bot /reset"
    assert test_bot.respond() == json.dumps({"state": "default"})
