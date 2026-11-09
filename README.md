# DOT-AGENT-ANGEL-AND-DEVIL

<p align="center">
  <img src="logo.jpg" alt="DOT-AGENT-ANGEL-AND-DEVIL" width="720" />
</p>

<p align="center">
  <strong>Double-perspective contrarian feedback system</strong><br />
  <a href="README_ja.md">日本語</a>
</p>

An Agent Skill that has an **Angel** 😇 and a **Devil** 😈 read your notes, docs, or web pages and trade impressions in a short back-and-forth.

- The Angel finds concrete strengths and reframes setbacks with warm encouragement.
- The Devil teases slips and temptations—and smuggles in **one real critique** per turn.

---

## What’s included

| Path | Description |
|------|-------------|
| `skills/angel-and-devil-note/` | Agent Skill (`SKILL.md` + personas + optional TTS) |
| `skills/.../references/Angel.md` | Angel persona |
| `skills/.../references/Devil.md` | Devil persona |
| `skills/.../scripts/speak.py` | Optional Gemini TTS for reading the dialogue aloud |
| `examples/` | Sample dialogues + TTS audio (`sample-en.mp3` / `sample-ja.mp3`) |
| `install.sh` | Symlinks skills into `~/.agents/skills/` |

---

## Install

Requires a shell environment where Agent Skills are loaded from `~/.agents/skills/` (e.g. Cursor / Codex-compatible agents).

```bash
./install.sh
```

You will be prompted `[y/N]` before each link is created. Preview without changing anything:

```bash
./install.sh --dry-run
```

This creates a symlink:

```text
~/.agents/skills/angel-and-devil-note  →  <repo>/skills/angel-and-devil-note
```

---

## Usage

### Slash command

In Agent chat, type `/` and select the skill (or type it out):

```text
/angel-and-devil-note @notes/today.md
```

More examples:

```text
/angel-and-devil-note @notes/today.md
/angel-and-devil-note @README.md append the dialogue to the end
/angel-and-devil-note @notes/today.md speak it aloud
/angel-and-devil-note https://example.com/article
```

Prefer `@path` when pointing at a file or folder so the agent attaches it as context (e.g. `@notes/today.md`, `@docs/`). Plain paths also work, but `@` is clearer in Cursor / Codex-style chats.

### Natural language

You can also ask without the slash command:

- “Have the angel and devil read @notes/today.md.”
- “Angel/devil take on this note.”
- “Review this URL with angel and devil.”

If no source is given, the skill asks you for one (web page, file, stdin, etc.).

### Example

**Input** (`@notes/today.md`):

```markdown
# Tasks
- [ ]
- [ ]
- [ ]
# Notes
Tried scrambling eggs that were four days past their best-by date. Probably not great for the body, but I doubt it's as bad as people say. My mouth got too eggy, so I chased it with Castella cake. Upside: I woke up feeling pretty good this morning. And development on this angel-and-devil skill moved along reasonably well.
```

**Output:**

```markdown
😇 **Angel**: Good morning! Waking up feeling refreshed and actually cooking yourself a warm plate of scrambled eggs is such a wonderful way to start the day! Even if the eggs were four days past their best-by date, making the smart call to cook them thoroughly instead of eating them raw shows great practical judgment! And chasing them with Castella cake gave your brain a nice morning glucose boost—plus, look at how much solid progress you've already made on developing this Angel and Devil skill before the day has barely begun!

😈 **Devil**: Pfft, four-day-expired scrambled eggs chased down with Castella sponge cake? What kind of chaotic morning combo is that?! And hold on—"my mouth tasted too eggy, so I washed it down with Castella"? You're literally trying to neutralize egg flavor with a cake made almost entirely of eggs and sugar! You're still half-asleep, aren't you?! Better yet, look at those three empty checkboxes under Tasks—totally blank! After all, you can't fail a goal you never bothered to write down, right? Brilliant lifehack! Just leave that task list blank forever, demolish the rest of the Castella loaf, and crawl right back into bed!

😇 **Angel**: Oh, stop being so dramatic, Devil! That sweet Castella finish clearly worked like a charm, because the note explicitly says they woke up feeling great—and that's a win in my book! Besides, leaving those task boxes open right now just means they jumped straight into building and shipping this skill instead of overthinking a massive to-do list. Once you grab a refreshing glass of water, how about we crown just one tiny, easy task as today's main win?

😈 **Devil**: Heh heh heh, "made decent progress on the skill," huh? Sounds to me like you're procrastinating on the real, heavy work by tinkering with shiny side-tools again—classic developer escapism! Well, here's the beauty of your morning gamble: if those "four-day vintage eggs" start staging a rebellion in your stomach around noon, you've got a bulletproof medical excuse to cancel every single thing on your schedule today! Call it a tactical food-poisoning holiday and slack off guilt-free!

😇 **Angel**: Your stomach is going to be completely fine, don't listen to him! Getting up early, writing your daily log, and wiring up multi-speaker voice synthesis for this skill is already a huge victory for the morning! Go ahead and pour yourself a nice cup of water or warm tea to treat your stomach kindly, jot down just one small finish line for today, and enjoy a fantastic, productive day! I'm cheering you on!
```

