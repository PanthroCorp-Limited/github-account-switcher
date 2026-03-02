from __future__ import annotations

import importlib.metadata


def test_entry_point_registered() -> None:
    """Console script 'gh-switcher' must be discoverable via entry points."""
    eps = importlib.metadata.entry_points(group="console_scripts")
    names = [ep.name for ep in eps]
    assert "gh-switcher" in names


def test_version_is_set() -> None:
    """Package version must be a non-empty string."""
    version = importlib.metadata.version("gh-switcher")
    assert isinstance(version, str)
    assert len(version) > 0


def test_core_modules_importable_without_gtk() -> None:
    """Core modules must not pull in GTK/gi at import time.

    This guards against accidentally importing system-only packages at
    module level, which would break CI environments.
    """
    # These imports must succeed without python3-gi installed.
    from gh_switcher import accounts  # noqa: F401
    from gh_switcher import config  # noqa: F401
    from gh_switcher import identity  # noqa: F401
    from gh_switcher import switcher  # noqa: F401
