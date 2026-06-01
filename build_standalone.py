#!/usr/bin/env python3
"""Inline CSS + base64-embed all images into one portable HTML file."""
import base64, re, pathlib

ROOT = pathlib.Path(__file__).parent
html = (ROOT / "index.html").read_text()
css = (ROOT / "styles.css").read_text()

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml"}

def data_uri(rel_path: str) -> str:
    p = ROOT / rel_path
    mime = MIME[p.suffix.lower()]
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

# inline the stylesheet
html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}\n</style>")

# replace every assets/... reference (img src and CSS url(...)) with a data URI
for rel in sorted(set(re.findall(r'assets/[^\s"\')]+', html))):
    html = html.replace(rel, data_uri(rel))

out = ROOT / "infinite-audio-video.html"
out.write_text(html)
print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
