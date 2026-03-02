from __future__ import annotations

import tomllib
from pathlib import Path

from gh_switcher import config as config_mod
from gh_switcher.accounts import GhAccount
from gh_switcher.config import ensure_exists, get_identity
from gh_switcher.identity import GitIdentity

# -- sample TOML content ---------------------------------------------------

ACCOUNTS_TOML_FULL = """\
[alice]
name = "Alice Smith"
email = "alice@example.com"

[bob]
name = "Bob Jones"
email = "bob@example.com"
"""

ACCOUNTS_TOML_INCOMPLETE = """\
[alice]
name = ""
email = "alice@example.com"
"""

ACCOUNTS_TOML_MISSING_EMAIL = """\
[alice]
name = "Alice Smith"
email = ""
"""


def _write_accounts_toml(content: str) -> None:
    """Write TOML content to the monkeypatched accounts file."""
    accounts_file: Path = config_mod.ACCOUNTS_FILE
    accounts_file.parent.mkdir(parents=True, exist_ok=True)
    accounts_file.write_text(content, encoding="utf-8")


# -- get_identity ----------------------------------------------------------


class TestGetIdentity:
    def test_missing_file(self, tmp_home: Path) -> None:
        """Returns None when accounts.toml does not exist."""
        assert get_identity("alice") is None

    def test_missing_username(self, tmp_home: Path) -> None:
        """Returns None when the requested username is not in the file."""
        _write_accounts_toml(ACCOUNTS_TOML_FULL)
        assert get_identity("charlie") is None

    def test_incomplete_entry_blank_name(self, tmp_home: Path) -> None:
        """Returns None when the name field is blank."""
        _write_accounts_toml(ACCOUNTS_TOML_INCOMPLETE)
        assert get_identity("alice") is None

    def test_incomplete_entry_blank_email(self, tmp_home: Path) -> None:
        """Returns None when the email field is blank."""
        _write_accounts_toml(ACCOUNTS_TOML_MISSING_EMAIL)
        assert get_identity("alice") is None

    def test_returns_identity(self, tmp_home: Path) -> None:
        """Returns a GitIdentity with the correct name and email."""
        _write_accounts_toml(ACCOUNTS_TOML_FULL)
        result = get_identity("alice")
        assert result == GitIdentity(name="Alice Smith", email="alice@example.com")


# -- ensure_exists ---------------------------------------------------------


class TestEnsureExists:
    def test_creates_file(self, tmp_home: Path) -> None:
        """Creates accounts.toml with the active account's identity."""
        accounts = [
            GhAccount(username="alice", active=True),
            GhAccount(username="bob", active=False),
        ]
        identity = GitIdentity(name="Alice Smith", email="alice@example.com")

        ensure_exists(accounts, identity)

        accounts_file: Path = config_mod.ACCOUNTS_FILE
        assert accounts_file.exists()

        with accounts_file.open("rb") as fh:
            data = tomllib.load(fh)

        assert data["alice"]["name"] == "Alice Smith"
        assert data["alice"]["email"] == "alice@example.com"

    def test_stubs_inactive_accounts(self, tmp_home: Path) -> None:
        """Inactive accounts receive placeholder values containing '(set me)'."""
        accounts = [
            GhAccount(username="alice", active=True),
            GhAccount(username="bob", active=False),
        ]
        identity = GitIdentity(name="Alice Smith", email="alice@example.com")

        ensure_exists(accounts, identity)

        accounts_file: Path = config_mod.ACCOUNTS_FILE
        with accounts_file.open("rb") as fh:
            data = tomllib.load(fh)

        assert "(set me)" in data["bob"]["name"]
        assert "(set me)" in data["bob"]["email"]

    def test_noop_if_file_exists(self, tmp_home: Path) -> None:
        """Does not overwrite an existing accounts.toml."""
        existing_content = ACCOUNTS_TOML_FULL
        _write_accounts_toml(existing_content)

        accounts_file: Path = config_mod.ACCOUNTS_FILE
        mtime_before = accounts_file.stat().st_mtime

        accounts = [GhAccount(username="alice", active=True)]
        identity = GitIdentity(name="New Name", email="new@example.com")

        ensure_exists(accounts, identity)

        # Content must be unchanged
        assert accounts_file.read_text(encoding="utf-8") == existing_content
        assert accounts_file.stat().st_mtime == mtime_before

    def test_write_produces_valid_toml(self, tmp_home: Path) -> None:
        """The generated accounts.toml round-trips through tomllib cleanly."""
        accounts = [
            GhAccount(username="alice", active=True),
            GhAccount(username="bob", active=False),
        ]
        identity = GitIdentity(name="Alice Smith", email="alice@example.com")

        ensure_exists(accounts, identity)

        accounts_file: Path = config_mod.ACCOUNTS_FILE
        with accounts_file.open("rb") as fh:
            data = tomllib.load(fh)

        # Verify structure is a dict of dicts with string values
        assert isinstance(data, dict)
        for section_key, section_val in data.items():
            assert isinstance(section_key, str)
            assert isinstance(section_val, dict)
            for field_key, field_val in section_val.items():
                assert isinstance(field_key, str)
                assert isinstance(field_val, str)
