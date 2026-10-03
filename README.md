# .claude

Personal Claude Code configuration (WSL / Ubuntu).

| File | Purpose |
|---|---|
| `CLAUDE.md` | Global instructions loaded in every session |
| `settings.json` | Model, auto mode default, disabled skills, hooks |
| `hooks/git_approval_gate.sh` | Forces an approval prompt before any commit, push, or PR create/merge (bash only) |
| `hooks/verify_git_approval_gate.py` | Test for the gate: `python3 hooks/verify_git_approval_gate.py` should print CONFIRMED |

Only allow-listed files are tracked (see `.gitignore`); credentials and session data never are.

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
   `printf '/verify_*.py\n/verify-*.js\n' >> ~/.config/git/ignore`
5. Install and sign in to the GitHub CLI (`gh auth login`, SSH protocol).
