from __future__ import annotations

import subprocess
from unittest.mock import MagicMock

import pytest

from gh_switcher.switcher import SwitchError, run_switch

EXPECTED_ARGS = [
    "gh",
    "auth",
    "switch",
    "--hostname",
    "github.com",
    "--user",
    "alice",
]


class TestRunSwitch:
    def test_calls_gh_with_correct_args(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verifies the exact argument list passed to subprocess.run."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=EXPECTED_ARGS,
                returncode=0,
                stdout="",
                stderr="",
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        run_switch("alice")

        mock_run.assert_called_once()
        actual_args = mock_run.call_args[0][0]
        assert actual_args == EXPECTED_ARGS

    def test_passes_capture_output(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verifies that capture_output and text flags are set."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=EXPECTED_ARGS,
                returncode=0,
                stdout="",
                stderr="",
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        run_switch("alice")

        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["capture_output"] is True
        assert call_kwargs["text"] is True

    def test_raises_switch_error_on_nonzero(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """SwitchError is raised with stderr content when gh exits non-zero."""
        error_message = "auth failed"
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=EXPECTED_ARGS,
                returncode=1,
                stdout="",
                stderr=error_message,
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        with pytest.raises(SwitchError, match=error_message):
            run_switch("alice")

    def test_success_does_not_raise(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """No exception is raised on a zero return code."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=EXPECTED_ARGS,
                returncode=0,
                stdout="",
                stderr="",
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        # Should complete without raising
        run_switch("alice")
