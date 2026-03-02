#!/usr/bin/env bash
# Shared helpers for install.sh bats tests.
# Sourced by install.bats — do not execute directly.

# make_fake_cmd NAME [exit_code] [stdout]
#
# Write an executable stub to $TEST_BIN that prints optional stdout and
# exits with the given code. Ignores all arguments passed to it.
make_fake_cmd() {
    local name="$1"
    local exit_code="${2:-0}"
    local stdout="${3:-}"
    local stub="${TEST_BIN}/${name}"

    if [[ -n "${stdout}" ]]; then
        cat > "${stub}" <<STUB
#!/usr/bin/env bash
printf '%s\\n' '${stdout//\'/\'\\\'\'}'
exit ${exit_code}
STUB
    else
        cat > "${stub}" <<STUB
#!/usr/bin/env bash
exit ${exit_code}
STUB
    fi
    chmod +x "${stub}"
}

# make_fake_python NAME VERSION
#
# Write a python stub to $TEST_BIN that prints VERSION and exits 0.
# The stub ignores all arguments (including -c), making it suitable for
# both the version check and gi-importability check in install.sh.
make_fake_python() {
    local name="$1"
    local version="$2"
    local stub="${TEST_BIN}/${name}"

    cat > "${stub}" <<STUB
#!/usr/bin/env bash
printf '%s\\n' '${version//\'/\'\\\'\'}'
exit 0
STUB
    chmod +x "${stub}"
}

# make_sudo_passthrough
#
# Write a sudo stub that executes its arguments directly (no privilege
# escalation). Required when install.sh calls `sudo apt-get ...`.
make_sudo_passthrough() {
    local stub="${TEST_BIN}/sudo"
    printf '#!/usr/bin/env bash\nexec "$@"\n' > "${stub}"
    chmod +x "${stub}"
}
