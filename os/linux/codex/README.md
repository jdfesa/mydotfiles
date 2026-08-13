# Codex CLI on Linux

Codex CLI uses a companion executable for Code Mode. The companion must match
the installed Codex version and be available beside `codex` in the user's
`PATH`.

## Install the Code Mode host

Preview the operation first:

```sh
os/linux/codex/scripts/install-code-mode-host
```

Install the matching official release artifact:

```sh
os/linux/codex/scripts/install-code-mode-host --execute
```

The installer:

1. reads the version from `codex --version`;
2. selects the official Linux asset for the current CPU architecture;
3. verifies its SHA-256 against the digest published by the GitHub release API;
4. installs it atomically as `~/.local/bin/codex-code-mode-host`;
5. backs up `~/.codex/config.toml`;
6. enables `features.code_mode_host` through the Codex CLI;
7. checks the effective feature state and runs `codex doctor --summary`.

No authentication files are read or copied. The installer is user-scoped and
does not require `sudo`.

## Why not compile it locally?

For Codex `0.147.0`, building the official tag with Cargo failed because
`rusty_v8` requested a prebuilt V8 archive that was not published at the
generated URL. The official Codex release already provides a signed-build
artifact for Linux, so using that version-matched binary is smaller, faster,
and easier to reproduce.

