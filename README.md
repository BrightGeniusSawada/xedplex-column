# XedPlex 塾運営お役立ちコラム

塾管理システム XedPlex（ゼドプレックス）の集客用コラムサイト。
GitHub Pages で https://column.bright-genius.jp/ として公開。

- 記事は2日に1本、Claudeの定期タスクが自動生成・自動コミットします
- 新記事追加時は index.html のカード一覧と sitemap.xml も更新されます
- アイキャッチ画像: 記事ごとの文言を tools/eyecatch.json に登録すると、GitHub Actions（.github/workflows/eyecatch.yml）が tools/eyecatch.py で images/<slug>.png（1280x670）を自動生成してコミットします。各記事はこの画像を本文冒頭と OGP（og:image）に使用します
  - ローカルで確認する場合: `python3 tools/build_eyecatch.py --only <slug>`（要 Pillow / Noto Sans CJK）
