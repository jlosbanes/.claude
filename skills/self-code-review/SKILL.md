---
name: self-code-review
description: Review the current diff, a branch or a PR for bugs and risks, and report the verified findings as two short tables, "Fix" and "Decide", tagged by type (Business Behaviour, Code Level, AI Behaviour, Security, Data, Performance, Test Coverage, Maintainability). Use this when the user types /self-code-review, or asks to review their changes, a branch or a PR and wants the findings in their table format. Read-only: it never edits code.
argument-hint: "[PR number, URL, branch or path]"
---

# Self Code Review

Review a change the way the built-in `/code-review` does: find real bugs and risks, verify each one against the code. But report them as two scannable tables, one of fixes to make and one of choices for the user, instead of long failure-scenario paragraphs.

Don't call the `ReportFindings` tool. Print the tables as text.

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
- When reading can't settle it, run a test or a small verification script, following the user's global rules for those. If it still can't be settled, keep it in the Decide table as "Check: <how>".
- Drop style nits a formatter or linter would catch, and anything the user already decided.

## 5. Report

Split the findings into two tables:

- **Fix**: the findings you'd fix without needing the user's input.
- **Decide**: everything that needs the user's call: product choices, manual checks, and findings you'd skip.

Give every row a severity:

| Severity | Meaning |
|---|---|
| Critical | Silent data loss or corruption, wrong money or stock, or a security hole, in a normal flow |
| High | A wrong result users will hit in normal use |
| Medium | Wrong in a less common flow, or a cost users notice (slow screens, extra requests) |
| Low | Rare edge cases, cosmetic issues, small drift from the spec or design |

Rank each table by severity, most severe first. Reply with exactly this shape:

```markdown
**Fix**

| # | Severity | Type | Issue | Fix |
|---|---|---|---|---|
| 1 | High | Code Level | Saving with every field blank creates an empty reference row | Skip the save if blank, trivial |
| 2 | Low | Maintainability | The same rule is computed twice in the Summary section | Reuse one helper, trivial |

**Decide**

| # | Severity | Type | Issue | Recommend |
|---|---|---|---|---|
| 3 | High | Business Behaviour | Job Numbers like "N/A" end in "A", so they count as Apex Insurance | Lean: ignore "N/A" (none in local data) |
| 4 | Medium | Business Behaviour | Archived jobs still show on the board until refresh | Check: archive one on staging |
| 5 | Low | Security | Admins can edit totals through the API, skipping the audit log | Skip: admins are trusted |
```

Then one closing line: which rows to fix and the decisions needed, e.g. "Fix all? Your call on the Decide rows." When only some fixes are worth doing now, name them by severity: "Fix the Critical and High rows?"

Rules for the tables:
- **Issue:** one plain-language line, about 15 words at most. Say what goes wrong for whom, not how the code is built. Name screens and fields the way the product does. Add a code identifier only when it's the clearest pointer.
- **Fix** (first table): how to fix it in a few words; end with ", small" or ", trivial" when that's true.
- **Recommend** (second table): start with one of these words:
  - `Lean`: the user or client must choose; give the option you'd pick in a few words.
  - `Check`: it needs a manual or staging check; say what to check.
  - `Skip`: why it's not worth fixing, in a few words, e.g. "already like this on dev" or "separate apps".
- Leave out a table that has no rows.
- **#:** number the rows straight through both tables (Fix 1–2, then Decide 3–5), so the user can point at any row by its number alone. When re-issuing the tables, keep each row's number; don't renumber.
- No failure-scenario paragraphs, no file list. Keep the `file:line` and the scenario for each row to yourself, ready for when the user asks you to explain one.
- If nothing survived verification, say so in one line and name the lenses you checked.
- If the change is uncommitted, say once that the review covers the working tree.
- When re-issuing the tables in the same conversation, drop rows the user has already resolved.

## 6. After the user chooses

This skill is read-only. Fix only the rows the user picks, following their global rules: use Edit/Write, run the project's tests and type checks, then stop and list the changed files for review. Don't commit or push.
