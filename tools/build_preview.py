#!/usr/bin/env python3
"""Bundle index.html + style.css + script.js + logos into ONE self-contained file.

    python3 tools/build_preview.py                 -> scholaredu-preview.html
    python3 tools/build_preview.py --fragment OUT  -> head/body-less variant for artifact hosting

Edit index.html / style.css / script.js (the sources), then re-run this script.
"""
import base64, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read(p):
    return (ROOT / p).read_text(encoding="utf-8")


def data_uri(path):
    raw = (ROOT / path).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


def bundle():
    html = read("index.html")
    html = re.sub(r'src="(logo/[^"]+\.svg)"', lambda m: f'src="{data_uri(m.group(1))}"', html)
    html = re.sub(r'href="(logo/[^"]+\.svg)"', lambda m: f'href="{data_uri(m.group(1))}"', html)
    html = re.sub(r'<link rel="stylesheet" href="([\w./-]+\.css)">', lambda m: "<style>\n" + read(m.group(1)) + "\n</style>", html)
    html = re.sub(r'<script src="([\w./-]+\.js)"></script>', lambda m: "<script>\n" + read(m.group(1)) + "\n</script>", html)
    assert not re.search(r'href="[\w./-]+\.css"|src="[\w./-]+\.js"|src="logo/', html), "unbundled local file left"
    return html


def to_fragment(html):
    """Artifact hosting wraps the page itself: keep <title>, <style>, body content, scripts."""
    title = re.search(r"<title>.*?</title>", html, re.S).group(0)
    fonts = re.findall(r'<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', html)
    styles = "\n".join(re.findall(r"<style>.*?</style>", html, re.S))
    body = re.search(r"<body[^>]*>(.*)</body>", html, re.S).group(1)
    return "\n".join([title, *fonts, styles, body.strip()]) + "\n"


if __name__ == "__main__":
    html = bundle()
    if len(sys.argv) > 2 and sys.argv[1] == "--fragment":
        out = pathlib.Path(sys.argv[2])
        out.write_text(to_fragment(html), encoding="utf-8")
    else:
        out = ROOT / "scholaredu-preview.html"
        out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
