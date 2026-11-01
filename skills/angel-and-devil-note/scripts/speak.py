#!/usr/bin/env python3
"""Read angel/devil dialogue aloud via Gemini TTS when GEMINI_API_KEY is set."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_SETTINGS_PATH = SKILL_DIR / "settings.yaml"

# Built-in fallbacks if settings.yaml is missing or incomplete.
BUILTIN_MODEL = "gemini-3.8-flash-tts"
BUILTIN_ANGEL_VOICE = "Kore"
BUILTIN_DEVIL_VOICE = "Puck"
BUILTIN_SPEED_JA = 1.2
BUILTIN_SPEED_EN = 1.0
BUILTIN_ANGEL_STYLE = "warm, bright, polite, and encouraging"
BUILTIN_DEVIL_STYLE = "rough, streetwise, teasing, and mischievously cynical"

SPEAKER_ANGEL = "Angel"
SPEAKER_DEVIL = "Devil"

TURN_START = re.compile(
    r"^(?P<emoji>😇|😈)\s*\*\*(?P<label>天使|悪魔|Angel|Devil)\*\*\s*[:：]\s*(?P<body>.*)$"
)


@dataclass(frozen=True)
class SpeakSettings:
    model: str = BUILTIN_MODEL
    angel_voice: str = BUILTIN_ANGEL_VOICE
    devil_voice: str = BUILTIN_DEVIL_VOICE
    speed_ja: float = BUILTIN_SPEED_JA
    speed_en: float = BUILTIN_SPEED_EN
    angel_style: str = BUILTIN_ANGEL_STYLE
    devil_style: str = BUILTIN_DEVIL_STYLE


def load_settings(path: Path | None = None) -> SpeakSettings:
    """Load settings.yaml. Missing file falls back to built-ins."""
    settings_path = path or DEFAULT_SETTINGS_PATH
    if not settings_path.is_file():
        return SpeakSettings()

    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "PyYAML が未インストールです。例:\n"
            "  scripts/.venv/bin/pip install -r scripts/requirements.txt"
        ) from exc

    raw = yaml.safe_load(settings_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise SystemExit(f"設定ファイルの形式が不正です: {settings_path}")

    speed = raw.get("speed") or {}
    voices = raw.get("voices") or {}
    styles = raw.get("styles") or {}
    if not isinstance(speed, dict) or not isinstance(voices, dict) or not isinstance(styles, dict):
        raise SystemExit(
            f"settings.yaml の speed / voices / styles はマップである必要があります: {settings_path}"
        )

    return SpeakSettings(
        model=str(raw.get("model") or BUILTIN_MODEL),
        angel_voice=str(voices.get("angel") or BUILTIN_ANGEL_VOICE),
        devil_voice=str(voices.get("devil") or BUILTIN_DEVIL_VOICE),
        speed_ja=float(speed.get("ja", BUILTIN_SPEED_JA)),
        speed_en=float(speed.get("en", BUILTIN_SPEED_EN)),
        angel_style=str(styles.get("angel") or BUILTIN_ANGEL_STYLE),
        devil_style=str(styles.get("devil") or BUILTIN_DEVIL_STYLE),
    )


def first_defined(*values: object) -> object | None:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def resolve_runtime(
    args: argparse.Namespace,
    file_settings: SpeakSettings,
) -> SpeakSettings:
    """CLI > env > settings.yaml > built-in."""
    return SpeakSettings(
        model=str(
            first_defined(
                args.model,
                os.environ.get("GEMINI_TTS_MODEL"),
                file_settings.model,
            )
        ),
        angel_voice=str(
            first_defined(
                args.angel_voice,
                os.environ.get("GEMINI_TTS_ANGEL_VOICE"),
                file_settings.angel_voice,
            )
        ),
        devil_voice=str(
            first_defined(
                args.devil_voice,
                os.environ.get("GEMINI_TTS_DEVIL_VOICE"),
                file_settings.devil_voice,
            )
        ),
        speed_ja=file_settings.speed_ja,
        speed_en=file_settings.speed_en,
        angel_style=file_settings.angel_style,
        devil_style=file_settings.devil_style,
    )


def label_to_speaker(label: str, emoji: str) -> str:
    if label in ("天使", "Angel") or emoji == "😇":
        return SPEAKER_ANGEL
    return SPEAKER_DEVIL


def strip_markup(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def parse_turns(transcript: str) -> list[tuple[str, str]]:
    """Parse `😇 **天使**:` / `😈 **悪魔**:` dialogue into (speaker, text) turns."""
    turns: list[tuple[str, str]] = []
    current_speaker: str | None = None
    body_lines: list[str] = []

    def flush() -> None:
        nonlocal current_speaker, body_lines
        if current_speaker is None:
            return
        spoken = strip_markup("\n".join(body_lines))
        if spoken:
            turns.append((current_speaker, spoken))
        current_speaker = None
        body_lines = []

    for raw_line in transcript.splitlines():
        line = raw_line.rstrip()
        match = TURN_START.match(line)
        if match:
            flush()
            current_speaker = label_to_speaker(match.group("label"), match.group("emoji"))
            first = match.group("body").strip()
            body_lines = [first] if first else []
            continue
        if current_speaker is not None:
            body_lines.append(line)

    flush()
    return turns


def is_japanese_turns(turns: list[tuple[str, str]]) -> bool:
    """Return True if any turn contains Japanese (Hiragana, Katakana, or CJK) characters."""
    return any(
        re.search(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]", text)
        for _, text in turns
    )


def default_speed_for_turns(turns: list[tuple[str, str]], settings: SpeakSettings) -> float:
    return settings.speed_ja if is_japanese_turns(turns) else settings.speed_en


def resolve_speed(
    args: argparse.Namespace,
    turns: list[tuple[str, str]],
    settings: SpeakSettings,
) -> float:
    if args.speed is not None:
        return float(args.speed)
    if "GEMINI_TTS_SPEED" in os.environ:
        return float(os.environ["GEMINI_TTS_SPEED"])
    return default_speed_for_turns(turns, settings)


def build_parts(turns: list[tuple[str, str]], settings: SpeakSettings) -> list[dict]:
    parts: list[dict] = []
    for speaker, text in turns:
        style = (
            settings.angel_style if speaker == SPEAKER_ANGEL else settings.devil_style
        )
        parts.append(
            {
                "text": text,
                "speech_metadata": {
                    "speaker": speaker,
                    "style": style,
                },
            }
        )
    return parts


def synthesize(
    turns: list[tuple[str, str]],
    *,
    settings: SpeakSettings,
    api_key: str,
) -> bytes:
    try:
        from google import genai
    except ImportError as exc:
        raise SystemExit(
            "google-genai が未インストールです。例:\n"
            "  python3 -m venv scripts/.venv\n"
            "  scripts/.venv/bin/pip install -r scripts/requirements.txt"
        ) from exc

    # Force Gemini Developer API even if GOOGLE_GENAI_USE_VERTEXAI=true in the env.
    client = genai.Client(api_key=api_key, vertexai=False)
    response = client.models.generate_content(
        model=settings.model,
        contents=[
            {
                "role": "user",
                "parts": build_parts(turns, settings),
            }
        ],
        config={
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "multi_speaker_voice_config": {
                    "speaker_voice_configs": [
                        {
                            "speaker": SPEAKER_ANGEL,
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": settings.angel_voice
                                }
                            },
                        },
                        {
                            "speaker": SPEAKER_DEVIL,
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": settings.devil_voice
                                }
                            },
                        },
                    ]
                }
            },
        },
    )

    try:
        data = response.candidates[0].content.parts[0].inline_data.data
    except (AttributeError, IndexError, TypeError) as exc:
        raise SystemExit(f"Gemini TTS から音声データを取得できませんでした: {response!r}") from exc

    if not data:
        raise SystemExit("Gemini TTS の応答に音声データがありませんでした。")
    return data


def atempo_filter(speed: float) -> str:
    """Build an ffmpeg atempo chain (each factor must be in 0.5..2.0)."""
    if speed <= 0:
        raise ValueError("speed must be positive")
    factors: list[float] = []
    remaining = speed
    while remaining > 2.0:
        factors.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        factors.append(0.5)
        remaining /= 0.5
    factors.append(remaining)
    return ",".join(f"atempo={factor:.6g}" for factor in factors)


def apply_speed(audio: bytes, speed: float) -> bytes:
    """Time-stretch WAV with ffmpeg atempo (pitch-preserving)."""
    if abs(speed - 1.0) < 1e-6:
        return audio
    if speed <= 0:
        raise SystemExit("--speed は正の数である必要があります。")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit(
            "速度変更には ffmpeg が必要です（例: brew install ffmpeg）。"
        )

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "in.wav"
        dst = Path(tmp) / "out.wav"
        src.write_bytes(audio)
        cmd = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(src),
            "-filter:a",
            atempo_filter(speed),
            str(dst),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or b"").decode("utf-8", errors="replace").strip()
            raise SystemExit(f"ffmpeg による速度変更に失敗しました: {detail}") from exc
        return dst.read_bytes()


def play_wav(path: Path) -> None:
    if shutil.which("afplay"):
        subprocess.run(["afplay", str(path)], check=True)
        return
    if shutil.which("ffplay"):
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str(path)],
            check=True,
        )
        return
    if shutil.which("aplay"):
        subprocess.run(["aplay", "-q", str(path)], check=True)
        return
    raise SystemExit(
        f"音声ファイルは保存しましたが再生コマンドが見つかりません: {path}"
    )


def read_input(path: Path | None) -> str:
    if path is None:
        return sys.stdin.read()
    return path.read_text(encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="天使と悪魔の掛け合いを Gemini TTS で読み上げます。"
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="掛け合いテキストのファイル（省略時は標準入力）",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力 WAV パス（省略時は一時ファイル。--play 時は再生後も残す場合に指定）",
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="生成後に再生する（macOS は afplay）",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help=f"設定ファイルパス（default: {DEFAULT_SETTINGS_PATH}）",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="TTS モデル名（未指定時は settings.yaml / 環境変数）",
    )
    parser.add_argument(
        "--angel-voice",
        default=None,
        help="天使の prebuilt voice（未指定時は settings.yaml / 環境変数）",
    )
    parser.add_argument(
        "--devil-voice",
        default=None,
        help="悪魔の prebuilt voice（未指定時は settings.yaml / 環境変数）",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=None,
        help="再生速度（ffmpeg atempo。未指定時は言語別 settings / 環境変数）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="API を呼ばず、パース結果だけ表示する",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    file_settings = load_settings(args.config)
    settings = resolve_runtime(args, file_settings)

    transcript = read_input(args.input)
    turns = parse_turns(transcript)

    if not turns:
        print(
            "天使/悪魔の発話が見つかりませんでした。"
            " `😇 **天使**:` / `😈 **悪魔**:` 形式か確認してください。",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        for speaker, text in turns:
            preview = text if len(text) <= 80 else text[:77] + "..."
            print(f"[{speaker}] {preview}")
        speed = resolve_speed(args, turns, settings)
        print(
            f"(settings) model={settings.model} "
            f"angel={settings.angel_voice} devil={settings.devil_voice} "
            f"speed={speed}",
            file=sys.stderr,
        )
        return 0

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print(
            "GEMINI_API_KEY が未設定のため読み上げをスキップします。",
            file=sys.stderr,
        )
        return 2

    speed = resolve_speed(args, turns, settings)

    print(
        f"Gemini TTS で生成中… model={settings.model} "
        f"angel={settings.angel_voice} devil={settings.devil_voice} "
        f"speed={speed} turns={len(turns)}",
        file=sys.stderr,
    )
    audio = synthesize(turns, settings=settings, api_key=api_key)
    audio = apply_speed(audio, speed)

    if args.output is not None:
        out_path = args.output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(audio)
        print(f"保存しました: {out_path}")
        if args.play:
            play_wav(out_path)
        return 0

    if args.play:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(audio)
        try:
            print(f"一時保存: {tmp_path}")
            play_wav(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)
        return 0

    out_path = Path("angel-and-devil.wav")
    out_path.write_bytes(audio)
    print(f"保存しました: {out_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
