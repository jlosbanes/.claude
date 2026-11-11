#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile

DEPENDENCY_DIRS = ("node_modules", ".venv", "venv")
SKIP_DIRS = DEPENDENCY_DIRS + (".git",)
MAX_DEPTH = 3


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def find_dependency_dirs(root):
    found = []
    for dirpath, dirnames, _ in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        found += [os.path.normpath(os.path.join(rel, d)) for d in dirnames if d in DEPENDENCY_DIRS]
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS] if depth < MAX_DEPTH else []
    return found


def link_dependencies(root, worktree, rels):
    for rel in rels:
        target = os.path.join(worktree, rel)
        if os.path.isdir(os.path.dirname(target)) and not os.path.lexists(target):
            os.symlink(os.path.join(root, rel), target)


def unlink_dependencies(worktree, rels):
    for rel in rels:
        target = os.path.join(worktree, rel)
        if os.path.islink(target):
            os.unlink(target)


def check(root, worktree, rels, rev, command, label):
    git("checkout", "-q", "-f", "--detach", rev, cwd=worktree)
    link_dependencies(root, worktree, rels)
    result = subprocess.run(command, shell=True, cwd=worktree, capture_output=True, text=True)
    passed = result.returncode == 0
    print(("PASS " if passed else "FAIL ") + label + git("log", "-1", "--format=%h %s", rev, cwd=root))
    if not passed:
        for line in (result.stdout + result.stderr).strip().splitlines()[-20:]:
            print("    " + line)
    return passed


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: check_commits.py <base> '<check command>'")
    base, command = sys.argv[1], sys.argv[2]
    root = git("rev-parse", "--show-toplevel")
    commits = git("rev-list", "--reverse", f"{base}..HEAD", cwd=root).split()
    if not commits:
        sys.exit(f"no commits after {base}")
    rels = find_dependency_dirs(root)
    worktree = tempfile.mkdtemp(prefix="check-commits-")
    os.rmdir(worktree)
    git("worktree", "add", "-q", "--detach", worktree, commits[0], cwd=root)
    try:
        failed = [sha for sha in commits if not check(root, worktree, rels, sha, command, "")]
        if failed:
            check(root, worktree, rels, base, command, "base ")
    finally:
        unlink_dependencies(worktree, rels)
        subprocess.run(["git", "worktree", "remove", "--force", worktree], cwd=root)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