**Listen:** [English audio](examples/sample-en.mp3) · [Japanese audio](examples/sample-ja.mp3)

(Source transcripts: [`sample-en.md`](examples/sample-en.md) · [`sample-ja.md`](examples/sample-ja.md). Generated with the optional Gemini TTS path below.)

### Output options

By default, dialogue goes to **stdout**. You can also ask for:

| Mode | Behavior |
|------|----------|
| Separate file | Write the exchange to a path you specify |
| Append to source | Append as a blockquote at the end of the original file |
| Speak aloud | TTS (only when you explicitly ask—see below) |

Typical length: about **2–3 exchanges**, ending on a clean beat (the Angel usually closes).

### Dialogue markers

```markdown
😇 **Angel**: …
😈 **Devil**: …
```

(Japanese markers `天使` / `悪魔` are also supported.)

---

## Optional: text-to-speech

Requires `GEMINI_API_KEY`. Without it, the skill skips speech and keeps text-only output.

**Cost / consent:** TTS calls the Gemini API and may incur charges on the Google account / project tied to `GEMINI_API_KEY`. Speech runs only when you explicitly ask, and the agent must confirm with you before generating audio. `speak.py` also prompts for confirmation (use `-y` / `--yes` only after you have already approved).

```bash
cd skills/angel-and-devil-note
python3 -m venv scripts/.venv
scripts/.venv/bin/pip install -r scripts/requirements.txt

export PYTHON=scripts/.venv/bin/python
# Save WAV (omit -y to get an interactive confirm prompt)
$PYTHON scripts/speak.py path/to/dialogue.md -o out.wav -y
# Play
$PYTHON scripts/speak.py path/to/dialogue.md --play -y
# Parse check only (no API call)
$PYTHON scripts/speak.py path/to/dialogue.md --dry-run
```

Defaults live in [`settings.yaml`](skills/angel-and-devil-note/settings.yaml) (model, voices, styles, per-language speed). Do not put API keys there.

`language` sets the banter language used when the request does not name one (`ja`, `en`, …; `auto` matches the language you write in). Asking for a language in the request (e.g. "in Japanese") always wins.

Prebuilt voice names: [`Voices.md`](skills/angel-and-devil-note/references/Voices.md).

Override precedence: CLI flags > `GEMINI_TTS_*` env vars > `settings.yaml` > built-ins.

---

## Personas (summary)

| | Angel 😇 | Devil 😈 |
|---|----------|----------|
| Role | Praise specific effort; reframe setbacks | Spot unfinished work, excuses, indulgence |
| Style | Warm, concrete, motivating | Sharp, teasing, tempting |
| Rule | Push back on cynicism; leave the user affirmed | Hide **one true insight** inside the temptation |

Full specs: [`Angel.md`](skills/angel-and-devil-note/references/Angel.md) · [`Devil.md`](skills/angel-and-devil-note/references/Devil.md)

---

## License

[PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) — see [`LICENSE`](LICENSE).

This is **source-available / non-commercial**, not OSI open source.

**Intent (see also the non-binding notes in `LICENSE`):**

- **Allowed:** personal use at work when the skill is incidental to your own tasks (e.g. reviewing your own notes while employed).
- **Not allowed:** use where this project (or a substantially similar derivative) is a primary product, paid feature, commercial service, or otherwise central to generating revenue.
- **Unsure?** Ask the copyright holder for written permission or a separate commercial license.
