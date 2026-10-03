# vrc-gw230529-einstein-toolkit-LT

## プロジェクト概要

**VRChat 物理学集会 LT 用スライド資料**。
[gw230529-einstein-toolkit](https://github.com/s-sasaki-earthsea-wizard/gw230529-einstein-toolkit)
(Einstein Toolkit によるブラックホール・中性子星合体 GW230529 の数値相対論
シミュレーション) と、そのクラウド実行基盤
[gw230529-einstein-toolkit-aws-tf](https://github.com/s-sasaki-earthsea-wizard/gw230529-einstein-toolkit-aws-tf)
の成果を `reveal.js` のスライドにまとめる。5 月の LT
[vrc-gw150914-einstein-toolkit-LT](https://github.com/s-sasaki-earthsea-wizard/vrc-gw150914-einstein-toolkit-LT)
の続編。

## 発表の主題 (この LT のスコープ)

- **対象集会**: VRChat 物理学集会。物理が好きな聴衆で、クラウドや HPC の知識は
  前提にしない
- **主役は物理**。GW230529 と質量ギャップ、潮汐破壊、残骸ブラックホールの質量と
  自転、重力波の波形を前半から中盤に置く
- **クラウド運用は「どうやって計算を完走させたか」の物語**として後半に置く。
  サービス名や型番は出さず、仕組みを平易な言葉で説明する
  (スポットインスタンスは AWS を紹介してから出す)
- **学術的な新規性は主張しない**。公開されている計算例の追試 (自由研究)

詳細は [docs/project_overview.md](docs/project_overview.md) と
[docs/talk_outline.md](docs/talk_outline.md)。

## 現在地 (2026-10-03)

- スライドは `slides-jp/index.html` (本編 43 枚 + Appendix 6 枚)。第一稿に
  レビューを反映し、「利点と弱点」「応用性」の 2 枚を足した
- 合体時刻を sim 側の訂正 (2026-10-03) に合わせて 674 M☉ = 3.32 ms にした。
  自宅 PC の試走の比較も同じ訂正を受けて書き直した
- 発表日・持ち時間は未定。持ち時間が決まったら `docs/talk_outline.md` の
  削り順に従って絞る
- 「完走した感想」のスライドは発表者本人が書いた
- タイトルは「円盤になったのか、丸呑みされたのか」に変え、タイトル画像を
  `title.png` に差し替えた

## 関連リンク

- シミュレーション本体: <https://github.com/s-sasaki-earthsea-wizard/gw230529-einstein-toolkit>
- クラウド実行基盤: <https://github.com/s-sasaki-earthsea-wizard/gw230529-einstein-toolkit-aws-tf>
- 前回の LT: <https://github.com/s-sasaki-earthsea-wizard/vrc-gw150914-einstein-toolkit-LT>
- スライドテンプレート: <https://github.com/s-sasaki-earthsea-wizard/lt-slide-template>
- 観測論文: [Astrophys. J. Lett. 970, L34 (2024)](https://arxiv.org/abs/2404.04248)
- 追試した計算の論文: [arXiv:2603.07374](https://arxiv.org/abs/2603.07374)
- Einstein Toolkit 公式ギャラリー: <https://einsteintoolkit.org/gallery/bhns/index.html>

## 言語設定

ユーザへの応答は**日本語**。スライド本文と `docs/` も日本語。
コード内のコメント・ログ・エラーメッセージ・docstring は**英語**で書く。

## 開発ルール

### スライド作成

- ベース: [reveal.js](https://github.com/hakimel/reveal.js) 5.1.0
- メインファイル: `slides-jp/index.html` (Markdown を `<textarea>` に書く)
- カスタムスタイル: `slides-jp/styles/custom-style.css`
- 数式は KaTeX (`$...$` / `$$...$$`)。数式プラグインは維持すること
- **1 枚の高さは 700px**。本文はおよそ 9 行が上限で、超えると下にはみ出す。
  書いたら必ずレンダリングして確かめる
- Markdown の落とし穴
  - 数式の中で `\,` `\{` `\%` のような「バックスラッシュ + 記号」は使わない
    (Markdown のエスケープとして食われる)
  - `**...$M_{\odot}$**` の直後に全角の句読点が来ると太字にならない。
    `<strong>` で書く
  - `<small>` の中では KaTeX の添字がずれる。`M☉` のように文字で書く
- 単位は聴衆が読めるものにする: 時間はミリ秒、長さは km、質量は太陽質量 M☉。
  幾何単位 ($G = c = M_\odot = 1$) の値はスライドに出さない

### 図

- 計算結果の図は、クラウド実行基盤のリポジトリの `postprocessing/` の出力を
  `slides-jp/assets/images/` にコピーして使う (SI 単位版)
- この LT だけで使う図 (`bh_mass_spin.png`, `matter_outside.png`) は
  `scripts/plot_physics.py` が `docs/data/*.tsv` から描く。配色とフォントは
  `postprocessing/common.py` に合わせてある
- 概念図は SVG で手書きし、同じ配色 (Okabe-Ito) を使う

### 数字の扱い

- スライドに出す数字は [docs/source_material.md](docs/source_material.md) に
  出典か導出を書く。出典の無い数字を足さない
- 格子全体の静止質量には**数値大気 (約 0.25 M☉) が含まれる**。
  「合体後に残った物質」を語るときは必ず差し引く (同ファイルに導出)
- 合体時刻は **674 M☉ = 3.32 ms** (Ψ4 のピークから tortoise 座標の遅延を
  引いた値)。t − r で引いた旧値 713 M☉ は使わない。infra 側の文書と図には
  まだ旧値が残っている
- 参照計算の計算資源は、論文の記述と公開データのログで値が違う。
  スライドでは論文の値を「論文の計算は」と論文の値として出す。
  食い違いの理由を推測で書かない

### コーディング規約

- Python: PEP 8 準拠、Google Style の docstring
- HTML / JS のインデントはスペース 2 文字

### Git 運用

- ブランチ戦略: `feature/*`, `fix/*`, `refactor/*`
- コミットメッセージ: 英文を使用、動詞から始める
- PR は main ブランチへ

### コミットメッセージ規約

#### コミット粒度

- **1 コミット = 1 つの主要な変更**
- 関連する変更は 1 つのコミットにまとめる
- 大きな変更は段階的に分割

#### プレフィックスと絵文字

- ✨ feat: 新機能
- 🐞 fix: バグ修正
- 📚 docs: ドキュメント
- 🎨 style: コードスタイル修正
- 🛠️ refactor: リファクタリング
- ⚡ perf: パフォーマンス改善
- ✅ test: テスト追加・修正
- 🏗️ chore: ビルド・補助ツール
- 🚀 deploy: デプロイ
- 🔒 security: セキュリティ修正
- 📝 update: 更新・改善
- 🗑️ remove: 削除

**重要**: Claude Code を使用してコミットする場合は、必ず以下の署名を含める:

```text
🤖 Assisted by [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## ディレクトリ構成

```text
.
├── CLAUDE.md                    # 本ファイル
├── README.md                    # プロジェクト README
├── Makefile                     # serve / pdf / figures
├── organizer.yaml               # GitHub branch protection 設定
├── docs/
│   ├── project_overview.md      # 何を・誰に話すか
│   ├── talk_outline.md          # 構成と削り順
│   ├── source_material.md       # スライドの数字の出典と導出
│   └── data/*.tsv               # 本番 run から抜き出した時系列
├── scripts/
│   ├── extract_run_data.py      # run の出力 → docs/data/*.tsv
│   └── plot_physics.py          # docs/data/*.tsv → 図 2 枚
└── slides-jp/
    ├── index.html               # スライド本体
    ├── assets/images/           # 図 (PNG / SVG)
    ├── assets/videos/           # 密度の動画
    ├── yt_script.md             # YouTube 脚本 (TBA)
    └── youtube_description.md   # YouTube 動画概要文 (TBA)
```

## ドキュメント更新プロセス

スライドの構成や数字を変えたら、以下を同期更新する:

1. **docs/talk_outline.md**: 構成と削り順
2. **docs/source_material.md**: 数字の出典と導出
3. **README.md**: 概要の表
4. **CLAUDE.md**: 「現在地」
5. **Makefile**: ターゲットを足したらヘルプテキスト (`##` コメント)
