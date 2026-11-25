#!/usr/bin/env python3
"""Dispatch milestone gates without confusing scaffold hygiene with acceptance."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def load_manifest(root):
    manifest = json.loads((root / "hack/acceptance/phases.json").read_text())
    ledger = (root / "docs/PHASES.md").read_text()
    if not ledger.startswith("---\n"):
        raise ValueError("PHASES must have phases/v1 YAML frontmatter")
    header = ledger.split("\n---", 1)[0]
    if not re.search(r"^schema: phases/v1$", header, re.M):
        raise ValueError("PHASES schema must be phases/v1")
    phase_ids = re.findall(r"^  - id: (M[0-9]+)$", header, re.M)
    rows = {key: value for key, value in manifest.items() if not key.startswith("_")}
    if not phase_ids or len(phase_ids) != len(set(phase_ids)) or set(rows) != set(phase_ids):
        raise ValueError("manifest milestones must match ledger milestones exactly")
    for phase, row in rows.items():
        if not isinstance(row, dict) or not re.fullmatch(r"M[0-9]+", phase):
            raise ValueError("invalid milestone row")
        if not isinstance(row.get("gate"), str) or not row.get("tier"):
            raise ValueError(phase + ": gate and tier are required")
        if any(type(row.get(key, False)) is not bool for key in ("manual", "skeleton")):
            raise ValueError(phase + ": manual/skeleton must be booleans")
        for key in ("requires", "args"):
            value = row.get(key, [])
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                raise ValueError(phase + ": " + key + " must be a string list")
        if any(re.fullmatch(r"M[0-9]+", item) or ":M" in item for item in row.get("requires", [])):
            raise ValueError(phase + ": requires contains capabilities, not phase dependencies")
        path = (root / row["gate"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(phase + ": gate path must resolve inside the repository")
        block = re.search(r"^  - id: " + phase + r"\n(.*?)(?=^  - id: |\Z)", header, re.M | re.S)
        if row.get("skeleton") and re.search(r"^    status: done$", block.group(1), re.M):
            raise ValueError(phase + ": a skeleton milestone cannot be done")
    return rows


def run(root, phase=None, manual=False, capabilities=(), timeout=600):
    rows = load_manifest(root)
    if phase is not None:
        if phase not in rows:
            raise ValueError("unknown milestone: " + phase)
        rows = {phase: rows[phase]}
    failed = False
    for name, row in rows.items():
        if row.get("manual") and not manual:
            print(name + ": PENDING manual evidence; not executed", flush=True)
            failed |= phase is not None
            continue
        skeleton = row.get("skeleton", False)
        missing = set(row.get("requires", [])) - set(capabilities)
        if missing and not skeleton:
            print(name + ": ERROR missing capabilities: " + ", ".join(sorted(missing)), flush=True)
            failed = True
            continue
        command = ["sh", str(root / row["gate"]), *row.get("args", [])]
        result = subprocess.run(command, cwd=root, timeout=timeout, check=False)
        if skeleton:
            if result.returncode != 1:
                print(name + ": ERROR skeleton must exit exactly 1", flush=True)
                failed = True
            else:
                print(name + ": PENDING skeleton; no product acceptance", flush=True)
                failed |= phase is not None
        elif result.returncode:
            print(name + ": FAIL exit " + str(result.returncode), flush=True)
            failed = True
        else:
            print(name + ": PASS executed gate", flush=True)
    if phase is None:
        print("Commit checks do not turn pending milestones into completed work.", flush=True)
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", help="require actual acceptance for this milestone")
    parser.add_argument("--manual", action="store_true", help="execute manual gates in this environment")
    parser.add_argument("--capability", action="append", default=[], help="capability supplied by this environment")
    parser.add_argument("--timeout", type=int, default=600, help="maximum seconds per gate")
    args = parser.parse_args()
    try:
        if args.timeout < 1:
            raise ValueError("timeout must be positive")
        return run(Path(__file__).resolve().parents[1], args.phase, args.manual,
                   args.capability, args.timeout)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print("acceptance: ERROR: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
