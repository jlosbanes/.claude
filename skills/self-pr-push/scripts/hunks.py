#!/usr/bin/env python3
import io
import subprocess
import sys

USAGE = "usage: hunks.py list <file> | hunks.py stage <file> <n,n,...>"


def unstaged_diff(path):
    return subprocess.run(
        ["git", "diff", "--no-color", "--no-ext-diff", "--", path],
        check=True,
        capture_output=True,
    ).stdout


def split(diff):
    head, hunks = [], []
    for line in io.BytesIO(diff).readlines():
        if line.startswith(b"@@"):
            hunks.append([line])
        elif hunks:
            hunks[-1].append(line)
        else:
            head.append(line)
    return b"".join(head), [b"".join(h) for h in hunks]


def show(hunks):
    for number, hunk in enumerate(hunks, 1):
        lines = hunk.decode(errors="replace").splitlines()
        changed = [l for l in lines[1:] if l.startswith(("+", "-"))]
        print(f"#{number} {lines[0]}")
        for line in changed[:8]:
            print("    " + line[:160])
        if len(changed) > 8:
            print(f"    ... {len(changed) - 8} more changed lines")


def stage(path, head, hunks, picks):
    numbers = sorted({int(n) for n in picks.split(",")})
    missing = [n for n in numbers if not 1 <= n <= len(hunks)]
    if missing:
        sys.exit(f"{path} has hunks 1-{len(hunks)}, not {missing}")
    patch = head + b"".join(hunks[n - 1] for n in numbers)
    subprocess.run(["git", "apply", "--cached", "--recount", "-"], input=patch, check=True)
    subprocess.run(["git", "diff", "--cached", "--stat", "--", path], check=True)


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("list", "stage") or len(args) != (2 if args[0] == "list" else 3):
        sys.exit(USAGE)
    path = args[1]
    head, hunks = split(unstaged_diff(path))
    if not hunks:
        sys.exit(f"{path}: no unstaged text hunks (untracked, binary or unchanged); stage the whole file with git add")
    if args[0] == "list":
        show(hunks)
    else:
        stage(path, head, hunks, args[2])


if __name__ == "__main__":
    main()
