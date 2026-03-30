#!/usr/bin/env bash
# install.sh — gh-switcher installer
# Usage: curl -fsSL https://raw.githubusercontent.com/PanthroCorp-Limited/github-account-switcher/main/install.sh | bash
set -euo pipefail

VENV_DIR="${HOME}/.local/share/gh-switcher"
BIN_DIR="${HOME}/.local/bin"
BINARY="${BIN_DIR}/gh-switcher"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

info()    { printf '\033[1;34m[info]\033[0m  %s\n' "$*"; }
success() { printf '\033[1;32m[ok]\033[0m    %s\n' "$*"; }
warn()    { printf '\033[1;33m[warn]\033[0m  %s\n' "$*"; }
die()     { printf '\033[1;31m[error]\033[0m %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------------------

check_linux() {
    if [[ "$(uname -s)" != "Linux" ]]; then
        die "gh-switcher currently supports Linux only. Got: $(uname -s)"
    fi
}

check_python() {
    local python=""

    for candidate in python3.12 python3; do
        if command -v "${candidate}" &>/dev/null; then
            local ver
            ver=$("${candidate}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
            local major minor
            major="${ver%%.*}"
            minor="${ver##*.}"
            if (( major > 3 )) || (( major == 3 && minor >= 12 )); then
                python="${candidate}"
                break
            fi
        fi
    done

    if [[ -z "${python}" ]]; then
        die "Python 3.12+ is required but was not found. Install it with: sudo apt-get install python3.12"
    fi

    info "Using Python: $(command -v "${python}") (${ver})"
    PYTHON="${python}"
}

install_system_deps() {
    # Check if the GTK/XApp bindings are already importable
    if "${PYTHON}" -c "import gi; gi.require_version('XApp', '1.0'); from gi.repository import XApp" &>/dev/null 2>&1; then
        info "System GTK/XApp bindings already present — skipping apt install."
        return
    fi

    if command -v apt-get &>/dev/null; then
        info "Installing system dependencies via apt-get..."
        sudo apt-get install -y gir1.2-xapp-1.0 python3-gi python3-gi-cairo
    else
        warn "apt-get not found. Please install the GTK/XApp bindings manually:"
        warn "  gir1.2-xapp-1.0  python3-gi  python3-gi-cairo"
        warn "Continuing — the install may fail if bindings are absent."
    fi
}

create_venv() {
    if [[ -d "${VENV_DIR}" ]]; then
        info "Existing venv found at ${VENV_DIR} — will upgrade in place."
    else
        info "Creating venv at ${VENV_DIR}..."
        "${PYTHON}" -m venv --system-site-packages "${VENV_DIR}"
    fi
}

install_package() {
    info "Installing gh-switcher..."
    "${VENV_DIR}/bin/pip" install --quiet --upgrade gh-switcher
}

link_binary() {
    mkdir -p "${BIN_DIR}"
    ln -sf "${VENV_DIR}/bin/gh-switcher" "${BINARY}"
    info "Binary linked: ${BINARY} -> ${VENV_DIR}/bin/gh-switcher"
}

check_path() {
    case ":${PATH}:" in
        *":${BIN_DIR}:"*)
            : # already present
            ;;
        *)
            warn "${BIN_DIR} is not in your PATH."
            warn "Add this line to your shell profile (e.g. ~/.bashrc or ~/.profile):"
            warn "  export PATH=\"\${HOME}/.local/bin:\${PATH}\""
            ;;
    esac
}

print_success() {
    success "gh-switcher installed successfully."
    printf '\n  Run: gh-switcher\n\n'
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    check_linux
    check_python
    install_system_deps
    create_venv
    install_package
    link_binary
    check_path
    print_success
}

if [[ "${BASH_SOURCE[0]:-${0}}" == "${0}" ]]; then
    main "$@"
fi
