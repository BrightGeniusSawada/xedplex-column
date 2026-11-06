"""Build visible topic/related links. Preview by default; --write applies changes."""
import argparse
import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://column.bright-genius.jp/"


def block(name, content):
    return "<!-- seo-{}:start -->\n{}\n<!-- seo-{}:end -->".format(name, content, name)


def replace_block(source, name, content, marker):
    pattern = r"<!-- seo-" + name + r":start -->.*?<!-- seo-" + name + r":end -->"
    replacement = block(name, content)
    if re.search(pattern, source, re.S):
        return re.sub(pattern, lambda _: replacement, source, flags=re.S)
    if source.count(marker) != 1:
        raise ValueError("Expected exactly one insertion marker: " + marker)
    return source.replace(marker, replacement + "\n\n" + marker, 1)


def links(entries):
    return "\n".join('  <li><a href="{}">{}</a></li>'.format(
        html.escape(filename, quote=True), html.escape(label)) for filename, label in entries)


def build(date):
    topics = json.loads((ROOT / "tools/seo-topics.json").read_text(encoding="utf-8"))
    memberships = {}
    topic_sections = []
    for topic in topics:
        entries = topic["articles"]
        if not re.fullmatch(r"[a-z-]+", topic["id"]):
            raise ValueError("Invalid topic id")
        for filename, label in entries:
            if not re.fullmatch(r"[a-z0-9-]+\.html", filename) or not (ROOT / filename).is_file():
                raise ValueError("Missing or invalid article: " + filename)
            memberships.setdefault(filename, []).extend(entries)
        topic_sections.append('<details id="topic-{}"><summary>{}</summary><ul>\n{}\n</ul></details>'.format(
            topic["id"], html.escape(topic["title"]), links(entries)))
    topic_body = ('<nav class="seo-topics" aria-labelledby="seo-topics-title">\n'
                  '<h2 id="seo-topics-title">テーマ別に記事を探す</h2>\n'
                  '<p>塾運営で見直したい業務から、基本と具体的な進め方を探せます。</p>\n'
                  + "\n".join(topic_sections) + '\n</nav>')
    updates = {}
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    updated = replace_block(source, "topics", topic_body,
                            "<!-- ▼ 新しい記事はこのリストの一番上に追加してください -->")
    topic_style = '''<style>
.seo-topics { padding: 18px 20px; margin: 24px 0; border: 1px solid #dde3ea; border-radius: 10px; }
.seo-topics h2 { font-size: 18px; margin: 0 0 8px; }
.seo-topics p { font-size: 14px; color: #4a5563; margin: 0 0 12px; }
.seo-topics details { border-top: 1px solid #e5e9ef; padding: 8px 0; }
.seo-topics summary { cursor: pointer; font-weight: 600; color: #1a5fb4; }
.seo-topics ul { padding-left: 22px; margin: 10px 0; }
.seo-topics li { margin: 6px 0; overflow-wrap: anywhere; }
</style>'''
    updated = replace_block(updated, "topic-style", topic_style, "</head>")
    if updated != source:
        updates["index.html"] = updated
    for filename, entries in memberships.items():
        seen = {filename}
        related = []
        for entry in entries:
            if entry[0] not in seen:
                seen.add(entry[0])
                related.append(entry)
        body = ('<nav aria-label="関連する塾運営の記事">\n<h2>あわせて読みたい記事</h2>\n'
                '<ul>\n' + links(related[:5]) + '\n</ul>\n</nav>')
        source = (ROOT / filename).read_text(encoding="utf-8")
        updated = replace_block(source, "related", body, '<div class="cta">')
        if updated != source:
            updated = re.sub(r'("dateModified"\s*:\s*")[^"]+("\s*[,}])',
                             lambda m: m[1] + date + m[2], updated)
            updates[filename] = updated
    if updates:
        source = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        updated = source
        for filename in updates:
            url = DOMAIN + ("" if filename == "index.html" else filename)
            pattern = r"(<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)[^<]+(</lastmod>)"
            updated, count = re.subn(pattern, lambda m: m[1] + date + m[2], updated)
            if count != 1:
                raise ValueError("Expected one sitemap entry: " + url)
        updates["sitemap.xml"] = updated
    return updates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    datetime.date.fromisoformat(args.date)
    updates = build(args.date)
    for filename, source in updates.items():
        print(("WRITE " if args.write else "PLAN  ") + filename)
        if args.write:
            with (ROOT / filename).open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(source)
    print("{} files; {}".format(len(updates), "applied" if args.write else "preview only"))


if __name__ == "__main__":
    main()
