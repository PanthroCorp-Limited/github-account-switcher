from __future__ import annotations

from pathlib import Path

from gh_switcher.accounts import GhAccount, active_account, load_accounts

# -- sample YAML content --------------------------------------------------

HOSTS_YAML_TWO_USERS = """\
github.com:
  user: alice
  users:
    alice:
      oauth_token: tok1
    bob:
      oauth_token: tok2
"""

HOSTS_YAML_NO_ACTIVE = """\
github.com:
  users:
    alice:
      oauth_token: tok1
    bob:
      oauth_token: tok2
"""


def _write_hosts(tmp_home: Path, content: str) -> None:
    """Write YAML content to the monkeypatched hosts file location."""
    from gh_switcher import accounts as accounts_mod

    hosts_file: Path = accounts_mod.HOSTS_FILE
    hosts_file.parent.mkdir(parents=True, exist_ok=True)
    hosts_file.write_text(content, encoding="utf-8")


# -- load_accounts ---------------------------------------------------------


class TestLoadAccounts:
    def test_missing_file(self, tmp_home: Path) -> None:
        """Returns an empty list when the hosts file does not exist."""
        result = load_accounts()
        assert result == []

    def test_empty_yaml(self, tmp_home: Path) -> None:
        """Returns an empty list when the hosts file is empty."""
        _write_hosts(tmp_home, "")
        result = load_accounts()
        assert result == []

    def test_returns_all_accounts(self, tmp_home: Path) -> None:
        """All users present in the YAML are returned as GhAccount objects."""
        _write_hosts(tmp_home, HOSTS_YAML_TWO_USERS)
        result = load_accounts()
        usernames = {a.username for a in result}
        assert usernames == {"alice", "bob"}
        assert len(result) == 2

    def test_marks_active(self, tmp_home: Path) -> None:
        """The user matching 'github.com.user' is flagged as active."""
        _write_hosts(tmp_home, HOSTS_YAML_TWO_USERS)
        result = load_accounts()
        by_name = {a.username: a for a in result}
        assert by_name["alice"].active is True
        assert by_name["bob"].active is False

    def test_no_active_user_key(self, tmp_home: Path) -> None:
        """When no 'user' key is present, no account is marked active."""
        _write_hosts(tmp_home, HOSTS_YAML_NO_ACTIVE)
        result = load_accounts()
        assert all(not a.active for a in result)


# -- active_account --------------------------------------------------------


class TestActiveAccount:
    def test_returns_none_on_empty(self) -> None:
        """Returns None for an empty account list."""
        assert active_account([]) is None

    def test_returns_active(self) -> None:
        """Returns the account with active=True."""
        accounts = [
            GhAccount(username="alice", active=True),
            GhAccount(username="bob", active=False),
        ]
        result = active_account(accounts)
        assert result is not None
        assert result.username == "alice"
        assert result.active is True

    def test_returns_none_when_none_active(self) -> None:
        """Returns None when no account is marked active."""
        accounts = [
            GhAccount(username="alice", active=False),
            GhAccount(username="bob", active=False),
        ]
        assert active_account(accounts) is None
