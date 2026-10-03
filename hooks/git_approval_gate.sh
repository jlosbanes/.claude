#!/usr/bin/env bash
# Claude Code PreToolUse hook: force a permission prompt before any commit, push, or PR create/merge.
#
# Every Bash command Claude runs is checked. If it would commit, push, or open/merge a pull
# request, Claude Code shows a permission prompt and waits for the user, in every permission
# mode. Approval is per command; nothing carries over. Anything else passes through untouched.
#
# Dependencies: bash only (built-in regex matching). No Python, Node, jq, or grep.
# Fail-closed: if the command cannot be read from the hook input, it asks anyway.

payload=$(cat)

ask() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Approval gate: %s. Review the changes in your IDE, then approve or deny."}}\n' "$1"
  exit 0
}

# Pull the command out of the hook JSON: "command":"<JSON-escaped string>".
json_cmd='"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)"'
[[ $payload =~ $json_cmd ]] || ask "could not read the command, so asking to be safe"
cmd=${BASH_REMATCH[1]}  # still JSON-escaped: quotes appear as \" and newlines as \n

# Building blocks (POSIX extended regex, matched against the escaped command text).
before='(^|[^[:alnum:]_.-]|\\[nrt])'                  # start, separator, "/", or an escaped newline/tab
after='([^[:alnum:]_-]|$)'                             # "push" but not "push-notifications"
token="(\\\\\"([^\\\\]|\\\\[^\"])*\\\\\"|'[^']*'|[^[:space:]]+)"  # \"quoted value\", 'quoted value', or bare word
git_opts="([[:space:]]+(-[Cc][[:space:]]+${token}|--?[[:alnum:]_.-]+(=${token})?))*"  # -C dir, -c k=v, --no-pager...

git_commit="${before}git${git_opts}[[:space:]]+commit${after}"
git_push="${before}git${git_opts}[[:space:]]+push${after}"
gh_pr_create="${before}gh[[:space:]]+pr[[:space:]]+create${after}"
gh_pr_merge="${before}gh[[:space:]]+pr[[:space:]]+merge${after}"

hits=()
[[ $cmd =~ $git_commit ]]   && hits+=("git commit")
[[ $cmd =~ $git_push ]]     && hits+=("git push")
[[ $cmd =~ $gh_pr_create ]] && hits+=("gh pr create")
[[ $cmd =~ $gh_pr_merge ]]  && hits+=("gh pr merge")

if (( ${#hits[@]} )); then
  joined=$(IFS=,; echo "${hits[*]}")
  ask "this command runs ${joined//,/, }"
fi
exit 0  # no output = no opinion; the normal permission flow continues
