# vrc-gw230529-einstein-toolkit-LT

VRChat 物理学集会 LT 用スライド資料 — **Einstein Toolkit による GW230529
(ブラックホール・中性子星合体) の数値相対論シミュレーションを、クラウドの
スポットインスタンスで回した話** の発表用プロジェクト。

スライド本体は [reveal.js](https://github.com/hakimel/reveal.js) で構成し、
[lt-slide-template](https://github.com/s-sasaki-earthsea-wizard/lt-slide-template) を
ベースにしている。5 月の LT
[vrc-gw150914-einstein-toolkit-LT](https://github.com/s-sasaki-earthsea-wizard/vrc-gw150914-einstein-toolkit-LT)
(連星ブラックホール合体を自宅 PC で) の続編にあたる。

## 概要

2023 年 5 月 29 日に検出された重力波 **GW230529** は、質量ギャップにある軽い
ブラックホール (約 3.6 M☉) と中性子星 (約 1.4 M☉) の合体と解釈されている。
Einstein Toolkit の公式ギャラリーにはこの合体を想定した例題が公開されており、
本プロジェクトはそれを**公式と同じ解像度で追試**した。

- シミュレーション本体: <https://github.com/s-sasaki-earthsea-wizard/gw230529-einstein-toolkit>
- クラウド実行基盤: <https://github.com/s-sasaki-earthsea-wizard/gw230529-einstein-toolkit-aws-tf>
- 公式ギャラリー (参照): <https://einsteintoolkit.org/gallery/bhns/index.html>
- 追試した計算の論文: [arXiv:2603.07374](https://arxiv.org/abs/2603.07374)
- 公開データ: <https://doi.org/10.5281/zenodo.18940220>

前回との違いは 2 つ。**物質 (中性子星) が入る**ことと、自宅 PC には載らないので
**クラウドで回す**こと。安く借りられるスポットインスタンスは 2 分前の予告で
止められるので、途中経過を外部ストレージへ送り続け、止められるたびに自動で
再開する構成を組んだ。

| 量 | 値 |
| --- | --- |
| 計算した物理時間 | 8.62 ms (合体後 5.1 ms まで) |
| かかった時間 | 45 時間 33 分 (計算機 14 台、中断 13 回) |
| 残骸ブラックホール | 質量 4.72 M☉、無次元スピン 0.60 |
| 合体後 5 ms で格子上に残る物質 | 星の約 6% (約 0.09 M☉) |
| 公開データとの波形の差 | 最大 4.4×10⁻⁴ (ピーク振幅比) |

数字の出どころは [docs/source_material.md](docs/source_material.md) にまとめてある。

## ディレクトリ構成

```text
.
├── docs/                     # 発表の設計と素材
│   ├── project_overview.md   # 何を・誰に話すか
│   ├── talk_outline.md       # 構成と、時間が足りないときの削り順
│   ├── source_material.md    # スライドの数字とその出典・導出
│   └── data/                 # 本番 run から抜き出した時系列 (TSV)
├── scripts/                  # スライドの図を再現するスクリプト
│   ├── extract_run_data.py   # run の出力 → docs/data/*.tsv
│   └── plot_physics.py       # docs/data/*.tsv → 図 2 枚
└── slides-jp/                # reveal.js スライド
    ├── index.html            # スライド本体
    ├── assets/images/        # 図 (PNG は計算結果、SVG は概念図)
    └── assets/videos/        # 密度の動画
```

## 開発環境

- Node.js 18 以上 (reveal.js 5.x の要求。`npm start` を使う場合)
- Python 3 + numpy + matplotlib (図を描き直す場合)
- 必要に応じて [decktape](https://github.com/astefanutti/decktape) (PDF エクスポート用)

## 使い方

```bash
make help       # ターゲット一覧
make serve      # http://localhost:8000 でスライドをプレビュー
make pdf        # slides-jp/slides-jp.pdf にエクスポート
make figures    # docs/data から図を描き直す
```

`make serve` は静的ファイルを配信するだけなので `npm install` は要らない。
reveal.js の開発サーバを使うなら従来どおり `cd slides-jp && npm install && npm start`。

### 図の再生成

`slides-jp/assets/images/` の図は 3 種類ある。

- **`bh_mass_spin.png` / `matter_outside.png`**: このリポジトリの
  `scripts/plot_physics.py` が `docs/data/*.tsv` から描く
- **それ以外の PNG と動画**: クラウド実行基盤のリポジトリの `postprocessing/`
  (`make figures` / `make movie` / `make ledger-chart`) の出力をそのまま置いている
- **SVG**: 手書きの概念図

`docs/data/*.tsv` は本番 run の出力 (約 10 GB) から `scripts/extract_run_data.py`
で抜き出したもの。元の出力が無くても図は再現できる。

## 関連ドキュメント

- [docs/project_overview.md](docs/project_overview.md) — 発表の目的・聴衆・スコープ
- [docs/talk_outline.md](docs/talk_outline.md) — 構成と削り順
- [docs/source_material.md](docs/source_material.md) — 数字の出典と導出

## 免責事項

本スライドの内容に従ったいかなる結果においても著者は一切の責任を負いません。
