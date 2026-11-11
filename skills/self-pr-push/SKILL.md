---
name: self-pr-push
description: Commit the current working-tree changes as small, one-concern commits in the user's `<type>: <summary>` format, check that each commit builds on its own, push the branch, and reply with the list of commits. Run only when the user types /self-pr-push.
argument-hint: "[what to include, leave out, or do after]"
disable-model-invocation: true
---

# Small commits and push

The user types this instead of "create small commits and push". Typing it is their approval to commit and push the changes in the working tree right now, which they have reviewed in their IDE, so don't stop to ask again. The approval covers only those changes: never edit code to make a commit pass a check.

`$ARGUMENTS` may narrow or extend the job ("include the lock files", "only backend/", "then fix review 1"). Follow it. Anything it asks for after the push is a normal request, outside this skill.

`<skill-dir>` below is the base directory shown when this skill loads.

## 1. Read the starting point

1. `git status --short`, `git branch --show-current`, `git remote -v`, then `git fetch -q` and `git status -sb` for ahead/behind. Save `git rev-parse HEAD` as `<base>`.
2. Read the project's CLAUDE.md, CLAUDE.local.md, AGENTS.md and memory for git rules: where to push (Bitbucket plus a GitHub mirror script, Azure DevOps, several repos run with `git -C`), commit format, push hooks. They beat this skill's defaults.
3. Branch:
   - A work branch: push it.
   - The default branch (`main`, `master`, `development`, `dev`): push only if the project's instructions or memory say work goes straight onto it (for example a "build on main" memory). Otherwise make the commits, then ask before pushing and offer a `<type>/<short-kebab-case-summary>` branch.
   - Behind its remote: stop before committing and say so. Pulling, rebasing or merging needs the user's OK.
4. What goes in:
   - Every tracked change in the tree, including edits the user or another session made while you worked. The user means "the current diff".
   - Lockfiles, with the dependency change that produced them.
   - Untracked files this session created or that are plainly part of the work (a new file the diff imports, a migration).
   - Leave out untracked files you can't place, and list them in the reply.
   - Local commits not yet pushed go out with yours; list them in the reply too.

## 2. Group into commits

Read `git diff --stat`, then the diff itself wherever the groups aren't obvious from the paths. Group it so each commit is one concern a reviewer can read on its own:

- one fix, one feature step, one refactor, one dependency bump or one config change per commit;
- refactors and moves before the behaviour change that needs them, and shared code before the code that uses it, so every commit builds;
- generated files with their source (a migration with its generated types), docs with the change they describe, tests with the code they test;
- the user's or another session's edits in their own commit when they are a separate concern.

Split a file that holds two concerns by hunk with `hunks.py` (step 3), and stop there. Never edit the working tree to fake an in-between version of a file, and never write blobs into the index by hand: it is slow, and the result is code nobody wrote or reviewed. If a split would need that, keep those concerns in one commit and say why in the reply. A commit that must be large to build, such as a rename across many files, is fine for the same reason.

Commit messages use the user's format: `<type>: <summary>` with `feat`, `fix`, `refactor` or `chore`, no scope in parentheses, a lowercase imperative summary in plain words, no trailing period. Add a body of plain full sentences only when the subject can't carry the why (what was wrong, or what changes for the user). Never add AI attribution: no co-author trailers, no generated-with footers.

## 3. Commit

For each commit, stage only its files or hunks, check `git diff --cached --stat`, and commit. Commits that are plain file lists can go in one shell call with `set -e`. At the end, `git status --short` shows only what you meant to leave out.

```bash
python3 <skill-dir>/scripts/hunks.py list <file>       # numbered hunks of the file's unstaged diff
python3 <skill-dir>/scripts/hunks.py stage <file> 1,3  # stage hunks 1 and 3 only
```

Hunk numbers change after every commit, so list a file again right before staging from it.

## 4. Check each commit

A commit that only builds together with a later one breaks reverts and `git bisect`, so check each one on its own before pushing. Use the project's quick checks only: typecheck and lint, plus any step they need first (such as `next typegen` or codegen). Skip builds, tests and browser checks; a push hook that needs them runs them anyway.

```bash
python3 <skill-dir>/scripts/check_commits.py <base> '<check command>'
```

The script checks out each commit after `<base>` in a throwaway worktree with the repo's `node_modules` and virtualenvs linked in, runs the command there, and prints PASS or FAIL per commit with the end of the output. When a commit fails, it also runs the command on `<base>`, so an error the base already had isn't blamed on your commit. With a single commit, run the checks in the working tree instead. If the project has no checks, say so in the reply.

If a commit fails on its own, it is still local: `git reset --soft <base>`, regroup and recommit. If the last commit fails, the work itself is broken: stop, report the errors, and don't push.

## 5. Push

Run `git push` (with `-u origin <branch>` when there's no upstream), or whatever the project's instructions say instead. Never force-push and never pass `--no-verify`. If the push is rejected or a hook blocks it, stop and report why.

## 6. Reply

```
Pushed N commits to <remote>/<branch> (<old>..<new>):
1. `abc1234` fix: ...
2. `def5678` feat: ...
```

List the commits oldest first. After the list, add only the lines that apply, one each:
- the checks each commit passes on its own, or which weren't run and why;
- files left out, and why;
- a commit that is larger than it should be or mixes concerns, and why;
- the branch's open PR link, with an offer to run `/self-pr-describe` if the new commits change what its description says;
- anything pushed that isn't live yet, such as a migration not applied to the hosted database.
