---
name: describe-pr
description: Write a pull request description in the user's house format (Why, What with a Before/After table, How to manually test, Worth knowing) in plain, client-facing language, with every claim checked against the code. Use this whenever the user asks to describe, write up, document or fill in a PR, pull request or merge request, wants a PR body or summary for reviewers or QA, or is about to open a PR and needs its description, even if they don't name the format. Not for reviewing a PR's code for bugs.
argument-hint: "[PR number, URL or branch]"
---

# Describe PR

Write the description of a pull request so a reviewer, tester or product owner can see why it exists, what changes for the people using the product, and how to check it themselves, without reading the code.

## 1. Find the change

Target given by the user: $ARGUMENTS

If none was given, use the current branch.

- **PR number or URL:** `gh pr view <target> --json number,url,title,body,baseRefName,headRefName,commits` and `gh pr diff <target>`.
- **Branch, or nothing given:** check for an open PR with `gh pr view <branch> --json number,url,title,body,baseRefName`. If there is none, the base is the repo's default branch (`gh repo view --json defaultBranchRef`). Fetch first so the base is current, then read `git log <base>..<branch>` and `git diff <base>...<branch>`.
- If the project's CLAUDE.md or CLAUDE.local.md says not to use `gh` (for example, a work org it can't reach), use git only and skip the offer to update the PR.
- Uncommitted or unpushed work isn't part of the PR. If there is some, say so and ask whether to include it, so you don't describe code that reviewers won't see.

Read the existing PR body, the commit messages and any linked issue to learn the intent, but treat them as claims to check, not as facts.

## 2. Understand what actually changes

The diff alone rarely shows what a person will experience. For each change:

- Read the changed code **and** the code around it: callers, the screens and API responses it feeds, and the old version (`git show <base>:<path>`). That way the Before column is real, not inferred.
- Find the exact words users see (button labels, screen titles, toasts, error messages, menu paths) in the UI code or translation files. A test step that names a label that doesn't exist wastes a tester's time.
- Look for test helpers the project already has, such as seed data, dev tools, test cards and fixtures, so the test steps can use them.
- Work out concrete figures for the examples. If a number comes from a calculation (fees, totals, tax, limits), get it by running the project's own code or a small verification script as the global rules describe. Don't do the arithmetic in your head.
- Note anything a reviewer or deployer needs that the UI doesn't show: migrations and their effect on existing data, new settings or env vars with surprising defaults, deferred work, known gaps, costs and risks.

If a claim can't be verified, leave it out of the description and report it to the user (see step 4).

## 3. Write it

Use exactly these four sections in this order, with `##` headings. Put nothing above `## Why`, because the PR title already names the change.

```markdown
## Why

- **<The problem, stated as what went wrong for a person or the business.>** <A concrete instance with real numbers or a real sequence of events.>

## What

- **<A change, stated as what people now see, get or can do.>** <One or two sentences of detail.>

| Situation | Before | After |
|---|---|---|
| <A concrete situation> | <What happened before> | <What happens now> |

## How to manually test

1. **<Scenario title stating the outcome to confirm>**
   - As the <role>, <action, with the exact path: Account → Payments → Payment history>.
   - <What they should see, e.g. "It should show A$1,100.">
   - Before: <what used to happen, when the contrast helps>.

## Worth knowing

- **<A non-obvious consequence, limitation or caveat.>** <Why it matters and what, if anything, someone must do.>
```

### Why
- Write 1 to 3 bullets. Each one names a problem that existed before this PR, from the point of view of the people affected. "Refactored X" or "Added Y" is not a reason.
- Back each bold sentence with a specific example: an amount, a sequence of events or a count.

### What
- Write one bullet for each behaviour change people will notice. Start with who it affects, in the present tense ("Customers now…", "An invoice can't be sent until…").
- Also cover guards against bad states, and anything that deliberately stays the same ("What's already sent keeps its price") when a reviewer would otherwise wonder about it.
- Add the Before/After table whenever behaviour changes. Each row is a concrete situation, cells are short, and figures match the examples elsewhere in the description. Skip the table only when nothing visible changes, and then say so in a bullet ("No change for users; …").

### How to manually test
- Write one numbered scenario for each behaviour in What. Its bold title states what should be true ("A tradie without a bank account can't send an invoice").
- Write steps as a person doing things: "As the customer, open…". Say so explicitly when the scenario switches roles.
- Give a tester everything they need without guessing: setup, exact amounts, test data, which tool fills a form, and where to check results outside the app (for example, a payment provider's dashboard).
- Put an expected result after every meaningful action ("It should…", "The toast should…").
- End with a cleanup step when a scenario changes shared settings.
- For changes with no UI, the steps can be API calls or commands, written the same way.

### Worth knowing
- Cover what a reviewer, tester or deployer would want to know before merging: defaults on existing environments, migrations, settings someone must enter, money or security implications, edge cases not handled, and work deliberately deferred.
- Each bullet is a bold headline stating the consequence, followed by the reason and anything someone must do about it.
- If there is genuinely nothing, write `- Nothing beyond the changes above.` Keep the section either way, so the format stays predictable.

### Style (from the user's global response style)
- Use plain, client-facing language that a product owner could forward as-is. Name people and things the way the product does (the roles and screen names in the UI), not by class, function, file or table names. Code identifiers belong only where someone must act on them, such as a command to run or a setting to set, and then in backticks.
- Lead every bullet with its point in bold. Keep to one idea per bullet and one or two sentences after the bold lead.
- Be concrete: real amounts, real labels, real counts. Use the same figures throughout so the table, examples and test steps agree.
- Leave out filler and "This PR…" openers, and don't walk through the diff file by file. Never add AI attribution: no "Generated with Claude Code", no co-author lines, no session links.
- Scale to the change. A one-line fix may need one bullet per section, one table row and one test scenario.

See `references/example.md` for a complete description written this way.

## 4. Hand it over

Reply in the user's usual style, in this order:

1. One line naming the audience, e.g. "Written for: reviewers and QA testing this PR."
2. The description in a single ```markdown fenced block, so it can be copied exactly.
3. Brief notes for the user, not for the PR: anything you couldn't verify under **HYPOTHESIS:** (with what would confirm it), then the key checks you made under **FACT:**, with `file:line` sources.
4. If the existing PR body has content the new one drops (issue links such as "Closes #123", screenshots, checklists), list it and ask whether to keep it.
5. Offer the next step, and wait for a yes before doing it:
   - **PR exists:** update it. Save the body to a file outside the repo (the session scratchpad) with the Write tool, then run `gh pr edit <number> --body-file <file>`. Other people can see a PR edit, so this needs the user's go-ahead every time.
   - **No PR yet:** offer to open one with this body in a single step: `gh pr create --title "<type>: <summary>" --body-file <file>`, with the title in the user's commit format. Pushing the branch and creating the PR each need the user's explicit approval under the global git rules.
