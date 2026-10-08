## 1. Baseline And Provenance

- [ ] 1.1 Record the reviewed Arch tmux package, installed version, upstream
  references and current live absence of config/server without changing the host.
- [ ] 1.2 Confirm Zellij and Sesh remain absent and record them as not adopted,
  without installing either package.
- [ ] 1.3 Inventory every option, binding, script and layout in `shared/tmux/` as
  keep, rewrite, defer or remove, with a reason.
- [ ] 1.4 Capture a rootless isolated-server result for the pre-change config,
  including its inherited inner TERM defect.

## 2. Core XDG Configuration

- [ ] 2.1 Refactor `shared/tmux/tmux.conf` into a minimal core-only config with no
  TPM, Sesh, plugin or runtime download path.
- [ ] 2.2 Set a tmux-derived default TERM and add local/remote `infocmp` preflight
  with a documented compatible fallback.
- [ ] 2.3 Replace global RGB overrides with verified Kitty/Ghostty
  `terminal-features` patterns and negative unknown-terminal tests.
- [ ] 2.4 Keep passthrough disabled and set the least-privilege clipboard policy;
  document the review required to relax either option.
- [ ] 2.5 Keep `C-b` as the initial prefix and audit every custom binding for tmux,
  shell, Neovim, Kitty, Ghostty and Silakka54 collisions.
- [ ] 2.6 Change reload, layout and helper paths to XDG targets and remove runtime
  dependence on `~/mydotfiles`.
- [ ] 2.7 Separate candidate/deferred helpers from files reachable by the
  production config.

## 3. Automated Isolation Tests

- [ ] 3.1 Add a test harness that creates isolated HOME, XDG roots and a unique
  tmux socket, always killing the server during cleanup.
- [ ] 3.2 Load the config under clean Kitty, Ghostty and unknown TERM fixtures and
  fail on tmux messages, syntax errors or unreviewed option drift.
- [ ] 3.3 Assert inner TERM, terminal features, passthrough, clipboard, prefix,
  plugin absence and config path through tmux introspection.
- [ ] 3.4 Verify the config starts with TPM, Sesh and plugin directories absent and
  performs no network or Git operation.
- [ ] 3.5 Add profile resolution, temporary-HOME link, strict doctor and rollback
  tests for the tmux layer.
- [ ] 3.6 Verify macOS and all non-Arch profile projections are byte-identical to
  their pre-change state.

## 4. Declarative Workspaces

- [ ] 4.1 Define a minimal versioned workspace format for session, window, pane,
  layout and working-directory topology.
- [ ] 4.2 Implement `tmux-workspace` with allowlisted names, full directory
  preflight and no `eval`, history discovery or implicit project scan.
- [ ] 4.3 Make first run create the declared topology and second run attach without
  duplicate sessions, windows, panes or start-once commands.
- [ ] 4.4 Reject missing paths and malformed declarations before creating partial
  session state.
- [ ] 4.5 Add one repository workspace using portable paths and shell-only panes;
  defer servers/builds with side effects.
- [ ] 4.6 Keep scrollback, buffers, commands, socket paths and live session state
  outside Git and generated evidence.

## 5. Arch Canary Layer

- [ ] 5.1 Create `profiles/layers/linux-tmux.links` with only XDG config/layouts
  and the reviewed workspace launcher.
- [ ] 5.2 Document plan, apply and rollback commands for applying the layer alone
  before it enters `arch-workstation`.
- [ ] 5.3 Run resolver, dry-run and strict doctor in an isolated HOME and review
  every target before requesting live activation.
- [ ] 5.4 Obtain explicit approval, verify no active tmux/Zellij work, and link the
  layer only on `lab-desktop-01` without changing terminal auto-start.
- [ ] 5.5 Verify fresh Kitty, Ghostty and shell launches remain outside tmux unless
  the operator explicitly invokes it.

## 6. Functional And SSH Matrix

