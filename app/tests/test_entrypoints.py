from unittest.mock import patch

from app.interfaces.cli.main import main as cli_main
from app.services.api import main as api_main
from app.services.reconciler.main import run as reconciler_run
from app.services.strategy_runner.main import run as runner_run


def test_cli_main_prints_placeholder(capsys) -> None:
    cli_main()
    captured = capsys.readouterr()
    assert "CLI placeholder" in captured.out


def test_strategy_runner_run_prints_placeholder(capsys) -> None:
    runner_run()
    captured = capsys.readouterr()
    assert "strategy-runner placeholder" in captured.out


def test_reconciler_run_prints_placeholder(capsys) -> None:
    reconciler_run()
    captured = capsys.readouterr()
    assert "reconciler placeholder" in captured.out


def test_api_run_invokes_uvicorn() -> None:
    with patch("uvicorn.run") as mocked_run:
        api_main.run()

    mocked_run.assert_called_once_with(
        "app.services.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
