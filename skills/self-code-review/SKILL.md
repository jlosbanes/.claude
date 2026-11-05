---
name: self-code-review
description: Review the current diff, a branch or a PR for bugs and risks, and report the verified findings as one short table, tagged by type (Business Behaviour, Code Level, AI Behaviour, Security, Data, Performance, Test Coverage, Maintainability), with a recommendation per row. Use this when the user types /self-code-review, or asks to review their changes, a branch or a PR and wants the findings in their table format. Read-only: it never edits code.
argument-hint: "[PR number, URL, branch or path]"
---

# Self Code Review

Review a change the way the built-in `/code-review` does: find real bugs and risks, verify each one against the code. But report them as one scannable table the user can decide from at a glance, instead of long failure-scenario paragraphs.

Don't call the `ReportFindings` tool. Print the table as text.

## 1. Find the change

Target given by the user: $ARGUMENTS

- **Nothing given:** review the current branch: uncommitted changes plus the commits since its base. The base is the branch it was cut from (check the project's CLAUDE.md or memory first, e.g. `dev`). Fetch first, then use `git diff <base>...HEAD` plus `git diff` and `git status --short` for uncommitted and untracked files.
- **PR number or URL:** `gh pr view <target> --json number,title,body,baseRefName,headRefName` and `gh pr diff <target>`. If the project says not to use `gh`, use git only.
- **Branch:** `git diff <base>...<branch>`.
- **Path:** review only that file or folder within the current change.

Skip generated files (codegen output, lockfiles, build output) unless they're the point of the change.

## 2. Learn the intent

Read the commit messages, the PR body, the project's task notes (e.g. `tasks/todo.md`) and any ticket text in the conversation. Note what the change is supposed to do and any decisions the user already made, so you don't report an agreed behaviour as a bug. Treat them as claims to check, not facts.

## 3. Review

Read each changed hunk **and** the code around it: callers, consumers and the old version (`git show <base>:<path>`). Look through these lenses. Each one becomes a Type label:

| Type | What it covers |
|---|---|
| Business Behaviour | What users or clients see or get is wrong, surprising, or depends on a product rule that needs a decision |
| Code Level | Logic errors, crashes, wrong state, missing error handling, races, type holes |
| AI Behaviour | Prompts and model output: instructions the model may ignore, data the model shouldn't see |
| Security | Auth, trust boundaries, data exposure, injection |
| Data | Migrations, existing records, integrity, irreversible writes |
| Performance | Extra queries, heavy loops, slow renders |
| Test Coverage | Behaviour the change adds or alters that no test pins |
| Maintainability | Duplication, scattered rules, structure that invites the next bug |

Use only the types that have findings. Add a new type only when none of these fits.

For a large change (roughly 10+ files or several areas), send one subagent per lens or area in parallel. Ask each for findings with `file:line`, a concrete failure scenario, and whether the same code already behaved this way on the base. Keep the verification step for yourself.

## 4. Verify every finding

Before a finding goes in the table:

- Re-read the code it points at and confirm the failure scenario really happens. Drop it if it doesn't.
- Check the base version. If the problem existed before this change, keep it but say "(already like this on <base>)".
- When reading can't settle it, run a test or a small verification script, following the user's global rules for those. If it still can't be settled, keep it and mark the recommendation "Check: <how>".
- Drop style nits a formatter or linter would catch, and anything the user already decided.

## 5. Report

Rank by severity, most severe first. Reply with exactly this shape:

```markdown
| # | Type | Issue | Recommend |
|---|---|---|---|
| 1 | Business Behaviour | Job Numbers like "N/A" end in "A", so they count as Apex Insurance | Decide (none in local data) |
| 2 | Code Level | Saving with every field blank creates an empty reference row | Fix: skip if blank |
| 3 | Maintainability | The same rule is computed twice in the Summary section | Fix, trivial |
```

Then one closing line: which rows to fix, and the decisions needed, e.g. "Fix 2 and 3? Your call on 1."

Rules for the table:
- **Issue:** one plain-language line, about 15 words at most. Say what goes wrong for whom, not how the code is built. Name screens and fields the way the product does. Add a code identifier only when it's the clearest pointer.
- **Recommend:** start with one of these words:
  - `Fix`: add ", small" or ", trivial" when that's true, or a few words on how.
  - `Skip`: say why in a few words, e.g. "already like this on dev" or "separate apps".
  - `Decide`: the user or client must choose; give your leaning in a few words.
  - `Check`: it needs a manual or staging check; say what to check.
- No severity column, no failure-scenario paragraphs, no file list. Keep the `file:line` and the scenario for each row to yourself, ready for when the user asks "explain #3".
- If nothing survived verification, say so in one line and name the lenses you checked.
- If the change is uncommitted, say once that the review covers the working tree.

## 6. After the user chooses

This skill is read-only. Fix only the rows the user picks, following their global rules: use Edit/Write, run the project's tests and type checks, then stop and list the changed files for review. Don't commit or push.
