#!/usr/bin/env python3
# tools/eyecatch.json の全エントリから images/<slug>.png を生成する
# （GitHub Actions .github/workflows/eyecatch.yml から実行される。ローカルでも実行可）
# 使い方: python3 tools/build_eyecatch.py [--only slug]
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eyecatch import make  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "tools", "eyecatch.json")
OUT_DIR = os.path.join(ROOT, "images")

only = None
if len(sys.argv) >= 3 and sys.argv[1] == "--only":
    only = sys.argv[2]

with open(MANIFEST, encoding="utf-8") as fp:
    entries = json.load(fp)

os.makedirs(OUT_DIR, exist_ok=True)
for e in entries:
    if only and e["slug"] != only:
        continue
    make(e["title"], e["subtitle"], os.path.join(OUT_DIR, e["slug"] + ".png"))
