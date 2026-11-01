# DOT-AGENT-ANGEL-AND-DEVIL

<p align="center">
  <img src="logo.jpg" alt="DOT-AGENT-ANGEL-AND-DEVIL" width="720" />
</p>

<p align="center">
  <strong>二面視点のコントラリアン・フィードバック・システム</strong><br />
  <a href="README.md">English</a>
</p>

ノート・文書・Web ページを **天使** 😇 と **悪魔** 😈 に読ませ、短い掛け合いで感想を返す Agent Skill です。

- 天使は具体的な良い点を拾い、つまずきも前向きに捉え直して励ます
- 悪魔は抜け・言い訳・誘惑をからかいつつ、各ターンに **本当の指摘を1つ** 混ぜる

---

## 同梱内容

| パス | 説明 |
|------|------|
| `skills/angel-and-devil-note/` | Agent Skill（`SKILL.md`・ペルソナ・任意 TTS） |
| `skills/.../references/Angel.md` | 天使の性格定義 |
| `skills/.../references/Devil.md` | 悪魔の性格定義 |
| `skills/.../scripts/speak.py` | 掛け合いを Gemini TTS で読み上げる任意スクリプト |
| `examples/` | サンプル掛け合いと TTS 音声（`sample-en.mp3` / `sample-ja.mp3`） |
| `install.sh` | スキルを `~/.agents/skills/` へシンボリックリンク |

---

## インストール

Agent Skills を `~/.agents/skills/` から読み込む環境（Cursor / Codex 互換エージェントなど）向けです。

```bash
./install.sh
```

リンク作成前に `[y/N]` で確認されます。変更せず予定だけ見る場合:

```bash
./install.sh --dry-run
```

作成されるリンク:

```text
~/.agents/skills/angel-and-devil-note  →  <repo>/skills/angel-and-devil-note
```

---

## 使い方

### スラッシュコマンド

Agent チャットで `/` を押し、スキルを選ぶ（またはそのまま入力する）:

```text
/angel-and-devil-note @notes/today.md
```

ほかの例:

```text
/angel-and-devil-note @notes/today.md
/angel-and-devil-note @README.md 末尾に掛け合いを追記して
/angel-and-devil-note @notes/today.md 音声で読み上げて
/angel-and-devil-note https://example.com/article
```

ファイルやフォルダを指すときは `@path` を使うと、エージェントがコンテキストとして添付しやすいです（例: `@notes/today.md`, `@docs/`）。素のパスでも動きますが、Cursor / Codex 系のチャットでは `@` 付きの方が明確です。

### 自然言語

スラッシュなしでも依頼できます。

- 「@notes/today.md を天使と悪魔に読ませて」
- 「このノートを天使・悪魔でレビューして」
- 「この URL を天使と悪魔に感想させて」

ソース未指定の場合は、Web・ファイル・標準入力などから取るようスキル側が尋ねます。

### サンプル

**入力**（`@notes/today.md`）:

```markdown
# Tasks
- [ ]
- [ ]
- [ ]
# Notes
賞味期限を4日経過した卵をスクランブルエッグにして食べてみる。身体には良くないかも知れないが、言うほど悪くはないだろう。口の中が卵っぽくなったので、カステラで押し込んでみる。良い点としては朝から良い感じで目が覚めた。そしてこの天使と悪魔のスキルの開発はそこそこ進んだ。
```

**出力:**

```markdown
😇 **天使**: おはようございます！朝からすっきり目覚めて、温かいスクランブルエッグを自分で作って食べられたなんて、素敵な一日の始まりですね！賞味期限が4日過ぎた卵でも、生で食べずにきちんと火を通した判断はさすがです！カステラで後味を整えたのも朝の糖分補給になってよし、しかも日も浅いのに天使と悪魔スキルの開発までしっかり進めているなんて、もう立派な朝の成果ですよ！

😈 **悪魔**: ケッ、賞味期限切れ4日の卵をスクランブルにして、追いカステラだと？朝からカオスなコンボじゃねえか！しかも「卵っぽいからカステラで押し込んだ」だって？卵の味を卵と砂糖のかたまりで打ち消す気かよ、まだ半分寝てやがるな！ヒッヒッヒ、Tasks のチェックボックスも3つとも空っぽじゃねえか。書かなきゃ失敗もしねえ——最高のライフハックだぜ！このままタスクは白紙のまま、カステラの残りを平らげて二度寝ちまえよ！

😇 **天使**: 悪魔さん、大げさですよ！カステラの甘さのおかげか、ノートにも「朝から良い感じで目が覚めた」とちゃんと書いてあります。それだけで立派な勝ちです！空欄のタスクは、巨大な ToDo を悩むより先にスキル開発へ飛び込んだ証拠でもありますよね。お水を一杯飲んだら、今日のご褒美タスクをひとつだけ小さく決めてみませんか？

😈 **悪魔**: ヒッヒッヒ、「スキル開発はそこそこ進んだ」ねえ。本丸の重い仕事から逃げて、キラキラした横道ツール弄りに逃げてるだけじゃねえのか？朝のギャンブルのいいところはこれだ——昼ごろに「ヴィンテージ卵」が腹で蜂起したら、予定ぜんぶドタキャンできる鉄壁の医療言い訳が手に入るぜ！戦術的食中毒ホリデーで、罪悪感ゼロのサボりを決めこめ！

😇 **天使**: お腹は大丈夫です、悪魔の言うことなんか聞かないで！早起きして日記を書いて、このスキルのマルチスピーカー音声まで繋いだ朝は、それだけで大きな勝利です！お水か温かいお茶でお腹を優しく労って、今日の小さなゴールを一行だけ書いて、素敵な一日を楽しんでくださいね。応援しています！
```

