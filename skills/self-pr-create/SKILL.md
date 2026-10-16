---
name: self-pr-create
description: Take the current work from finished code to an open pull request in the user's usual order — /simplify, small commits, /self-pr-describe, then gh pr create — stopping for the user's approval before committing and again before pushing and opening the PR. Run only when the user types /self-pr-create.
argument-hint: "[base branch]"
disable-model-invocation: true
---

# Create PR

Ship the current work as a pull request: clean it up, commit it in small pieces, describe it, and open it with `gh`. Two approval stops are required by the user's global git rules. Never skip them, even if an earlier commit or PR in this session was approved.

## 1. Check the starting point

1. Current branch: `git branch --show-current`. If it is the repo's default or base branch (`development`, `main`, `master`), propose a branch name in the user's format `<type>/<short-kebab-case-summary>` and create it only after the user agrees.
2. Existing PR: `gh pr view --json number,url,state`. If an open PR already exists, stop and offer `/self-pr-describe` to update it instead.
3. Base branch:
   - Use `$ARGUMENTS` if given.
   - Otherwise follow the project's CLAUDE.md, CLAUDE.local.md or memory (for example, stacked PRs that base each branch on the previous feature branch).
   - Otherwise find the branch this one was cut from: among local branches and the default branch, take the one whose tip is an ancestor of `HEAD` with the fewest commits in `git log --oneline <candidate>..HEAD`.
   - Name the base you picked and why in your first reply, so the user can correct it before anything is committed.
4. Work in scope: `git status --short` and `git log <base>..HEAD --oneline`. Another Claude session may share this working tree, so only take files and hunks that belong to this work. Ask about anything you can't place.

## 2. Simplify

Run the `simplify` skill on this work only: the uncommitted changes plus the commits since the base. Apply its fixes.

After the cleanup, run only the quick checks the project has (typecheck, formatter). Don't rerun slow verify scripts or browser runs for a behaviour-preserving cleanup; say they weren't rerun.

**Stop 1.** Summarise what simplify changed (files and one line each), then propose the commits:
- small, one concern each, in the user's `<type>: <summary>` format (no scope in parentheses);
- the files or hunks in each.

Wait for the user to review the diff in their IDE and approve. Their approval covers exactly these commits.

## 3. Commit

Make the approved commits, staging only the listed files or hunks. Check `git log <base>..HEAD --oneline` matches the plan. Never add AI attribution: no co-author trailers, no generated-with footers.

## 4. Describe

Run the `self-pr-describe` skill on the current branch against the chosen base. Save the description it produces to a file in the session scratchpad with the Write tool, so `gh` can read it. Don't take up that skill's own offer to open the PR; this skill does that in step 5, after Stop 2.

**Stop 2.** Show, in this order:
1. Title: `<type>: <summary>`, in the user's commit format.
2. Base ← head branch.
3. The description, as `self-pr-describe` returned it.

Ask for approval to push and open the PR. A PR is visible to other people, so wait for an explicit yes.

## 5. Push and open

```bash
git push -u origin <branch>
gh pr create --base <base> --head <branch> --title "<type>: <summary>" --body-file <scratchpad file>
```

- Never force-push. If the push is rejected, stop and report why.
- If the project's instructions say to push elsewhere too (for example, Brightwater pushes to both Bitbucket and GitHub) or not to use `gh`, follow them. Where no CLI can open the PR, give the user the title and body ready to paste, and the URL to open.
- Don't merge. Merging is a separate request.

Reply with the PR link, the base it targets and the commits it contains.
