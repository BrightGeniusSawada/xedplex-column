#!/usr/bin/env python3
# XedPlex コラム アイキャッチ画像ジェネレータ
# 使い方: python3 eyecatch.py "タイトル" "サブタイトル" 出力ファイル.png
#   - タイトル中の「|」は強制改行（例: "塾のシステム、どう選ぶ？|小規模塾の5つの基準"）
#   - 行頭に「、。？」などが来ないよう簡易禁則処理を行う
# サイズ: 1280x670（OGP / note の推奨比率）
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 670
FONT_DIR = "/usr/share/fonts/opentype/noto"
FONT = os.path.join(FONT_DIR, "NotoSansCJK-Bold.ttc")
FONT_BLACK = os.path.join(FONT_DIR, "NotoSansCJK-Black.ttc")
if not os.path.exists(FONT_BLACK):
    FONT_BLACK = FONT  # Black が無い環境では Bold で代用

# 行頭禁則（この文字で行を始めない）／行末禁則（この文字で行を終えない）
NO_HEAD = set("、。，．・：；？！?!」』）〕］｝〉》〟ー～…‥っゃゅょぁぃぅぇぉッャュョァィゥェォ")
NO_TAIL = set("「『（〔［｛〈《〝")


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def wrap(d, text, font, max_w):
    """1文字ずつ詰めて折り返す。「|」は強制改行。簡易禁則つき。"""
    lines = []
    for para in text.replace("\n", "|").split("|"):
        line = ""
        for ch in para:
            if d.textlength(line + ch, font=font) <= max_w:
                line += ch
                continue
            # 折り返し
            if ch in NO_HEAD and line:
                # 追い出し: 直前の1文字を次行へ送る
                lines.append(line[:-1])
                line = line[-1] + ch
            elif line and line[-1] in NO_TAIL:
                lines.append(line[:-1])
                line = line[-1] + ch
            else:
                lines.append(line)
                line = ch
        lines.append(line)
    return [l for l in lines if l != ""] or [""]


def make(title, subtitle, out):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # 斜めグラデーション（濃紺→ブランドブルー）
    c1, c2 = (16, 45, 84), (26, 95, 180)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=lerp(c1, c2, t * 0.9))
    # 装飾: 右上の大きな円・左下の細い円
    d.ellipse([W - 320, -180, W + 140, 280], outline=(255, 255, 255), width=3)
    d.ellipse([W - 260, -120, W + 80, 220], outline=(120, 170, 230), width=2)
    d.ellipse([-120, H - 160, 160, H + 120], outline=(120, 170, 230), width=2)
    # 上部タグ
    tag_font = ImageFont.truetype(FONT, 30, index=2)
    tag = "塾運営お役立ちコラム"
    tw = d.textlength(tag, font=tag_font)
    d.rounded_rectangle([80, 70, 80 + tw + 48, 128], radius=29, fill=(255, 255, 255))
    d.text((80 + 24, 82), tag, font=tag_font, fill=(26, 95, 180))
    # タイトル（自動折り返し・最大3行。収まらなければ縮小）
    size = 76
    while size >= 48:
        f = ImageFont.truetype(FONT_BLACK, size, index=2)
        lines = wrap(d, title, f, W - 180)
        if len(lines) <= 3:
            break
        size -= 6
    y = 200
    for line in lines:
        d.text((84, y), line, font=f, fill=(255, 255, 255))
        y += int(size * 1.35)
    # アクセントバー＋サブタイトル
    d.rectangle([84, y + 18, 84 + 72, y + 26], fill=(255, 200, 60))
    sub_font = ImageFont.truetype(FONT, 38, index=2)
    d.text((84, y + 46), subtitle, font=sub_font, fill=(205, 224, 246))
    # 下部ブランド
    brand_font = ImageFont.truetype(FONT_BLACK, 40, index=2)
    b = "XedPlex"
    bw = d.textlength(b, font=brand_font)
    d.text((W - 100 - bw, H - 92), b, font=brand_font, fill=(255, 255, 255))
    small = ImageFont.truetype(FONT, 24, index=2)
    s = "教育機関向け総合DXプラットフォーム"
    sw = d.textlength(s, font=small)
    d.text((W - 100 - sw, H - 44), s, font=small, fill=(160, 195, 235))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    img.save(out, optimize=True)
    print("saved:", out)


if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2], sys.argv[3])
