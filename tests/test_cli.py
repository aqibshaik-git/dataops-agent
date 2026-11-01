from pathlib import Path

from dataops_agent.cli import main
from tests.fakes import FakeClient

CONFIG = Path(__file__).resolve().parent.parent / "config.toml"


def test_cli_prints_answer_and_report(capsys):
    assert main(["hi", "--config", str(CONFIG)], client=FakeClient()) == 0
    out = capsys.readouterr().out
    assert out.startswith("Hello world")
    for label in ("input tokens : 12", "output tokens: 4", "stop reason  : end_turn", "cost         : $"):
        assert label in out


def test_cli_warns_when_cut_off(capsys):
    main(["hi", "--config", str(CONFIG), "--max-tokens", "4"], client=FakeClient(stop_reason="max_tokens"))
    assert "cut off" in capsys.readouterr().err
