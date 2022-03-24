import json
import pytest
import app


@pytest.fixture
def lab():
    test_lab_url = "https://test.net"
    return app.Lab(test_lab_url)


@pytest.fixture
def bot(lab):
    test_bot_name = "Test"
    test_msg_help = "@bot /help"
    return app.Bot(test_bot_name, lab, test_msg_help)


def test_bot_help(bot):
    assert bot.respond() == "Hi! I'm Test bot. Supported commands: /status /reset"


def test_bot_not_implemented(bot):
    bot.msg = "@bot /command"
    assert bot.respond() == "Command not implemented."


def test_bot_lab_reset(bot):
    bot.msg = "@bot /reset"
    assert bot.respond() == json.dumps({"state": "default"})
