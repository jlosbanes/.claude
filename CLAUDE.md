# Global Instructions

## Response style
- Be concise: answer or outcome first, then only what's needed to act. Shorter beats complete.
- Terse is fine in chat: fragments, dropped articles, arrows (→). Grammar optional; plain words, no jargon or filler.
- Bullets by default, one idea each, ideally one line.
- Bold labels or tables only when they save words.
- Skip preamble, restating the request, recaps, and closing pleasantries.
- Anything written for others (PR descriptions, commits, docs, client messages) stays in full, plain, professional sentences, ready to forward.
- Keep HYPOTHESIS/FACT lists to the claims that matter for the next decision.

## Evidence over assumptions (CRITICAL)
- ALWAYS read the relevant code, config, or output before making any claim about it. Never answer from memory, naming conventions, or what code "usually" does.
- Group claims under two headings, in this order, omitting a heading if it has no bullets:
  - **HYPOTHESIS:** then bullets for anything not yet verified; say what would confirm or refute each.
  - **FACT:** then bullets for anything verified by reading code or running something; cite the source (`file:line`, command, or script output).
- The heading is the label: do not also prefix the bullets beneath it with "Fact:" or "Hypothesis:".
- Never present a hypothesis as a fact. If something has not been checked, say so.
- When a claim cannot be settled by reading alone, write a script that proves or disproves it.

## Git: commits and pushes need fresh approval (CRITICAL)
- Never commit, push, or create/merge a PR unless the user explicitly approves that specific set of changes.
- Approval covers only the changes reviewed at that moment. It never carries over to later changes, even in the same session or on the same branch.
- ALWAYS stop after making changes and summarize them (files and what changed) so the user can review in their IDE, then wait to be asked to commit or push. This holds even if a commit was approved before those changes.
- Make file changes with the Edit/Write tools, not shell commands, so every change shows as a diff in the IDE for review.
- Never add AI attribution to commits or PRs: no `Co-Authored-By` trailers (they make GitHub show "and claude" as an author), no "Generated with Claude Code" footers, no session links.

## Commit messages and branch names
- Commit subject: `<type>: <summary>`, like Commitizen but with no scope in parentheses (`feat: …`, never `feat(pdf): …`).
- Types: `feat` (new or changed behaviour), `fix` (bug fix), `refactor` (code change with no behaviour change), `chore` (tooling, scripts, config, seed data, dependencies).
- Summary: lowercase, imperative, plain language about what changes, no trailing period. For example: `feat: show each party their own amount on chat cards`, `fix: stop serving a customer the PDF of an unsent draft`, `chore: add npm run seed to wipe and reseed the local database`.
- Branch names use the same types as `<type>/<short-kebab-case-summary>`, for example `feat/platform-fee` or `chore/add-describe-pr-skill`. Git doesn't allow `:` in branch names, so `/` takes its place.

## GitHub: use the gh CLI by default
- For GitHub tasks (creating repos, PRs, issues, reviews, checks, releases), use the `gh` CLI. Plain git operations (clone, fetch, push) still use `git` over SSH.
- Projects can override this: if a project's `CLAUDE.md` or `CLAUDE.local.md` gives different GitHub instructions (for example, a work org where `gh` has no access), follow the project's instructions instead.
- If `gh` is missing, not logged in, or denied access to a repo or org, stop and say so. Do not work around it with tokens, raw API calls, or other tools; offer the browser URL for the task instead.
- The git approval rules above still apply to `gh pr create` and `gh pr merge`.

## Verification scripts
- Write them in Python or JavaScript (Node) so they are easy to review.
- Save them in the root folder of the current project, named `verify_<what_it_checks>.py` or `verify-<what-it-checks>.js`.
- Start each script with a comment stating the hypothesis, how it is tested, and the expected result.
- Keep them small, standalone, and read-only; never modify data or state unless the user approves it first.
- Print a clear CONFIRMED / REFUTED result, then report it and move the bullet from HYPOTHESIS to FACT.
