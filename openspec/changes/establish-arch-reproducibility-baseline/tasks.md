## 1. Audit Baseline And Boundaries

- [ ] 1.1 Re-run the read-only canary inventory and record repository revision,
  package counts, selected profiles and sandbox limitations without secret values.
- [ ] 1.2 Classify every explicitly installed official package as desired,
  dependency/build-only, candidate-remove or unknown, with an owner and reason.
- [ ] 1.3 Reconcile all reviewed AUR and pinned external packages with the live
  inventory and fail on an unreviewed foreign package.
- [ ] 1.4 Separate current normative facts from historical sections in
  `docs/machines/lab-desktop-01.md` and correct generated profile counts.
- [ ] 1.5 Document the trusted preflight substrate—Arch, network, sudo user, Git
  and Python—without claiming ISO-to-SSH automation.

## 2. State Schemas And Resolver

- [ ] 2.1 Create `os/linux/workstation/` with README, versioned component/role
  schemas, synthetic fixtures and no apply command.
- [ ] 2.2 Implement strict TOML loading with unknown-key, type, enum and schema
  version rejection using Python standard library only.
- [ ] 2.3 Implement reference resolution and stable resource keys for packages,
  user/root targets, services, checks and manual gates.
- [ ] 2.4 Reject missing references, include cycles and conflicting ownership;
  deduplicate only identical resources with compatible owners.
- [ ] 2.5 Add deterministic graph serialization and tests whose output is stable
  across checkout roots and temporary HOME paths.
- [ ] 2.6 Extend host manifests with explicit current/target workstation roles
  while retaining user profiles as a separate field.
- [ ] 2.7 Extend host validation to cover all required keys, types, references,
  selector policy and documentation paths.

## 3. Arch Components And Package Coverage

- [ ] 3.1 Add the foundation component and declare Python plus every runtime
  dependency consumed by its selected user configuration.
- [ ] 3.2 Add boot-recovery declarations for base, kernels, firmware, microcode,
  UEFI/GRUB, Btrfs, Snapper and related verification without applying them.
- [ ] 3.3 Add networking, audio and common graphics components with explicit
  packages, services and checks.
- [ ] 3.4 Add mutually compatible Intel/AMD graphics selectors and fixtures for
  supported, ambiguous and unknown GPU facts.
- [ ] 3.5 Add SDDM/XFCE/Xorg/SSH/XRDP recovery declarations, preserving reviewed
  AUR provenance and exposing the missing XRDP installer as a blocker.
- [ ] 3.6 Connect existing Wayland and daily-workstation package lists to
  components without copying package names.
- [ ] 3.7 Create `arch-workstation` and `arch-hyprland` roles and prove their
  resolved graphs have no ownership conflicts.
- [ ] 3.8 Add cross-list duplicate reporting and explain or remove every duplicate
  package declaration.
- [ ] 3.9 Add a static Pacman policy test that rejects refresh-then-partial-install
  command paths and permits only a full synchronized upgrade transaction.

## 4. Hardware Facts And Fail-closed Selection

- [ ] 4.1 Implement read-only adapters for architecture, boot mode, CPU vendor,
  GPU vendor/driver, battery presence and root filesystem.
- [ ] 4.2 Normalize facts without serials, UUIDs, connector names, IP addresses or
  other host identifiers.
- [ ] 4.3 Implement selector evaluation and show the fact and policy that selected
  each component.
- [ ] 4.4 Add fixtures for Intel, AMD, mixed-GPU, laptop and unsupported hardware.
- [ ] 4.5 Prove unknown or ambiguous hardware stops before privileged planning and
  reports a qualification action.

## 5. Read-only Planner And Evidence

- [ ] 5.1 Implement `os/linux/workstation/scripts/plan` with host/role selection,
  human output and JSON output but no execute or sudo path.
- [ ] 5.2 Observe official/reviewed packages and classify missing, unexpected and
  version drift without installing, removing or downgrading anything.
- [ ] 5.3 Observe selected profiles, runtime commands, services and declared
  root-owned metadata with bounded timeouts and explicit unsupported states.
- [ ] 5.4 Represent authentication, reboot, audio, suspend, screen-sharing and
  recovery drills as named manual gates with safe checks.
- [ ] 5.5 Produce raw evidence only under XDG state and a separately requested,
  stable deterministic projection.
