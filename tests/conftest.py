from __future__ import annotations

from pathlib import Path

import pytest

import gh_switcher.accounts as accounts_mod
import gh_switcher.config as config_mod


@pytest.fixture()
def tmp_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect all home-based paths to a temporary directory.

    Patches the module-level path constants that are evaluated at import time
    so that tests never touch the real filesystem.
    """
    monkeypatch.setenv("HOME", str(tmp_path))

    # accounts.py — hosts file read by the gh CLI
    hosts_file = tmp_path / ".config" / "gh" / "hosts.yml"
    monkeypatch.setattr(accounts_mod, "HOSTS_FILE", hosts_file)

    # config.py — gh-switcher's own configuration directory and file
    config_dir = tmp_path / ".config" / "gh-switcher"
    accounts_file = config_dir / "accounts.toml"
    monkeypatch.setattr(config_mod, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(config_mod, "ACCOUNTS_FILE", accounts_file)

    return tmp_path
