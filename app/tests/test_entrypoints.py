from unittest.mock import patch

from app.interfaces.cli import main as cli_module
from app.services.api import main as api_main
from app.services.reconciler import main as reconciler_module
from app.services.strategy_runner import main as runner_module


def test_cli_main_logs_startup() -> None:
    with patch.object(cli_module.logger, "info") as mocked_info:
        cli_module.main()

    mocked_info.assert_called_once_with("cli.startup")


def test_strategy_runner_logs_startup() -> None:
    with patch.object(runner_module.logger, "info") as mocked_info:
        runner_module.run()

    mocked_info.assert_called_once_with("strategy_runner.startup")


def test_reconciler_logs_startup() -> None:
    with patch.object(reconciler_module.logger, "info") as mocked_info:
        reconciler_module.run()

    mocked_info.assert_called_once_with("reconciler.startup")


def test_api_run_invokes_uvicorn() -> None:
    with patch("uvicorn.run") as mocked_run:
        api_main.run()

    mocked_run.assert_called_once_with(
        "app.services.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1,
    )