- [ ] 6.1 Test create, rename, split, resize, zoom, choose, detach, attach, kill and
  config reload from both Kitty and Ghostty.
- [ ] 6.2 Test true color, undercurl, Unicode, resize and rendering at 80x24 without
  requiring Nerd Font glyphs.
- [ ] 6.3 Test Zsh, Neovim, FZF, Yazi and LazyGit input, mouse, focus and redraw;
  document any intentional binding exception.
- [ ] 6.4 Test OSC52 copy locally and over SSH while confirming clipboard read and
  passthrough are not broadened.
- [ ] 6.5 Force an SSH disconnect with an active remote process and prove reattach
  recovers the live session and output.
- [ ] 6.6 Test local tmux → SSH → remote tmux, inner-prefix forwarding, resize and
  detach without terminating the outer session.
- [ ] 6.7 If SSH agent forwarding is in use, test socket refresh on reattach and
  redact its path; otherwise record the check as not applicable.
- [ ] 6.8 Verify tmux adds no network listener and only expected user-owned Unix
  sockets exist.
- [ ] 6.9 Reboot the canary during an approved window and verify the documentation
  predicts process loss while workspace reconstruction remains idempotent.

## 7. Runtime Measurements And Canary Gate

- [ ] 7.1 Define reproducible cold/warm startup and four-pane idle measurement
  commands with version, kernel, terminal and sampling metadata.
- [ ] 7.2 Measure server/client PSS and CPU for 60 seconds; fail the idle gate at
  one percent or more of one core.
- [ ] 7.3 Run a 30-minute idle/output test and block promotion on continuous memory
  growth, lost input or redraw failure.
- [ ] 7.4 Run sustained-output and real-latency SSH scenarios without inferring
  runtime performance from package size.
- [ ] 7.5 Complete at least seven days of canary use and record incidents,
  workarounds and whether the core workflow improved daily recovery.
- [ ] 7.6 Hold a controller review of all automated, interactive, SSH, reboot,
  performance and rollback evidence before promotion.

## 8. Documentation And Decision Record

- [ ] 8.1 Add ADR 0009 with the accepted Arch-only tmux decision, rejected
  alternatives, challenger policy and consequences.
- [ ] 8.2 Rewrite `shared/tmux/README.md` for Pacman/XDG, explicit startup,
  disconnect-versus-reboot semantics, canary and rollback.
- [ ] 8.3 Add a concise keybinding reference and nested SSH prefix instructions.
- [ ] 8.4 Document terminal capability and OSC52 diagnostics for Kitty, Ghostty and
  remote terminfo failure.
- [ ] 8.5 Correct Sesh, Ghostty, ROADMAP and related docs so source presence is not
  called active Arch ownership and no macOS instruction is presented as Arch.
- [ ] 8.6 Update the ADR index and Arch documentation index without changing other
  operating-system implementation.

## 9. Promotion, Rollback And Challenger

- [ ] 9.1 If every gate passes, add `layers/linux-tmux` to `arch-workstation`, run
  all profile projections and update host desired/current state honestly.
- [ ] 9.2 Verify the promoted profile links twice without changes and fresh
  terminals still require explicit tmux invocation.
- [ ] 9.3 Before rollback, list sessions and obtain operator confirmation that work
  is saved; never kill or delete session state automatically.
- [ ] 9.4 Exercise rollback by removing only the layer/include, validating a fresh
  Zsh terminal and leaving package removal as a separate package decision.
- [ ] 9.5 Open a separate Zellij challenger change only if a reproducible tmux gate
  fails and the user approves the bounded comparison.
- [ ] 9.6 If challenged, require official Zellij, a mutually exclusive layer,
  launch outside tmux, built-in plugins only, web/sharing off and the identical
  matrix for no more than 14 days.
- [ ] 9.7 Preserve tmux on a tie; transfer ownership only if Zellij demonstrates a
  documented daily improvement while passing every mandatory gate.
