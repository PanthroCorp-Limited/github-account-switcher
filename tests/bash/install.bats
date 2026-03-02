#!/usr/bin/env bats
# Tests for install.sh functions.
# Requires bats-core, bats-support, bats-assert (libs/ submodules).

load '../../libs/bats-support/load'
load '../../libs/bats-assert/load'
load 'helpers/mock_env'

INSTALL_SH="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)/install.sh"

setup() {
    TEST_BIN="$(mktemp -d)"
    TEST_HOME="$(mktemp -d)"
    export HOME="${TEST_HOME}"
    export PATH="${TEST_BIN}:${PATH}"

    # Source install.sh — the BASH_SOURCE guard means main() is NOT called.
    # shellcheck source=../../install.sh
    source "${INSTALL_SH}"
}

teardown() {
    rm -rf "${TEST_BIN}" "${TEST_HOME}"
}

# ---------------------------------------------------------------------------
# check_linux
# ---------------------------------------------------------------------------

@test "check_linux passes on Linux" {
    run check_linux
    assert_success
}

@test "check_linux dies on non-Linux" {
    make_fake_cmd uname 0 "Darwin"
    run check_linux
    assert_failure
}

# ---------------------------------------------------------------------------
# check_python
# ---------------------------------------------------------------------------

@test "check_python finds python3.12" {
    make_fake_python "python3.12" "3.12"
    check_python
    assert_equal "${PYTHON}" "python3.12"
}

@test "check_python falls back to python3 when python3.12 absent" {
    # Shadow any real python3.12 with a stub reporting a version that fails
    # the >= 3.12 check, forcing fallback to python3.
    make_fake_python "python3.12" "3.6"
    make_fake_python "python3" "3.12"
    check_python
    assert_equal "${PYTHON}" "python3"
}

@test "check_python rejects python 3.11" {
    make_fake_python "python3.12" "3.6"
    make_fake_python "python3" "3.11"
    run check_python
    assert_failure
}

@test "check_python dies with no python" {
    # Shadow both candidates with stubs that report a version too old to pass.
    make_fake_python "python3.12" "3.6"
    make_fake_python "python3" "3.6"
    run check_python
    assert_failure
}

# ---------------------------------------------------------------------------
# install_system_deps
# ---------------------------------------------------------------------------

@test "install_system_deps skips when gi already importable" {
    # Python stub exits 0 → gi importable
    make_fake_cmd _fake_python 0
    PYTHON="_fake_python"
    make_sudo_passthrough
    make_fake_cmd apt-get 0 "apt-get-executed"

    run install_system_deps
    assert_success
    refute_output --partial "apt-get-executed"
}

@test "install_system_deps calls apt-get when gi missing" {
    # Python stub exits 1 → gi not importable
    make_fake_cmd _fake_python 1
    PYTHON="_fake_python"
    make_sudo_passthrough
    make_fake_cmd apt-get 0 "apt-get-executed"

    run install_system_deps
    assert_success
    assert_output --partial "apt-get-executed"
}

@test "install_system_deps warns but succeeds when apt-get absent" {
    make_fake_cmd _fake_python 1
    PYTHON="_fake_python"
    # Restrict PATH to TEST_BIN only so the real /usr/bin/apt-get is hidden.
    # Restore immediately after run so teardown still has access to rm etc.
    local _saved_path="${PATH}"
    export PATH="${TEST_BIN}"
    run install_system_deps
    export PATH="${_saved_path}"

    assert_success
    assert_output --partial "apt-get not found"
}

# ---------------------------------------------------------------------------
# create_venv
# ---------------------------------------------------------------------------

@test "create_venv prints creating message when venv absent" {
    make_fake_cmd _fake_python 0
    PYTHON="_fake_python"

    run create_venv
    assert_success
    assert_output --partial "Creating venv"
}

@test "create_venv prints upgrade message when venv exists" {
    make_fake_cmd _fake_python 0
    PYTHON="_fake_python"
    mkdir -p "${VENV_DIR}"

    run create_venv
    assert_success
    assert_output --partial "upgrade"
}

# ---------------------------------------------------------------------------
# link_binary
# ---------------------------------------------------------------------------

@test "link_binary creates symlink at BIN_DIR" {
    mkdir -p "${VENV_DIR}/bin"
    touch "${VENV_DIR}/bin/gh-switcher"

    run link_binary
    assert_success
    assert [ -L "${BIN_DIR}/gh-switcher" ]
}

@test "link_binary creates BIN_DIR when absent" {
    mkdir -p "${VENV_DIR}/bin"
    touch "${VENV_DIR}/bin/gh-switcher"
    # BIN_DIR does not exist yet — link_binary must create it

    run link_binary
    assert_success
    assert [ -d "${BIN_DIR}" ]
}

# ---------------------------------------------------------------------------
# check_path
# ---------------------------------------------------------------------------

@test "check_path warns when BIN_DIR absent from PATH" {
    assert [ -n "${BIN_DIR}" ]
    export PATH="/usr/bin:/usr/local/bin"
    run check_path
    assert_output --partial "not in your PATH"
}

@test "check_path is silent when BIN_DIR present in PATH" {
    export PATH="${BIN_DIR}:${PATH}"
    run check_path
    refute_output --partial "not in your PATH"
}
