# .claude

Personal Claude Code configuration (WSL / Ubuntu).

| File | Purpose |
|---|---|
| `CLAUDE.md` | Global instructions loaded in every session |
| `settings.json` | Model, auto mode default, no AI attribution, disabled skills |
| `skills/` | Personal skills, listed below |

Only allow-listed files are tracked (see `.gitignore`); credentials and session data never are.

## Skills

| Skill | What it does |
|---|---|
| `/self-client-respond [client's message]` | Drafts a client email reply: "Hello, &lt;name&gt;", short plain-language bullets, house sign-off, every claim checked first |
| `/self-code-review [PR, branch or path]` | Reviews a diff, branch or PR and reports verified findings as two short tables, Fix and Decide, with a severity per row |
| `/self-grill-me` | Interviews you in rounds of questions to stress-test a plan or decision. Copied from [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) (MIT) |
| `/self-pr-create [base branch]` | Takes finished work to an open PR: /simplify, small commits, /self-pr-describe, then `gh pr create`, pausing for approval before committing and before pushing |
| `/self-pr-describe [PR or branch]` | Writes a PR description as Why / What (with a Before/After table) / How to manually test / Worth knowing |
| `/self-pr-push [what to include or leave out]` | Commits this session's changes as small, one-concern commits, checks each one builds on its own, pushes, and lists the commits |

## Restore on a new machine

1. Install Claude Code, then let npm run its setup script during updates:
   `npm install -g @anthropic-ai/claude-code`
   `npm config set allow-scripts=@anthropic-ai/claude-code --location=user`
2. Create an SSH key and add the `.pub` to GitHub (and Bitbucket):
   `ssh-keygen -t ed25519 -C "<user>@<machine>" -f ~/.ssh/id_ed25519`
3. Clone this repo into place (move any existing `~/.claude` aside first):
   `git clone git@github.com:jlosbanes/.claude.git ~/.claude`
4. Git identity and global ignore for verification scripts:
   `git config --global user.name "jlosbanes"`
   `git config --global user.email "<email>"`
   `printf '/claude-verify/\n/verify_*.py\n/verify-*.js\n' >> ~/.config/git/ignore`
5. Install and sign in to the GitHub CLI (`gh auth login`, SSH protocol).
