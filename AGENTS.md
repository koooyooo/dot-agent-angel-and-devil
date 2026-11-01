# AGENTS.md

AI コーディングエージェント向けのリポジトリガイドです。人向けの説明は `README.md` / `README_ja.md` を優先し、エージェント向けの作業ルールはここに書きます。

## What this is

`dot-agent-angel-and-devil` は、ノート・文書・Web ページを **天使** と **悪魔** に読ませ、短い掛け合いで感想を返す **Agent Skill** の配布リポジトリです。アプリ本体や Web UI はありません。

- 実行時の振る舞いの正本は `skills/angel-and-devil-note/SKILL.md`
- 口調・役割の正本は `references/Angel.md` / `references/Devil.md`
- TTS は任意で、`scripts/speak.py`（Gemini TTS）が担当

ライセンスは [PolyForm Noncommercial 1.0.0](LICENSE)（ソース公開・非商用）。商用製品の中核としての利用は想定しない。

## Project structure

```text
.
├── AGENTS.md
├── README.md / README_ja.md
├── LICENSE
├── examples/                           # サンプル掛け合い (.md) と音声 (.mp3)
├── install.sh                          # ~/.agents/skills/ へ symlink
└── skills/
    └── angel-and-devil-note/
        ├── SKILL.md                    # スキル手順（エントリ）
        ├── references/
        │   ├── Angel.md
        │   └── Devil.md
        └── scripts/
            ├── speak.py                # 掛け合い TTS
            └── requirements.txt        # google-genai
```

スキルを追加する場合は `skills/<name>/` を作り、`install.sh` が配下をまとめてリンクする前提に合わせる。

## Commands

```bash
./install.sh --dry-run   # 予定だけ表示
./install.sh             # 各スキルを ~/.agents/skills/<name> へ symlink（都度 y/N）

cd skills/angel-and-devil-note
python3 -m venv scripts/.venv
scripts/.venv/bin/pip install -r scripts/requirements.txt

export PYTHON=scripts/.venv/bin/python
$PYTHON scripts/speak.py path/to/dialogue.md --dry-run   # パース確認
$PYTHON scripts/speak.py path/to/dialogue.md -o out.wav  # WAV 保存（要 GEMINI_API_KEY）
$PYTHON scripts/speak.py path/to/dialogue.md --play      # 再生
```

TTS 関連の環境変数: `GEMINI_API_KEY`（必須）, `GEMINI_TTS_MODEL`, `GEMINI_TTS_ANGEL_VOICE`, `GEMINI_TTS_DEVIL_VOICE`, `GEMINI_TTS_SPEED`（既定は日本語 `1.2` / 英語 `1.0`。`1.0` 以外は `ffmpeg` が必要）。

## Working on the skill

- **ペルソナを変えるとき**: `Angel.md` / `Devil.md` を編集する。`SKILL.md` や README に性格の全文を複製しない（要約とリンクで足りる）。
- **手順・出力方式を変えるとき**: `SKILL.md` を更新し、必要なら README 両方を同期する。
- **発話マーカーを変えるとき**: `speak.py` の `TURN_START` 正規表現と `SKILL.md` / README の例を同時に更新する。現行は次の形式のみ:

  ```markdown
  😇 **天使**: …
  😈 **悪魔**: …
  ```

  （英語は `Angel` / `Devil`。絵文字と太字ラベルがパースの前提）
- **掛け合いの長さ**: 平均 2–3 往復、切りの良いところで終える。多くは天使が締める想定。悪魔は各ターンに本当の指摘を 1 つだけ混ぜる。
- **TTS は明示時のみ**: キーが無ければ読み上げをスキップし、テキスト出力のみ。

## Docs sync

ユーザー向けドキュメントは英語・日本語のペアです。

- インストール手順・使い方・環境変数・ペルソナ要約を変えたら `README.md` と `README_ja.md` の両方を更新する
- ロゴやライセンス意図の文言もペアで揃える

## Coding style

- Python: 3 系、型ヒント付き。標準ライブラリ優先。TTS SDK は `google-genai` のみ
- シェル: `bash`、`set -euo pipefail`。破壊的操作の前に確認（`install.sh` の y/N パターンを崩さない）
- コメント・ユーザー向けメッセージは日本語でよい。エージェント向けガイド（本ファイル）も日本語可
- 依存は最小限。`scripts/.venv/` と `*.wav` はコミットしない（`.gitignore` 済み）。配布用サンプル音声は `examples/*.mp3` のみコミットする

## Commits & PRs

- 短い命令形。`fix:` / `feat:` / `chore:` などの prefix 可。日本語も可
- PR には目的・変更点・確認方法（`--dry-run`、必要なら TTS dry-run）を書く
- `GEMINI_API_KEY` や生成音声、venv をコミットしない

## Do not

- ペルソナ定義を `SKILL.md` や README に丸ごと複製しない（正本は `references/`）
- 発話マーカー形式を TTS パーサと食い違わせない
- ライセンスを OSI オープンソースと誤記しない／商用再配布を勧める文言を足さない
- `install.sh` を確認なしの一括上書きに変えない
- `GOOGLE_GENAI_USE_VERTEXAI` に引きずられないよう、TTS クライアントは Developer API（`vertexai=False`）を維持する
