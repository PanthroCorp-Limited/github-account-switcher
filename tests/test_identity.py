from __future__ import annotations

import subprocess
from unittest.mock import MagicMock

import pytest

from gh_switcher.identity import GitIdentity, get_current, set_identity

GIT_CONFIG_NAME_ARGS = ["git", "config", "--global", "user.name"]
GIT_CONFIG_EMAIL_ARGS = ["git", "config", "--global", "user.email"]


class TestGetCurrent:
    def test_calls_git_config_twice(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """get_current() must invoke git config for both user.name and user.email."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=[],
                returncode=0,
                stdout="value\n",
                stderr="",
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        get_current()

        assert mock_run.call_count == 2

    def test_calls_correct_git_keys(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The two calls must request user.name and user.email respectively."""
        calls_made: list[list[str]] = []

        def fake_run(
            args: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess[str]:
            calls_made.append(args)
            return subprocess.CompletedProcess(
                args=args, returncode=0, stdout="value\n", stderr=""
            )

        monkeypatch.setattr(subprocess, "run", fake_run)

        get_current()

        assert calls_made[0] == GIT_CONFIG_NAME_ARGS
        assert calls_made[1] == GIT_CONFIG_EMAIL_ARGS

    def test_strips_whitespace(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Trailing newlines and whitespace are stripped from git output."""
        responses = iter(["Alice\n", "alice@example.com\n"])

        def fake_run(
            args: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(
                args=args, returncode=0, stdout=next(responses), stderr=""
            )

        monkeypatch.setattr(subprocess, "run", fake_run)

        result = get_current()

        assert result == GitIdentity(name="Alice", email="alice@example.com")


class TestSetIdentity:
    def test_calls_git_config_twice(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """set_identity() must invoke git config for both name and email."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=[], returncode=0, stdout="", stderr=""
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        set_identity("Alice", "alice@example.com")

        assert mock_run.call_count == 2

    def test_calls_with_check_true(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Both subprocess.run calls must use check=True."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=[], returncode=0, stdout="", stderr=""
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        set_identity("Alice", "alice@example.com")

        for c in mock_run.call_args_list:
            assert c[1].get("check") is True

    def test_calls_correct_args(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verifies the exact argument lists for both git config calls."""
        mock_run = MagicMock(
            return_value=subprocess.CompletedProcess(
                args=[], returncode=0, stdout="", stderr=""
            )
        )
        monkeypatch.setattr(subprocess, "run", mock_run)

        set_identity("Alice", "alice@example.com")

        expected_name_args = GIT_CONFIG_NAME_ARGS + ["Alice"]
        expected_email_args = GIT_CONFIG_EMAIL_ARGS + ["alice@example.com"]

        actual_calls = [c[0][0] for c in mock_run.call_args_list]
        assert actual_calls[0] == expected_name_args
        assert actual_calls[1] == expected_email_args
