#!/usr/bin/env python3

import json
import copy
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PILOT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_ROOT / "scripts"))

import pilot  # noqa: E402
import pilot_audit  # noqa: E402
import pilot_policy  # noqa: E402


class ContainmentTests(unittest.TestCase):
    def test_negative_matrix(self) -> None:
        results = pilot.containment_self_tests()
        self.assertTrue(results)
        self.assertTrue(all(results.values()))
        self.assertIn("symlink-escape", results)
        self.assertIn("active-profile-target", results)

    def test_existing_run_root_is_rejected(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="pilot-reused-test-"))
        self.addCleanup(shutil.rmtree, root, True)
        with self.assertRaises(pilot.PilotError):
            pilot.prepare_context("linux", root)

    def test_host_secrets_and_agent_are_not_inherited(self) -> None:
        injected = {
            "PILOT_TOKEN": "must-not-pass",
            "SSH_AUTH_SOCK": "/tmp/host-agent.sock",
            "HTTPS_PROXY": "https://user:password@example.invalid",
        }
        with mock.patch.dict(os.environ, injected, clear=False):
            context = pilot.prepare_context("linux")
            self.addCleanup(shutil.rmtree, context.root, True)
            environment = context.environment
        for key in injected:
            self.assertNotIn(key, environment)
        self.assertEqual(environment["HOME"], str(context.home))
        self.assertEqual(environment["TMPDIR"], str(context.temp))

    @unittest.skipUnless(sys.platform.startswith("linux"), "Bubblewrap prefix is Linux-only")
    def test_bubblewrap_uses_private_dev_and_one_host_backed_write_root(self) -> None:
        context = pilot.prepare_context("linux")
        self.addCleanup(shutil.rmtree, context.root, True)
        prefix = pilot.bubblewrap_prefix(context)
        self.assertNotIn("--dev-bind", prefix)
        self.assertNotIn("--unshare-net", prefix)
        self.assertIn(["--dev", "/dev"], [prefix[index:index + 2] for index in range(len(prefix) - 1)])
        self.assertIn(["--proc", "/proc"], [prefix[index:index + 2] for index in range(len(prefix) - 1)])
        self.assertIn(
            ["--bind", str(context.root), str(context.root)],
            [prefix[index:index + 3] for index in range(len(prefix) - 2)],
        )


class StaticPolicyTests(unittest.TestCase):
    def test_ambient_home_template_is_rejected(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="pilot-static-test-"))
        self.addCleanup(shutil.rmtree, root, True)
        (root / "dot_bad.tmpl").write_text("{{ .chezmoi.homeDir }}\n", encoding="utf-8")
        with self.assertRaises(pilot.PilotError):
            pilot.static_validate_source(root)

    def test_template_key_guardrail_is_rejected(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="pilot-template-test-"))
        self.addCleanup(shutil.rmtree, root, True)
        keys = "\n".join(f"{{{{ .pilot.git.key{index} }}}}" for index in range(6))
        (root / "dot_bad.tmpl").write_text(keys + "\n", encoding="utf-8")
        with self.assertRaises(pilot.PilotError):
            pilot.static_validate_source(root)

    def test_unexpected_fixture_key_is_rejected(self) -> None:
        data = pilot.load_json(PILOT_ROOT / "data/linux.json")
        data["pilot"]["unexpected"] = True
        with self.assertRaises(pilot.PilotError):
            pilot.validate_fixture_data(data, "linux")

    def test_secret_like_fixture_data_is_rejected(self) -> None:
        data = pilot.load_json(PILOT_ROOT / "data/linux.json")
        data["pilot"]["git"]["name"] = "token=github_pat_not_allowed_123456789"
        with self.assertRaises(pilot.PilotError):
            pilot.validate_fixture_data(data, "linux")


