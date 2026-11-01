---
name: angel-and-devil-note
description: Has an angel and a devil read a given document and share their impressions of it.
---

## 手順
- Webページ, File, 標準入力等から コンテンツを取得する
    - 指定がなければユーザーに訊く
- 指定したコンテンツに対して、天使と悪魔の立場で感想を述べる
    - 天使と悪魔の性格（掛け合いを書く前に必ず以下を読み、口調・役割を守る）
        - 天使: [references/Angel.md](references/Angel.md)
        - 悪魔: [references/Devil.md](references/Devil.md)
        - 天使は良い点を探して褒めあげる
        - 悪魔は悪い点を探してそそのかし、その誘惑に本当の指摘を1つ混ぜる
    - 会話の流れ
        - 天使と悪魔の掛け合いを切りの良いところまで、平均2-3往復
- 感想は基本的に標準出力に出すが、ユーザーの指定によっては以下の方式も存在する。
    - 指定の別ファイルに出力
    - 元ファイルの末尾に引用形式で出力
    - 音声で読み上げ（ユーザーが明示した場合のみ）
        - **必須: 生成前にユーザーへ許可を取る。** Gemini TTS は従量課金されうる。初回依頼でも「API を呼んで音声を生成してよいか」を確認し、拒否・曖昧なら読み上げをスキップしてテキストのみにする。勝手に `speak.py` を実行しない
        - 前提: 環境変数 `GEMINI_API_KEY` があること。無ければ読み上げはスキップし、テキスト出力のみ行う
        - 初回のみ依存インストール（venv 推奨）:
            - `python3 -m venv scripts/.venv`
            - `scripts/.venv/bin/pip install -r scripts/requirements.txt`
        - 掛け合いテキストをファイルに保存したうえで、次を実行する（`PYTHON=scripts/.venv/bin/python`）
            - ユーザー許可後のみ `-y` を付けてよい（対話確認を省略）:
                - 保存のみ: `$PYTHON scripts/speak.py path/to/dialogue.md -o out.wav -y`
                - 再生: `$PYTHON scripts/speak.py path/to/dialogue.md --play -y`
            - パース確認（API なし・許可不要）: `$PYTHON scripts/speak.py path/to/dialogue.md --dry-run`
        - 既定値は [settings.yaml](settings.yaml)（model / voices / styles / 言語別 speed）。API キーは書かない
        - 上書き優先順: CLI（`--speed` 等） > 環境変数（`GEMINI_TTS_*`） > `settings.yaml` > 組み込み既定
        - `1.0` 以外の速度変更は `ffmpeg` が必要
        - 発話マーカーは `😇 **天使**:` / `😈 **悪魔**:`（英語は `Angel` / `Devil`）を使うこと
