# Translating HUman

`fr.json` is the master. Each translation is a JSON file with exactly the same structure and keys.

Rules:
- Same keys, same array lengths: `chapters` 10, `questions` 3, `title_land` 3 lines, `title_port` 4 short lines, `caps` 27 items in the same order.
- Keep placeholders `{0}` and `{1}` exactly. Keep math symbols, formulas, units and arrows. Use the local decimal separator and number grouping, for example "0.72" and "384,400 km" in English and "0,72" in Spanish.
- `s.pct` is the percent format, for example "{0}%" in English and "{0} %" in French.
- Tone: an intimate, poetic first-person reflection by Mathieu. Write short, natural sentences, not literal ones. Keep each caption about as long as the French. Lens lines (`lens_*`) must stay short, at most 45 characters.
- "Mathieu", "Claude", "LLM" and "HUman" stay as they are. Translate "IA" into the local term for AI.
- `name` is the language's own name, for example "English" or "中文". `dir` is "rtl" for Arabic, otherwise "ltr". `cjk` is true only for Chinese and Japanese, where there are no spaces between words.
- `glyphs`: exactly 26 characters typical of the script, with no spaces. They are used as flickering particles, like letters. For Chinese or Japanese, use common characters or kana.
- `words` is the AI demo, where a sentence is built token by token:
  - `groups` holds 4 clusters: nature nouns (about 9), "I" and thinking verbs (about 9), grammatical or function words (about 14), and big concepts (about 6).
  - `start` plus the 8 picked tokens form the sentence.
  - `steps` has 8 steps with 4 candidates each, `[token, probability]`. Keep the French probabilities. Every candidate token must appear in `groups` with exactly the same spelling.
  - `pick[j]` is the index of the chosen candidate at step j. Exactly one step must pick a candidate other than index 0, to show that the draw is not always the most probable one. Pick the sea over the moon if you can.
  - `start` followed by the picked tokens, joined with `join` (" " or "" for CJK), must read as a natural sentence meaning "I look at the sea and I think of the universe". Tokens may be multi-word, such as "look at", or a single character. For SOV languages, reorder the sentence naturally, still in 8 steps, with plausible alternatives at each step.
- `predict.sentence` + `words.join` + a `predict.rows` word must read naturally, as in "The cat drinks" + "milk". Use a sentence that ends right before the blank, rephrasing if needed. Keep the 4 options (milk, coffee, tea, blood) and their probabilities.
- `amino`: the amino acid names in the language. `stop` means "end of the sentence".
- Validate: the JSON must load, its keys must match fr.json (including all keys of `s`), and the array lengths must match.
