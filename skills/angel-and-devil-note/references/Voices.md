# Gemini TTS prebuilt voices

Names for `settings.yaml` → `voices.angel` / `voices.devil` (and `--angel-voice` / `--devil-voice`).

Sources:
- Tendencies: [Gemini API — Text-to-speech](https://ai.google.dev/gemini-api/docs/speech-generation)
- Gender: [Cloud Text-to-Speech — Gemini-TTS](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts)

Preview in [Google AI Studio](https://aistudio.google.com/).

## Current defaults

| Role | Voice | Gender | Tendency |
|------|-------|--------|----------|
| Angel | `Leda` | Female | Youthful |
| Devil | `Puck` | Male | Upbeat |

## Full list

| Voice | Gender | Tendency |
|-------|--------|----------|
| `Achernar` | Female | Soft |
| `Achird` | Male | Friendly |
| `Algenib` | Male | Gravelly |
| `Algieba` | Male | Smooth |
| `Alnilam` | Male | Firm |
| `Aoede` | Female | Breezy |
| `Autonoe` | Female | Bright |
| `Callirrhoe` | Female | Easy-going |
| `Charon` | Male | Informative |
| `Despina` | Female | Smooth |
| `Enceladus` | Male | Breathy |
| `Erinome` | Female | Clear |
| `Fenrir` | Male | Excitable |
| `Gacrux` | Female | Mature |
| `Iapetus` | Male | Clear |
| `Kore` | Female | Firm |
| `Laomedeia` | Female | Upbeat |
| `Leda` | Female | Youthful |
| `Orus` | Male | Firm |
| `Pulcherrima` | Female | Forward |
| `Puck` | Male | Upbeat |
| `Rasalgethi` | Male | Informative |
| `Sadachbia` | Male | Lively |
| `Sadaltager` | Male | Knowledgeable |
| `Schedar` | Male | Even |
| `Sulafat` | Female | Warm |
| `Umbriel` | Male | Easy-going |
| `Vindemiatrix` | Female | Gentle |
| `Zephyr` | Female | Bright |
| `Zubenelgenubi` | Male | Casual |

## Pairing ideas

- **Angel-leaning:** `Sulafat`, `Aoede`, `Achernar`, `Vindemiatrix`, `Leda` (Female) / `Achird` (Male)
- **Devil-leaning:** `Fenrir`, `Algenib`, `Orus`, `Sadachbia`, `Puck` (Male) / `Pulcherrima` (Female)

Gemini also offers an Extended Voice Library, Voice design, and Voice replication; this skill’s `speak.py` currently expects **prebuilt** names like the table above.
