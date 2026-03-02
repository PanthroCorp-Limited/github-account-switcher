# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for gh-switcher (Windows, onedir, windowed).

Run from project root:
    pyinstaller packaging/gh-switcher.spec
"""
from __future__ import annotations

import os

# SPEC is a PyInstaller builtin: absolute path to this .spec file.
_SPEC_DIR = os.path.dirname(SPEC)
_PROJECT_ROOT = os.path.normpath(os.path.join(_SPEC_DIR, os.pardir))
_ENTRY_POINT = os.path.join(_PROJECT_ROOT, "src", "gh_switcher", "__main__.py")

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
a = Analysis(
    [_ENTRY_POINT],
    pathex=[os.path.join(_PROJECT_ROOT, "src")],
    binaries=[],
    datas=[],
    hiddenimports=[
        # pystray Windows backend (conditionally imported, not auto-detected)
        "pystray._win32",
        # Pillow image plugins used at runtime
        "PIL.Image",
        "PIL.ImageDraw",
        "PIL.ImageFont",
        "PIL.PngImagePlugin",
        # plyer is optionally imported for Windows desktop notifications
        "plyer.platforms.win.notification",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Linux GTK / XApp tray backend -- not needed on Windows
        "gi",
        "gi.repository",
        "gtk",
        "xapp",
        "gh_switcher.tray.xapp",
        # Linux-only notification helper
        "dbus",
        # Test / dev tooling that may leak in
        "pytest",
        "ruff",
        "black",
        "mypy",
    ],
    noarchive=False,
)

# ---------------------------------------------------------------------------
# PYZ (compressed archive of pure-Python modules)
# ---------------------------------------------------------------------------
pyz = PYZ(a.pure)

# ---------------------------------------------------------------------------
# EXE
# ---------------------------------------------------------------------------
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # required for onedir (COLLECT handles binaries)
    name="gh-switcher",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # --windowed: no console window for a tray app
    disable_windowed_traceback=False,
)

# ---------------------------------------------------------------------------
# COLLECT (onedir output)
# ---------------------------------------------------------------------------
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="gh-switcher",
)