- [ ] 5.6 Redact environment, host-private paths, network identifiers and
  secret-like values; add negative leakage fixtures.
- [ ] 5.7 Verify two identical synthetic runs are byte-identical and meaningful
  desired/observed changes alter the projection.
- [ ] 5.8 Define exit codes and summary aggregation for converged, incomplete,
  drifted, blocked, manual-gate and unsupported states.

## 6. Profile And Runtime Hardening

- [ ] 6.1 Add physical ancestor canonicalization so profile targets cannot escape
  the selected HOME through symlink parents.
- [ ] 6.2 Add rootless tests for lexical traversal, symlink-ancestor escape,
  blocked real targets, wrong symlinks and non-conventional checkout roots.
- [ ] 6.3 Declare runtime commands consumed by every selected Arch profile source
  and fail when a component does not provide them.
- [ ] 6.4 Remove runtime dependence on `$HOME/mydotfiles` from active Arch Kitty,
  Zsh and Yazi configuration while preserving the conventional clone in prose.
- [ ] 6.5 Add transitive include/path validation so a healthy top-level symlink
  cannot hide a missing or non-portable referenced source.
- [ ] 6.6 Add `scripts/doctor --strict`; preserve existing diagnostic behavior and
  test that missing desired targets produce non-zero only in strict mode.

## 7. Verification And CI

- [ ] 7.1 Add L0 schema, graph, package-policy, documentation-link and generated
  artifact checks to CI with reviewed tool/action provenance.
- [ ] 7.2 Add repository-wide private-key and secret-like scanning with a minimal
  reviewed allowlist and negative fixtures.
- [ ] 7.3 Add L1 isolated HOME/state/cache tests for plan, strict verification,
  drift and non-conventional checkout behavior.
- [ ] 7.4 Add failure-injection fixtures that prove byte-identical rollback for
  every mutating component tested by this change without claiming host rollback.
- [ ] 7.5 Label existing Ubuntu profile reconstruction as rootless-structural and
  prevent it from satisfying native Arch requirements.
- [ ] 7.6 Define L2-L7 evidence schemas and traceability entries while leaving
  native container, VM, hardware, human and timing gates visibly incomplete.
- [ ] 7.7 Run all repository validators, strict OpenSpec validation and generated
  document checks from a clean worktree.

## 8. Arch Documentation

- [ ] 8.1 Create `docs/arch/README.md` as the lifecycle index and support-status
  source for Arch.
- [ ] 8.2 Create `docs/arch/REPRODUCIBILITY.md` covering ownership, desired state,
  convergent-current semantics and non-goals.
- [ ] 8.3 Create `docs/arch/RESTORE.md` with phase preconditions, plan commands,
  manual gates, resume points and honest not-yet-automated steps.
- [ ] 8.4 Create `docs/arch/VERIFICATION.md` for L0-L7 claims, evidence handling,
  rollback scope and restore clocks.
- [ ] 8.5 Create `docs/arch/BACKLOG.md` mapping every P0/P1/P2 finding to an owner,
  acceptance gate and independent future change.
- [ ] 8.6 Update README quick access and platform status without editing macOS or
  Windows implementation and without claiming full Arch reproduction.
- [ ] 8.7 Generate package/profile/current-state matrices and make stale counts or
  unchecked generated docs fail validation.

## 9. Canary Review And Follow-ups

- [ ] 9.1 Run the planner on `lab-desktop-01` without sudo and review every
  unknown, unsupported, manual-gate and observed-drift result.
- [ ] 9.2 Verify the planner makes no filesystem, package, service or Git changes
  and leaves the active Hyprland session untouched.
- [ ] 9.3 Review and explicitly approve any redacted canary projection before it
  enters Git; otherwise keep it in XDG state only.
- [ ] 9.4 Record the initial dotfiles-only timing with cold/warm conditions and
  leave ISO-to-SSH and SSH-to-daily-ready unsatisfied until real drills exist.
- [ ] 9.5 Propose independent changes for package/service apply, blank-disk UEFI
  VM, backup/restore, firewall/remote access, SMART monitoring and recovery drills.
- [ ] 9.6 Decide whether to pilot Ansible only after the graph covers the P0
  boot/recovery state and compare it with explicit scripts on total complexity.
- [ ] 9.7 Complete a separate controller review before any privileged apply,
  migration of ownership, or claim that the minutes-level objective is met.
