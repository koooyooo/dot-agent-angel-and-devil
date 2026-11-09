---
name: angel-and-devil-note
description: Has an angel and a devil read a given document and share their impressions of it.
---

## Steps
- Load content from a web page, file, stdin, etc.
    - If none is specified, ask the user
- Decide the output language
    - If the user names a language in the request, use it
    - Otherwise read `language` in [settings.yaml](settings.yaml): a code such as `ja` / `en` means write in that language; `auto` (or missing) means match the language the user is writing in
- Have the angel and devil share impressions of that content
    - Personas (always read these before writing the exchange; keep tone and roles):
        - Angel: [references/Angel.md](references/Angel.md)
        - Devil: [references/Devil.md](references/Devil.md)
        - The angel finds concrete strengths and praises them
        - The devil teases weaknesses and temptations, and smuggles in **one real critique** per turn
    - Dialogue flow
        - Keep the back-and-forth short—about 2–3 exchanges—and end on a clean beat
- Default output is stdout; depending on the user request, also support:
    - Write to a separate file
    - Append to the end of the source file as a blockquote
    - Speak aloud (only when the user explicitly asks)
        - **Required: get user approval before generating audio.** Gemini TTS may incur usage charges. Even on the first request, confirm that calling the API to synthesize speech is OK. If they refuse or are unclear, skip speech and keep text only. Do not run `speak.py` on your own
        - Prerequisite: `GEMINI_API_KEY` must be set. If missing, skip speech and keep text-only output
        - One-time dependency install (venv recommended):
            - `python3 -m venv scripts/.venv`
            - `scripts/.venv/bin/pip install -r scripts/requirements.txt`
        - Save the dialogue text to a file, then run (with `PYTHON=scripts/.venv/bin/python`):
            - Use `-y` only after the user has approved (skips the interactive confirm):
                - Save only: `$PYTHON scripts/speak.py path/to/dialogue.md -o out.wav -y`
                - Play: `$PYTHON scripts/speak.py path/to/dialogue.md --play -y`
            - Parse check (no API; no approval needed): `$PYTHON scripts/speak.py path/to/dialogue.md --dry-run`
        - Defaults live in [settings.yaml](settings.yaml) (language / model / voices / styles / per-language speed). Do not put API keys there
        - Override precedence: CLI (`--speed`, etc.) > env (`GEMINI_TTS_*`) > `settings.yaml` > built-ins
        - Speed changes other than `1.0` require `ffmpeg`
        - Use turn markers `😇 **Angel**:` / `😈 **Devil**:` (Japanese: `天使` / `悪魔`)
