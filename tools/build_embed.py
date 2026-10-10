#!/usr/bin/env python3
"""Build embed/career-matching.html: the matching widget as ONE file for Wix "Embed HTML".

    python3 tools/build_embed.py

Sources: matching.js (logic + job/program tables) and matching.css. Edit those, then re-run.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
css = (ROOT / "matching.css").read_text(encoding="utf-8")
js = (ROOT / "matching.js").read_text(encoding="utf-8")

page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Career Discovery &amp; Matching — The Scholar Edu</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
  /* Wix에서 이 블록이 놓이는 섹션 배경색을 #ffffff(흰색)로 맞추면 경계 없이 자연스럽습니다. */
  :root {{ --bg:#ffffff; --band:#faf6f0; --surface:#ffffff; --text:#1e1e1a; --muted:#5b574f; --border:#e6e0d4; --line:#1e1e1a;
          --yellow:#ffda00; --purple:#ca92fc; --teal:#2aceaa; --yellow-soft:#fff4b3; --purple-soft:#efe1fe; --teal-soft:#d6f5ed;
          --on-color:#1e1e1a; --accent:#6b2fb3; --accent-soft:#efe1fe; --btn-bg:#ffda00; --btn-fg:#1e1e1a; --radius:18px; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 20px 16px; background: var(--bg); color: var(--text);
         font: 16px/1.7 "Noto Sans KR", -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif; word-break: keep-all; }}
  .wrap {{ max-width: 920px; margin: 0 auto; }}
  .btn {{ display: inline-block; padding: 10px 22px; border: 1.5px solid var(--line); border-radius: 999px; background: var(--surface); color: var(--text); font: inherit; font-weight: 700; font-size: 0.92rem; text-decoration: none; cursor: pointer; transition: transform .15s, box-shadow .15s; }}
  .btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 0 var(--line); }}
  .btn.primary {{ background: var(--btn-bg); border-color: var(--btn-bg); color: var(--btn-fg); }}
  .btn:focus-visible {{ outline: 3px solid var(--purple); outline-offset: 2px; }}
  .muted {{ color: var(--muted); }}
  .note {{ color: var(--muted); font-size: 0.85rem; }}
  .matcher {{ display: grid; gap: 14px; }}
</style>
<style>
{css}
</style>
</head>
<body>
<div class="wrap"><div id="matcher"></div></div>

<script>
{js}
</script>
<script>
/* 설정: 언어는 "ko" 또는 "en". 링크는 Wix 사이트 주소에 맞게 바꾸세요. 빈 문자열("")이면 해당 버튼이 숨겨집니다. */
initMatcher(document.getElementById("matcher"), {{
  lang: "ko",
  contactHref: "mailto:info@thescholaredu.com",   // 예: "https://내사이트주소/#contact"
  programHref: "",                                 // 예: "https://내사이트주소/#program"
  target: "_top"
}});
</script>
</body>
</html>
"""
out = ROOT / "embed" / "career-matching.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size/1024:.0f} KB)")
