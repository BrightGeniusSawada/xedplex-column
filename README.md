# XedPlex 塾運営お役立ちコラム

塾管理システム XedPlex（ゼドプレックス）の集客用コラムサイト。
GitHub Pages で https://column.bright-genius.jp/ として公開。

- 記事は2日に1本、Claudeの定期タスクが自動生成・自動コミットします
- 新記事追加時は index.html のカード一覧と sitemap.xml も更新されます
- アイキャッチ画像: 記事ごとの文言を tools/eyecatch.json に登録すると、GitHub Actions（.github/workflows/eyecatch.yml）が tools/eyecatch.py で images/<slug>.png（1280x670）を自動生成してコミットします。各記事はこの画像を本文冒頭と OGP（og:image）に使用します
  - ローカルで確認する場合: `python3 tools/build_eyecatch.py --only <slug>`（要 Pillow / Noto Sans CJK）

## SEOの保守

- テーマ別の案内と関連記事は `tools/seo-topics.json` を正本とします。新しい記事が既存テーマに合う場合は、ファイル名と読者に伝わる短いリンク名を追加してください。
- `python3 tools/update_seo_links.py --date YYYY-MM-DD` で変更予定を確認し、`--write` を付けて反映します。変更された記事の `dateModified` とサイトマップの `lastmod` も実際の更新日にそろいます。再実行して変更0件になることを確認してください。
- `index.html` の `seo-topics` / `seo-topic-style` と記事の `seo-related` マーカー内は生成箇所です。新記事追加用の既存コメントとカード一覧は維持してください。
- 記事本文や公開日は、リンク整備のために書き換えません。未登録の原因はSearch ConsoleのURL検査で確認し、登録済みと登録リクエスト済みを分けて記録してください。
- 詳細な点検・公開・効果測定は `transtudent` リポジトリの `docs/手順書/Search_Console_SEO改善_作業手順.md` を参照してください。
