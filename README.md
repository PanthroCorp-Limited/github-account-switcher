# github-account-switcher

A lightweight system tray app for switching between multiple GitHub accounts (`gh` CLI) with a single click. Each account can carry its own git identity (name + email), which is applied automatically on switch.

## Platform support

| Platform                              | Status       |
|---------------------------------------|--------------|
| Linux (X11, XApp-compatible desktop)  | ✓ Supported  |
| macOS                                 | Coming soon  |
| Windows                               | Coming soon  |

## Features

- System tray icon showing the active account's initials
- One-click account switching via `gh auth switch`
- Per-account git identity (`user.name` / `user.email`) applied on switch
- First-run auto-populates config from current `git config --global`
- Start on login (XDG autostart)

## Requirements

- Ubuntu 24.04+ / Debian 12+ (Python 3.12 required)
- [`gh` CLI](https://cli.github.com/) with at least one authenticated account
- System packages: `gir1.2-xapp-1.0`, `python3-gi`, `python3-gi-cairo`

## Installation

### From a release `.deb` (recommended)

Download the `.deb` from the [latest release](https://github.com/panthrocorp/github-account-switcher/releases/latest) and install with:

```bash
sudo apt install ./gh-switcher_<version>_amd64.deb
```

`apt` resolves the system package dependencies automatically. After installation, `gh-switcher` is available on your `PATH`.

### via curl

One-line install — fetches and runs the installer script:

```bash
curl -fsSL https://raw.githubusercontent.com/panthrocorp/github-account-switcher/main/install.sh | bash
```

Installs to `~/.local/share/gh-switcher` and links the binary to `~/.local/bin/gh-switcher`. Re-running upgrades to the latest release.

### via pip

For users who prefer full control over the install. Because `python3-gi` and `gir1.2-xapp-1.0` are system packages not available on PyPI, a plain `pip3 install gh-switcher` will fail at runtime. Use a venv with `--system-site-packages` instead:

```bash
# System deps (once)
sudo apt-get install -y gir1.2-xapp-1.0 python3-gi python3-gi-cairo

# Create an isolated venv that can see the system GTK bindings
python3 -m venv --system-site-packages ~/.local/share/gh-switcher
~/.local/share/gh-switcher/bin/pip install gh-switcher
ln -sf ~/.local/share/gh-switcher/bin/gh-switcher ~/.local/bin/gh-switcher
```

### From source

```bash
# Install system dependencies
sudo apt-get install -y gir1.2-xapp-1.0 python3-gi python3-gi-cairo

# Clone and install
git clone https://github.com/panthrocorp/github-account-switcher.git
cd github-account-switcher
make install
```

Run it:

```bash
.venv/bin/gh-switcher
```

> The venv is created with `--system-site-packages` so the GTK/XApp bindings (system packages) are accessible.

## Usage

Launch `gh-switcher` — the tray icon appears in your system tray. Left-click (or right-click) to open the menu:

```text
✓  alice
   alice-work
──────────────────
Refresh
Configure accounts...
Start on Login [ ]
──────────────────
Quit
```

Toggle **Start on Login** to add or remove the XDG autostart entry (`~/.config/autostart/gh-switcher.desktop`).

## Configuration

On first run, `~/.config/gh-switcher/accounts.toml` is created automatically. The active account is populated from your current `git config --global`; other accounts get stub entries to fill in:

```toml
[alice]
name = "Alice Smith"
email = "alice@example.com"

[alice-work]
name = "Alice Smith (Work)"
email = "alice@work.example.com (set me)"
```

Click **Configure accounts...** in the tray menu to open the file in your default editor.

## Development

```bash
make lint       # ruff check src/ tests/
make format     # ruff format src/ tests/
make test       # pytest + bats (test-py + test-bash)
make test-py    # pytest unit tests only
make test-bash  # bats shell tests only (install.sh)
```

## Releasing

Releases are driven by [semantic-release](https://semantic-release.gitbook.io/) via GitHub Actions on push to `main`. Commit messages must follow the convention:

| Prefix       | Release |
|--------------|---------|
| `fix:`       | patch   |
| `feat:`      | minor   |
| `breaking:`  | major   |

## Licence

[MIT](LICENSE)
