---
name: self-client-respond
description: Draft an email reply to a client in the user's house style — "Hello, <name>" greeting, a few short plain-language bullets a non-technical reader understands at a glance, and the "Warm Regards, John Christian L." sign-off — with every claim about the product checked first. Use this whenever the user wants to reply or respond to a client, answer a client's question or request, explain a bug, change or feature to a client, confirm or decline work, give a client an update, or pastes a client's email or screenshot and asks what to say back, even if they don't say "email". Not for internal messages to teammates, PR descriptions or commit messages.
argument-hint: "[the client's message, or what the reply should say]"
---

# Respond to Client

Write an email reply a client can read in under a minute and act on without needing to ask a follow-up question.

## 1. Understand what the client is asking

- Read the client's message (pasted text, screenshots or the earlier thread). List every direct question and request in it, so the reply answers all of them and adds nothing they didn't ask about. Remarks in passing, such as "not sure why this was set up initially", aren't requests; leave them unanswered, since explaining them adds length and can sound defensive.
- Note the name they sign with and the words they use for things ("the Assigned queue", "requests"). Reuse their words; it shows you understood them and avoids introducing new terms.
- If the user gave the gist ("tell her yes, we'll do it"), that's the decision. Your job is to word it well, not to reopen it.

## 2. Get the facts right

- Before explaining how something works, why something happened, or what will change, check it in the code, data or docs, following the global evidence rules. A wrong explanation sent to a client is hard to take back and costs trust.
- Don't promise a date, cost, scope or outcome the user hasn't confirmed. When the client asks for one, put a placeholder such as [date] in the email and flag it in your notes.
- If something can't be verified, leave it out of the email and tell the user (see step 4).

## 3. Write the email

Use this frame. It's plain text, so it pastes cleanly into any mail client:

```text
Hello, <client's first name>

<the answer or outcome in one short line, or labelled groups that answer directly>

- <point>
- <point>

<optional one-line next step or question>

Warm Regards,
John Christian L.
```

### Content
- **Answer first.** Open with the answer or the outcome ("Yes, we can do that."). For a "why" question, go straight into short labels that answer it ("Why it's in Assigned:"), each followed by its bullets.
- **Report a finished change as how things work now.** Open with "Here is now how the application behaves:" and describe the behaviour in the present tense. Leave out release timing and go-live dates. The user sends these emails once the change is live, so if it isn't live yet, say so in your notes rather than in the email.
- **Leave out backstory.** Why something was built a certain way, when it was added or who set it up doesn't help the client act, so skip it unless they asked directly.
- **One idea per bullet, one short sentence where possible.** Two to six bullets covers most replies. More than that usually means the email is explaining internals the client doesn't need.
- **Describe what the client sees or needs to do**, in the product's own terms: screen names, button labels and statuses as they appear on screen. Leave out how it's built, so no file, function, branch, field or table names and no words like deploy, cron, migration or API.
- **Use their own example when it helps.** A detail from their message ("Your screenshots show exactly this") proves you looked and makes the explanation concrete.
- **End with what happens next, only when there's something:** what you'll do, what you need from them, or a question they can answer with a word or two.

### Style
- Plain, warm and confident. Skip filler ("I hope this email finds you well", "Please don't hesitate to reach out") and jargon. One brief apology is fine when something actually went wrong on our side; more reads as defensive.
- Keep it short. A one-question reply usually fits in three to five bullets; padding makes the answer harder to find.
- Plain-text formatting only: "-" bullets and plain labels, no bold, headings, tables or emoji. Many mail clients show markdown as raw symbols.
- Match the client's spelling (Australian clients write "organisation", "colour").
- Greet them by first name exactly as they sign. For a shared inbox, use the team name ("Hello, Brightwater Customer Service"). If you don't know the name, write [name] and flag it.

See `references/example.md` for complete replies written this way.

## 4. Hand it over

Reply to the user in their usual style, in this order:

1. One line naming the audience, e.g. "Written for: Maria (Brightwater Customer Service)."
2. The email in a single ```text fenced block, so it can be copied exactly.
3. Brief notes for the user, not the client: anything unverified under **HYPOTHESIS:** (with what would confirm it), any placeholders to fill in, and the key checks under **FACT:** with their sources.

Don't send the email yourself. Sending is outward-facing and can't be undone, so even when a mail connector is available, create a draft or send only after the user says so for that specific email.
