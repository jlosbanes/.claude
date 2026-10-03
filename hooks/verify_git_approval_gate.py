#!/usr/bin/env python3
"""
Hypothesis: ~/.claude/hooks/git_approval_gate.sh (bash only, no Python at runtime) asks for
approval on every command that commits, pushes, or creates/merges a PR (however it is
written), stays silent for every other command, and asks if it cannot read the input.

Test: feed the hook the same JSON Claude Code sends it, for commands that should and
should not trigger, plus malformed input, and check its decision.

Expected: every "ask" case returns permissionDecision "ask"; every "pass" case returns
no output. Read-only: runs the hook only, touches no repo.
"""
import json
import os
import subprocess
import sys

HOOK = os.path.expanduser("~/.claude/hooks/git_approval_gate.sh")

ASK = [
    "git commit -m 'fix'",
    'git commit -m "fix: handle \\"quoted\\" text"',
    "git push",
    "git push origin main --force",
    "git -C /some/repo push",
    'git -C "/my repo" push',
    "git -c user.name=x -c user.email=y commit -m msg",
    "git --no-pager commit --amend",
    "cd app && git add . && git commit -m wip && git push",
    "git status\ngit push",
    "bash -c 'git push origin HEAD'",
    'eval "git commit -m x"',
    "/usr/bin/git push",
    "GIT_TRACE=1 git push",
    "gh pr create --fill",
    "gh pr merge 42 --squash",
]
PASS = [
    "git status",
    "git diff --stat",
    "git log --oneline -5",
    "git add .",
    "git fetch origin",
    "git pull",
    "git stash push",          # stash push is local, not a remote push
    "git show HEAD:commit.txt",
    "ls commit push",
    "npm run push-notifications",
    "gh pr view 42",
    "gh pr list",
]


def decision(payload):
    out = subprocess.run(["bash", HOOK], input=payload, capture_output=True, text=True, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out.strip() else "pass"


def bash_payload(command, description="Run a command"):
    return json.dumps({
        "session_id": "test", "cwd": "/home/me/git/push-service", "hook_event_name": "PreToolUse",
        "tool_name": "Bash", "tool_input": {"command": command, "description": description},
    })


cases = [("ask", c, bash_payload(c)) for c in ASK] + [("pass", c, bash_payload(c)) for c in PASS]
cases += [
    # Only the command is checked, not the description or the folder path.
    ("pass", "ls  [description mentions git commit]", bash_payload("ls", "Prepare to git commit and git push")),
    # Fail-closed: unreadable input must still ask.
    ("ask", "[malformed input]", "not json at all"),
]

failures = []
for expected, label, payload in cases:
    got = decision(payload)
    ok = got == expected
    if not ok:
        failures.append(label)
    print(f"{'ok  ' if ok else 'FAIL'} expected={expected:<4} got={got:<4} | {label!r}")

print()
print("CONFIRMED" if not failures else f"REFUTED: {len(failures)} case(s) wrong: {failures}")
sys.exit(1 if failures else 0)
