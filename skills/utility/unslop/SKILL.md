---
name: unslop
description: Final prose pass for human-facing output — lead with the conclusion, cut filler, full sentences. Use before saving a spec, review, research file, or any document a human will read, or when asked to make text readable.
---

# Unslop

The final pass over prose a **human** will read. `writing-for-agents` covers documents agents consume; this covers everything else — specs, reviews, research findings, reports, READMEs. Skills that produce human-facing files (`to-spec`, `review`, `research`) run their output through this before saving.

The standard is the reader's time: every sentence either informs a decision or goes. Apply each rule as a rewrite, not a checklist to report on.

## Shape

- **Lead with the conclusion.** The first sentence answers the question; reasoning and detail follow for readers who want them.
- **Full sentences.** Brevity comes from cutting redundant sentences, never from dropping the words that carry meaning — no fragments, no `A → B → fails` arrow chains, no invented abbreviations the reader must decode.
- **Say it once.** State the point where it belongs and trust it; a summary that restates the section above it is the section written twice.
- **Answer, don't narrate.** Cut restatements of the request, descriptions of the process ("I then examined…"), and announcements of what the document is about to say.

## Sentences

- **Cut puffery.** Adjectives that grade the work ("robust", "comprehensive", "seamless", "powerful") assert what the content should demonstrate. Delete them; keep the fact.
- **Cut filler transitions.** "It's worth noting that", "Additionally, it should be mentioned" — the sentence works without the ramp. Start at the point.
- **Cut chatbot phrases.** "Great question", "I hope this helps", "Feel free to" — a document has no small talk.
- **Commit or attribute.** Replace hedges ("might potentially", "could arguably") with the claim and its evidence, or with a named uncertainty: what is unknown and what would settle it.
- **Concrete over abstract.** "Leverages advanced capabilities" says nothing; the specific mechanism, number, or behavior says it all.

## Never touched

Identifiers, file paths, commands, and quoted output are written in full, exactly as they are — precision is the one place verbosity wins.