**音声:** [日本語](examples/sample-ja.mp3) · [英語](examples/sample-en.mp3)

（台本: [`sample-ja.md`](examples/sample-ja.md) · [`sample-en.md`](examples/sample-en.md)。後述の任意 Gemini TTS で生成）

### 出力方式

既定は **標準出力** です。指定により次も可能です。

| 方式 | 挙動 |
|------|------|
| 別ファイル | 指定パスへ書き出し |
| 元ファイル末尾 | 元文書の末尾に引用形式で追記 |
| 音声読み上げ | 明示指定時のみ（後述） |

長さの目安は **平均 2〜3 往復**。切りの良いところで終え、多くは天使が締める想定です。

### 発話マーカー

```markdown
😇 **天使**: …
😈 **悪魔**: …
```

（英語応答時は `Angel` / `Devil` も可）

---

## 任意: 音声読み上げ（TTS）

`GEMINI_API_KEY` が必要です。無い場合は読み上げをスキップし、テキスト出力のみ行います。

**費用・同意:** TTS は Gemini API を呼び、`GEMINI_API_KEY` に紐づく Google アカウント／プロジェクトへ従量課金されることがあります。読み上げは明示指定時のみで、エージェントは音声生成の前に必ず確認を取ります。`speak.py` も実行時に確認プロンプトを出します（既に許可済みのときだけ `-y` / `--yes` を使ってください）。

```bash
cd skills/angel-and-devil-note
python3 -m venv scripts/.venv
scripts/.venv/bin/pip install -r scripts/requirements.txt

export PYTHON=scripts/.venv/bin/python
# WAV 保存（-y を外すと対話で確認プロンプトが出る）
$PYTHON scripts/speak.py path/to/dialogue.md -o out.wav -y
# 再生
$PYTHON scripts/speak.py path/to/dialogue.md --play -y
# パース確認のみ（API なし）
$PYTHON scripts/speak.py path/to/dialogue.md --dry-run
```

既定値は [`settings.yaml`](skills/angel-and-devil-note/settings.yaml)（model / voices / styles / 言語別 speed）。API キーは書かないでください。

prebuilt 声の一覧: [`Voices.md`](skills/angel-and-devil-note/references/Voices.md)

上書きの優先順: CLI フラグ > 環境変数 `GEMINI_TTS_*` > `settings.yaml` > 組み込み既定。

---

## ペルソナ（要約）

| | 天使 😇 | 悪魔 😈 |
|---|----------|----------|
| 役割 | 具体的な努力を褒め、つまずきを再解釈 | 未完了・言い訳・怠惰を指摘し誘惑する |
| 口調 | 明るく丁寧（です・ます）、励まし | 荒くからかう（〜じゃねえか、ヒッヒッヒ など） |
| ルール | 悪魔の皮肉を押し返し、肯定して締める | 誘惑の中に **真実の指摘を1つ** 混ぜる |

詳細: [`Angel.md`](skills/angel-and-devil-note/references/Angel.md) · [`Devil.md`](skills/angel-and-devil-note/references/Devil.md)

---

## ライセンス

[PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0) — 詳細は [`LICENSE`](LICENSE)。

OSI のオープンソースではなく、**ソース公開・非商用（source-available / non-commercial）** です。

**運用上の意図（`LICENSE` 末尾の非拘束的ノートも参照）:**

- **許可:** 業務上でも、自分の作業の付随として個人的に使う場合（例: 雇用先で自分のメモをレビューする）
- **不可:** 本プロジェクト（または実質的に同様の派生物）が、主要な製品・有料機能・商用サービスになる場合、あるいは収益の中核になる場合
- **判断に迷う場合:** 著作権者へ書面の許諾、または別途の商用ライセンスを依頼してください。