class ModelTests(unittest.TestCase):
    def test_repository_model_and_support_matrix(self) -> None:
        result = pilot.validate_repository()
        self.assertEqual(result["profileReferences"], 0)
        self.assertTrue(result["semantics"]["windowsKeyReserved"])
        support = (PILOT_ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("Linux", support)
        self.assertIn("macOS", support)
        self.assertIn("Windows", support)

    def test_missing_git_data_fails_render(self) -> None:
        context = pilot.prepare_context("linux")
        self.addCleanup(shutil.rmtree, context.root, True)
        template = context.source / "dot_gitconfig.tmpl"
        template.write_text(template.read_text(encoding="utf-8") + "missing={{ .pilot.git.missing }}\n", encoding="utf-8")
        with self.assertRaises(pilot.PilotError):
            pilot.run_chezmoi(context, "missing-data", ["apply", "--dry-run", "--verbose"])

    def test_source_change_changes_preview_digest(self) -> None:
        context = pilot.prepare_context("linux")
        self.addCleanup(shutil.rmtree, context.root, True)
        before = pilot.input_digest(context)
        template = context.source / "dot_gitconfig.tmpl"
        template.write_text(template.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8")
        self.assertNotEqual(before, pilot.input_digest(context))

    def test_chezmoi_build_banner_does_not_change_preview_digest(self) -> None:
        context = pilot.prepare_context("linux")
        self.addCleanup(shutil.rmtree, context.root, True)
        arch_banner = "chezmoi version v2.72.0, built at 2026-08-03T08:20:49Z"
        upstream_banner = (
            "chezmoi version v2.72.0, commit f81cb321789aa3df62871248f5e4d361a59e7cc1, "
            "built at 2026-08-02T18:45:48Z, built by goreleaser"
        )
        with mock.patch.object(pilot, "chezmoi_version", return_value=arch_banner):
            arch_digest = pilot.input_digest(context)
        with mock.patch.object(pilot, "chezmoi_version", return_value=upstream_banner):
            upstream_digest = pilot.input_digest(context)
        self.assertEqual(arch_digest, upstream_digest)
        with mock.patch.object(
            pilot, "chezmoi_version", return_value="chezmoi version v2.73.0"
        ):
            self.assertNotEqual(arch_digest, pilot.input_digest(context))

    def test_windows_fixture_is_separate_json(self) -> None:
        result = pilot.validate_windows_fixture()
        self.assertTrue(result["structuralOnly"])
        parsed = json.loads((PILOT_ROOT / "fixtures/windows-terminal/settings.json").read_text(encoding="utf-8"))
        self.assertNotIn("kitty", json.dumps(parsed).lower())

    def test_false_os_window_mapping_is_rejected(self) -> None:
        semantics = pilot.load_json(PILOT_ROOT / "semantics.json")
        mapping = semantics["actions"]["terminal.new-os-window"]["macos"]
        mapping.update(
            {
                "status": "mapped",
                "chords": ["cmd+enter"],
                "nativeAction": "new_window",
                "expectedLine": "map cmd+enter new_window",
            }
        )
        with self.assertRaises(pilot.PilotError):
            pilot.validate_semantics(semantics)

    def test_semantic_chord_collision_is_rejected(self) -> None:
        semantics = pilot.load_json(PILOT_ROOT / "semantics.json")
        mapping = semantics["actions"]["terminal.new-os-window"]["macos"]
        mapping.update(
            {
                "status": "mapped",
                "chords": ["cmd+t"],
                "nativeAction": "new_os_window",
            }
        )
        with self.assertRaises(pilot.PilotError):
            pilot.validate_semantics(semantics)


class EvidencePolicyTests(unittest.TestCase):
    @staticmethod
    def evidence() -> dict:
        return {
            "recordedAt": "2026-01-01T00:00:00Z",
            "git": {
                "branch": "feature/openspec-chezmoi-pilot",
                "reviewedBase": "base",
                "headRevision": "head-a",
                "dirty": True,
            },
            "tools": {
                "chezmoi": "chezmoi version 2.72.0",
                "openspec": "1.9.0",
                "python": "3.14.7",
            },
            "results": {
                "linux": {
                    "commands": [{
                        "command": ["chezmoi", "apply"],
                        "exit": 0,
                        "startedAt": "start-a",
                        "endedAt": "end-a",
                        "stdoutSha256": "hash-a",
                        "rawStdoutSha256": "raw-a",
                        "rawStdoutLines": 246,
                        "rawStdoutPreview": ["raw-a"],
                    }],
                    "manifest": [{"path": ".config/file", "sha256": "manifest-a", "mode": "0644"}],
                }
            },
            "comparison": {"metric": 10},
        }

    def test_timestamps_do_not_change_projection(self) -> None:
        first = self.evidence()
        second = copy.deepcopy(first)
        second["recordedAt"] = "2030-12-31T23:59:59Z"
        command = second["results"]["linux"]["commands"][0]
        command["startedAt"] = "start-b"
        command["endedAt"] = "end-b"
        self.assertEqual(
            pilot_policy.evidence_projection(first),
            pilot_policy.evidence_projection(second),
        )

    def test_raw_dump_config_provenance_does_not_change_effective_projection(self) -> None:
        arch = self.evidence()
        ubuntu = copy.deepcopy(arch)
        command = ubuntu["results"]["linux"]["commands"][0]
        command.update(
            rawStdoutSha256="raw-ubuntu",
            rawStdoutLines=249,
            rawStdoutPreview=["raw-ubuntu"],
        )
        self.assertEqual(
            pilot_policy.evidence_projection(arch),
            pilot_policy.evidence_projection(ubuntu),
        )

    def test_publication_git_and_compatible_python_do_not_change_projection(self) -> None:
        feature = self.evidence()
        main = copy.deepcopy(feature)
        main["git"].update({
            "branch": "main",
            "reviewedBase": "rebased-base",
            "headRevision": "post-rebase-head",
            "dirty": False,
        })
        main["tools"]["python"] = "3.14.8"
        feature_projection = pilot_policy.evidence_projection(feature)
        main_projection = pilot_policy.evidence_projection(main)
        self.assertEqual(feature_projection, main_projection)
        self.assertNotIn("git", feature_projection)
        self.assertEqual(
            feature_projection["tools"]["python"],
            pilot_policy.PYTHON_COMPATIBILITY_CONTRACT,
        )
        self.assertEqual(
            feature_projection["tools"]["chezmoi"],
            pilot_policy.CHEZMOI_EXACT_VERSION,
        )
        self.assertEqual(feature_projection["tools"]["openspec"], "1.9.0")

    def test_chezmoi_build_provenance_does_not_change_exact_version_projection(self) -> None:
        arch = self.evidence()
        arch["tools"]["chezmoi"] = (
            "chezmoi version v2.72.0, built at 2026-08-03T08:20:49Z"
        )
        upstream = copy.deepcopy(arch)
        upstream["tools"]["chezmoi"] = (
            "chezmoi version v2.72.0, commit f81cb321789aa3df62871248f5e4d361a59e7cc1, "
            "built at 2026-08-02T18:45:48Z, built by goreleaser"
        )
        self.assertEqual(
            pilot_policy.evidence_projection(arch),
            pilot_policy.evidence_projection(upstream),
        )
        self.assertEqual(
            pilot_policy.evidence_projection(upstream)["tools"]["chezmoi"],
            "2.72.0",
        )

    def test_deterministic_evidence_changes_projection(self) -> None:
        changes = {
            "command": lambda value: value["results"]["linux"]["commands"][0]["command"].append("--dry-run"),
            "hash": lambda value: value["results"]["linux"]["commands"][0].update(stdoutSha256="hash-b"),
            "manifest": lambda value: value["results"]["linux"]["manifest"][0].update(sha256="manifest-b"),
            "metric": lambda value: value["comparison"].update(metric=11),
            "chezmoi-version": lambda value: value["tools"].update(chezmoi="chezmoi version 2.73.0"),
            "openspec-version": lambda value: value["tools"].update(openspec="1.9.1"),
            "unsupported-python": lambda value: value["tools"].update(python="3.10.19"),
        }
        baseline = self.evidence()
        for name, mutate in changes.items():
            with self.subTest(name=name):
                changed = copy.deepcopy(baseline)
                mutate(changed)
                self.assertNotEqual(
                    pilot_policy.evidence_projection(baseline),
                    pilot_policy.evidence_projection(changed),
                )

    def test_projection_diagnostics_report_normalized_leaf_paths(self) -> None:
        reviewed = pilot_policy.evidence_projection(self.evidence())
        fresh = copy.deepcopy(reviewed)
        fresh["comparison"]["metric"] = 11
        fresh["results"]["linux"]["manifest"][0]["sha256"] = "manifest-b"
        differences = pilot_policy.projection_differences(reviewed, fresh)
        self.assertEqual(
            [difference["path"] for difference in differences],
            [
                "$/comparison/metric",
                "$/results/linux/manifest/0/sha256",
            ],
        )

    @staticmethod
    def mandatory() -> dict:
        return {
            "outOfRootWrites": 0,
            "realOwnershipOverlaps": 0,
            "secretFindings": 0,
            "prohibitedFeatureFindings": 0,
            "protectedMetadataChanges": 0,
            "rollbackExact": True,
            "idempotent": True,
            "allSelectedFixturesPassed": True,
            "deterministic": True,
        }

    def test_outcome_selector_rejects_critical_failure(self) -> None:
        mandatory = self.mandatory()
        mandatory["secretFindings"] = 1
        self.assertEqual(
            pilot_policy.select_outcome(mandatory, {"windows": True}, {"policy": {"permitsSelectiveMigration": True}}),
            "reject",
        )

    def test_outcome_selector_continues_without_native_windows(self) -> None:
        self.assertEqual(
            pilot_policy.select_outcome(self.mandatory(), {"windows": False}, {"policy": {"permitsSelectiveMigration": True}}),
            "keep-and-continue-evaluation",
        )

    def test_outcome_selector_continues_on_incomplete_mandatory(self) -> None:
        mandatory = self.mandatory()
        mandatory["deterministic"] = False
        self.assertEqual(
            pilot_policy.select_outcome(mandatory, {"windows": True}, {"policy": {"permitsSelectiveMigration": True}}),
            "keep-and-continue-evaluation",
        )

    def test_outcome_selector_can_recommend_only_when_all_gates_pass(self) -> None:
        self.assertEqual(
            pilot_policy.select_outcome(self.mandatory(), {"windows": True}, {"policy": {"permitsSelectiveMigration": True}}),
            "recommend-selective-migration",
        )

    def test_recommendation_without_native_windows_violates_invariant(self) -> None:
        evidence = {
            "mandatory": self.mandatory(),
            "nativeEvidence": {"windows": False},
            "comparison": {"policy": {"permitsSelectiveMigration": True}},
            "outcome": "recommend-selective-migration",
        }
        with self.assertRaises(ValueError):
            pilot_policy.assert_outcome_invariants(evidence)


class TraceabilityTests(unittest.TestCase):
    def assert_ci_rejected(self, workflow: str) -> None:
        with tempfile.TemporaryDirectory(prefix="pilot-ci-policy-") as temp:
            repo_root = Path(temp)
            workflow_path = repo_root / ".github/workflows/chezmoi-pilot.yml"
            workflow_path.parent.mkdir(parents=True)
            workflow_path.write_text(workflow, encoding="utf-8")
            with self.assertRaises(pilot_audit.AuditError):
                pilot_audit.validate_ci_workflow(repo_root)

    def test_ci_policy_rejects_container_and_security_relaxations(self) -> None:
        workflow = (pilot.REPO_ROOT / ".github/workflows/chezmoi-pilot.yml").read_text(
            encoding="utf-8"
        )
        variants = {
            "job-container": workflow.replace(
                "    runs-on: ubuntu-22.04",
                "    runs-on: ubuntu-22.04\n    container: archlinux:base",
                1,
            ),
            "seccomp-unconfined": workflow + "\n# seccomp=unconfined\n",
            "privileged": workflow + "\n# --privileged\n",
            "cap-add": workflow + "\n# --cap-add SYS_ADMIN\n",
            "apparmor-bypass": workflow + "\n# apparmor=unconfined\n",
            "sysctl-weakening": workflow + "\n# sysctl kernel.unprivileged_userns_clone=1\n",
            "silent-skip": workflow + "\n# continue-on-error: true\n",
        }
        for name, variant in variants.items():
            with self.subTest(name=name):
                self.assert_ci_rejected(variant)

    def test_ci_policy_requires_smoke_before_checkout_and_harness(self) -> None:
        workflow = (pilot.REPO_ROOT / ".github/workflows/chezmoi-pilot.yml").read_text(
            encoding="utf-8"
        )
        reordered = workflow.replace(
            "bwrap --die-with-parent", "__PILOT_SMOKE__", 1
        ).replace(
            "experiments/chezmoi-pilot/scripts/validate",
            "bwrap --die-with-parent",
            1,
        ).replace(
            "__PILOT_SMOKE__",
            "experiments/chezmoi-pilot/scripts/validate",
            1,
        )
        self.assert_ci_rejected(reordered)

    def test_ci_policy_requires_full_reviewed_base_history(self) -> None:
        workflow = (pilot.REPO_ROOT / ".github/workflows/chezmoi-pilot.yml").read_text(
            encoding="utf-8"
        )
        self.assert_ci_rejected(workflow.replace("          fetch-depth: 0\n", "", 1))

    def test_ci_policy_requires_pinned_shellcheck(self) -> None:
        workflow = (pilot.REPO_ROOT / ".github/workflows/chezmoi-pilot.yml").read_text(
            encoding="utf-8"
        )
        self.assert_ci_rejected(workflow.replace("v0.11.0", "v0.10.0"))
        self.assert_ci_rejected(
            workflow.replace(
                "8c3be12b05d5c177a04c29e3c78ce89ac86f1595681cab149b65b97c4e227198",
                "0" * 64,
            )
        )

    def test_traceability_rejects_stale_check_id(self) -> None:
        declaration = pilot.load_json(PILOT_ROOT / "traceability.json")
        declaration = copy.deepcopy(declaration)
        automated = next(
            entry for entry in declaration["entries"]
            if entry["coverage"]["kind"] == "automated-check"
        )
        automated["coverage"]["id"] = "UT-DOES-NOT-EXIST"
        with self.assertRaises(pilot.PilotError):
            pilot.validate_traceability(declaration_override=declaration)

    def test_traceability_rejects_missing_scenario(self) -> None:
        declaration = pilot.load_json(PILOT_ROOT / "traceability.json")
        declaration = copy.deepcopy(declaration)
        declaration["entries"].pop()
        with self.assertRaises(pilot.PilotError):
            pilot.validate_traceability(declaration_override=declaration)


if __name__ == "__main__":
    unittest.main()
