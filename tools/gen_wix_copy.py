#!/usr/bin/env python3
"""Single source of truth for the Wix copy sheet (Korean / English).

    python3 tools/gen_wix_copy.py                 -> wix-copy.md + wix-copy.html
    python3 tools/gen_wix_copy.py --fragment OUT  -> artifact-hosting variant of the html

Edit the SECTIONS list below, then re-run.
"""
import html as H
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_preview import to_fragment  # noqa: E402

# (section title, where to put it in Wix, [(label, korean, english), ...])
SECTIONS = [
    ("0. 사이트 설정 (SEO)", "Wix 대시보드 → Settings / Marketing & SEO → 사이트 제목·설명", [
        ("사이트 제목", "더 스칼라 에듀 | 진로교육 · 글로벌교육 컨설팅", "The Scholar Edu | Career & Global Education Consulting"),
        ("검색 설명문", "더 스칼라 에듀는 호주의 학교·대학·산업 현장·멘토를 직접 경험하며 진로를 발견하도록 돕는 진로교육 · 글로벌교육 컨설팅입니다.",
         "The Scholar Edu helps young people discover their path by experiencing real Australian schools, universities, workplaces and mentors. Career education and global education consulting."),
        ("로고 태그라인", "진로교육 · 글로벌교육 컨설팅", "Global Education Consulting"),
        ("슬로건", "더 나은 교육. 더 밝은 미래.", "Better Education. Brighter Futures."),
    ]),
    ("1. 메뉴 (헤더)", "Editor → Menu (앵커 메뉴로 각 섹션에 연결)", [
        ("메뉴 1", "철학", "Our Approach"),
        ("메뉴 2", "진로탐색·매칭", "Discovery & Matching"),
        ("메뉴 3", "프로그램", "Programs"),
        ("메뉴 4", "멘토", "Mentor"),
        ("메뉴 5", "문의", "Contact"),
    ]),
    ("2. 히어로 (첫 화면)", "스트립 1 · 작은 글씨 + 큰 제목 + 설명 + 버튼 3개", [
        ("작은 글씨", "더 스칼라 에듀 · The Scholar Edu | 진로교육 · 글로벌교육 컨설팅", "The Scholar Edu | Career Education · Global Education Consulting"),
        ("큰 제목 (2줄)", "당신의 미래는 밖에 있습니다.\n직접 경험해 보세요.", "Your future is out there.\nGo experience it."),
        ("설명 1", "호주의 실제 경험, 멘토, 교육 경로를 연결해 학생이 무엇을 좋아하고, 무엇을 잘하며, 어디에 어울리는지 스스로 발견하도록 돕습니다.",
         "We connect young people with real-world experiences, mentors and educational pathways in Australia, helping them discover what they enjoy, what they are good at, and where they might belong."),
        ("설명 2", "진로를 “고르기” 전에 먼저 “경험”해 보세요. 호주의 학교·대학·현장·멘토를 직접 만나며 나에게 맞는 길을 찾습니다.",
         "Before you choose a career, experience it. Meet real schools, universities, workplaces and mentors in Australia and find the path that fits you."),
        ("버튼 1 (→ 프로그램)", "프로그램 보기", "Explore Programs"),
        ("버튼 2 (→ 멘토)", "멘토 만나기", "Meet a Mentor"),
        ("버튼 3 (→ 진로탐색 & 매칭)", "나의 진로 경로 찾기", "Discover Your Pathway"),
    ]),
    ("3. 철학 (Experience → Reflection → Pathway)", "스트립 2 · 제목 + 한 줄 설명 + 카드 5개", [
        ("제목", "경험 → 성찰 → 진로 경로", "Experience → Reflection → Pathway"),
        ("한 줄 설명", "진로를 고르기만 하지 마세요. 경험해 보세요.\n검사로 진로를 “결정”하지 않고, 경험을 통해 스스로 좁혀 갑니다.",
         "Don't just choose a career. Experience it.\nTests alone don't decide a path. Students narrow it down through experience."),
        ("카드 1 제목", "탐색", "Explore"),
        ("카드 1 설명", "관심 분야를 찾습니다. 의학, 비즈니스, 공학, AI, 교육, 디자인, 미디어, 법, 스포츠, 환경.",
         "Find your interests: medicine, business, engineering, AI, education, design, media, law, sport and the environment."),
        ("카드 2 제목", "경험", "Experience"),
        ("카드 2 설명", "학교·대학·산업 현장·미래 프로젝트를 직접 경험합니다. 가장 중요한 단계입니다.",
         "Try schools, universities, industry sites and future projects first-hand. This is the heart of what we do."),
        ("카드 3 제목", "만남", "Connect"),
        ("카드 3 설명", "그 일을 실제로 하는 사람을 만나 이야기를 듣습니다.", "Meet people who actually do the work and hear their story."),
        ("카드 4 제목", "성찰", "Reflect"),
        ("카드 4 설명", "무엇이 즐거웠고, 어려웠고, 놀라웠는지 스스로 돌아보고 기록합니다.",
         "Look back on what you enjoyed, what was hard and what surprised you, and keep a record."),
        ("카드 5 제목", "진로 경로", "Pathway"),
        ("카드 5 설명", "마지막에 비로소 교육과정과 호주 진학 경로를 연결합니다.",
         "Only then do we connect the right courses and Australian study pathways."),
    ]),
    ("4. 진로탐색 & 매칭", "스트립 3 · 제목 + 설명 + 3단계 카드 + (아래 임베드 코드 embed/career-matching.html 을 붙여 넣으면 유형 6개·직업군 목록·프로그램 연결 문구는 코드 안에 이미 들어 있습니다)", [
        ("제목", "진로탐색 & 매칭", "Career Discovery & Matching"),
        ("한 줄 설명", "무료 진로 흥미 검사를 한 뒤 결과 코드를 입력하면, 어울리는 직업군과 프로그램을 연결해 드립니다.",
         "Take a free career interest test, enter your result code, and we match you with suitable job groups and programs."),
        ("단계 1 제목", "검사하기", "Take the test"),
        ("단계 1 설명", "무료 흥미 검사(O*NET Interest Profiler)로 나의 흥미 유형을 확인합니다.", "Find your interest types with the free O*NET Interest Profiler."),
        ("단계 1 버튼 (→ https://www.mynextmove.org/explore/ip)", "검사 바로가기 (영어)", "Go to the test"),
        ("단계 2 제목", "결과 입력", "Enter your result"),
        ("단계 2 설명", "점수가 높은 순서대로 유형 3개를 아래에서 고릅니다. 검사를 아직 안 했다면 설명을 읽고 끌리는 유형을 골라도 됩니다.",
         "Pick your top three types in order, highest score first. If you have not taken the test, choose the types that appeal to you."),
        ("단계 3 제목", "매칭 확인", "See your matches"),
        ("단계 3 설명", "어울리는 직업군과 연결되는 프로그램을 확인합니다.", "See the job groups that fit you and the programs they connect to."),
        ("유형 R", "현실형 (Realistic) — 직접 만들고, 고치고, 다루는 일을 좋아합니다.", "Realistic — You like hands-on work: building, fixing and operating things."),
        ("유형 I", "탐구형 (Investigative) — 궁금한 것을 분석하고 연구하는 일을 좋아합니다.", "Investigative — You like analysing problems and researching how things work."),
        ("유형 A", "예술형 (Artistic) — 상상하고 표현하고 창작하는 일을 좋아합니다.", "Artistic — You like imagining, expressing and creating."),
        ("유형 S", "사회형 (Social) — 사람을 돕고 가르치고 돌보는 일을 좋아합니다.", "Social — You like helping, teaching and caring for people."),
        ("유형 E", "진취형 (Enterprising) — 이끌고 설득하고 새로운 일을 벌이는 것을 좋아합니다.", "Enterprising — You like leading, persuading and starting new things."),
        ("유형 C", "관습형 (Conventional) — 자료를 정리하고 규칙에 맞게 정확하게 처리하는 일을 좋아합니다.", "Conventional — You like organising information and working accurately to clear rules."),
        ("안내문", "샘플입니다. 직업군 매칭은 홀랜드(RIASEC) 흥미 유형에 따른 일반적인 분류이며, 진로를 결정해 주는 결과가 아닙니다. 검사 결과를 자동으로 가져오는 정식 연동은 준비 중입니다.",
         "This is a sample. Job group matching follows the general Holland (RIASEC) interest types and does not decide your career. Automatic import of test results is in preparation."),
    ]),
    ("5. 프로그램 (직무 관련 세미나 · 커리어 전환)", "스트립 4 · 제목 + 프로그램 카드 2개 (프로그램 1 안에 카테고리 카드 2개)", [
        ("제목", "프로그램", "Programs"),
        ("한 줄 설명", "대학 · 기관 · 산업체와 함께 직무와 학업을 연결하는 두 가지 프로그램입니다.",
         "Two programs that connect careers and study, together with universities, organisations and industry."),
        ("프로그램 1 제목", "직무 관련 세미나 프로그램", "Job-Related Seminar Program"),
        ("프로그램 1 설명", "대학, 기관, 산업체를 묶어 직무와 연결된 세미나로 구성합니다. 관심 있는 분야를 골라 참여하세요.",
         "Universities, organisations and industry come together in seminars built around real job roles. Choose the field that interests you."),
        ("프로그램 1 참여 주체", "대학 · 기관 · 산업체", "Universities · Organisations · Industry"),
        ("카테고리 1 제목", "Biotechnology & Bioengineering", "Biotechnology & Bioengineering"),
        ("카테고리 1 설명", "생명과학을 바탕으로 공학, 기술, AI 등을 결합해 새로운 기술과 제품을 개발하는 분야",
         "Fields that build on the life sciences and combine engineering, technology and AI to develop new technologies and products."),
        ("카테고리 2 제목", "Medicine, Nursing & Health Sciences", "Medicine, Nursing & Health Sciences"),
        ("카테고리 2 설명", "인간의 건강을 유지하고 질병을 예방·진단·치료하며 환자의 회복을 지원하는 분야",
         "Fields that maintain human health, prevent, diagnose and treat disease, and support patients' recovery."),
        ("프로그램 2 제목", "커리어 전환 및 학업 병행 프로그램", "Career Change & Study Program"),
        ("프로그램 2 설명", "직업과 연관된 학과의 커리어 과정을 통해 커리어 전환과 학업을 병행합니다.",
         "Change careers while you study, through career courses in the departments linked to the job."),
        ("안내문", "프로그램은 개발 중이며, 일정·장소·참가 조건은 각 기관 및 학교의 정책과 협의 결과에 따라 달라질 수 있습니다.",
         "These programs are in development. Schedule, locations and eligibility depend on each organisation's and school's policy."),
    ]),
    ("6. 멘토 소개", "스트립 5 · 사진 + 이름 + 직함 3줄", [
        ("제목", "멘토 소개", "Meet Your Mentor"),
        ("이름", "Liz Yum", "Liz Yum"),
        ("직함", "진로·교육 멘토", "Career & Education Mentor"),
        ("경력 1", "더 스칼라 에듀 (The Scholar Edu) — 대표", "The Scholar Edu — Founder"),
        ("경력 2", "Korean Language School teacher", "Korean Language School — Teacher"),
        ("경력 3", "호주한인상공회의소 사무국위원장",
         "Korean Chamber of Commerce in Australia — Chair of the Secretariat  ※ 공식 영문 명칭·직함을 확인해 맞춰 주세요"),
    ]),
    ("7. 문의", "스트립 6 · 제목 + 안내 + Wix 문의 폼 (받는 메일: info@thescholaredu.com)", [
        ("제목", "문의하기", "Contact"),
        ("안내", "프로그램, 멘토링, 학교·기관 협력 제안 모두 환영합니다.", "Programs, mentoring or partnership proposals are all welcome."),
        ("이메일", "info@thescholaredu.com", "info@thescholaredu.com"),
        ("폼 필드 1", "이름", "Name"),
        ("폼 필드 2", "이메일", "Email"),
        ("폼 필드 3", "문의 내용 / 관심 분야", "Message / Area of interest"),
        ("보내기 버튼", "보내기", "Send"),
        ("전송 완료 문구", "문의가 접수되었습니다. 곧 연락드리겠습니다.", "Thank you. We have received your message and will get back to you soon."),
    ]),
    ("8. 푸터", "맨 아래 · 세로형 로고 + 저작권", [
        ("저작권", "© 2026 더 스칼라 에듀 The Scholar Edu · Liz Yum. All rights reserved.", "© 2026 The Scholar Edu · Liz Yum. All rights reserved."),
    ]),
]

STEPS = [
    ("Wix 가입 · 새 사이트", "wix.com 가입 → 새 사이트 만들기. 가입 시 이름은 <b>liz</b>로 입력합니다. 사이트 만드는 방식은 <b>Wix Editor 직접 만들기(빈 템플릿)</b>를 권합니다. Wix가 묻는 사이트 종류는 ‘교육 · 컨설팅’ 계열을 고르면 됩니다."),
    ("사이트 이름과 제목 구분", "대시보드의 <b>사이트 이름은 관리용(liz)</b>입니다. 방문자에게 보이는 제목은 SEO 설정의 ‘사이트 제목’(위 0번 문구)에서 정합니다."),
    ("색상 · 글꼴 설정", "사이트 디자인에서 색을 먹색 <code>#1e1e1a</code>, 노랑 <code>#ffda00</code>, 연보라 <code>#ca92fc</code>, 민트 <code>#2aceaa</code>, 크림 <code>#faf6f0</code>로 정합니다. 로고와 명함은 네이비·골드 그대로입니다. 본문 글꼴은 Wix의 한글 지원 고딕(예: Noto Sans KR 계열)을 고릅니다."),
    ("로고 업로드", "미디어 관리자에 <code>logo/</code> 폴더 이미지를 올립니다. 헤더는 <code>scholar-horizontal-light</code>, 푸터는 <code>scholar-logo-light</code>, 파비콘은 <code>scholar-monogram-light</code> 를 씁니다."),
    ("페이지 구조", "한 페이지 사이트(홈) + 앵커 메뉴를 권합니다. 위 1번 메뉴 5개를 각 섹션(스트립)에 연결합니다."),
    ("섹션별 문구 붙여넣기", "이 문서의 2~8번을 위에서 아래 순서대로 붙여 넣습니다. 한글·영문을 함께 보여 줄 문장은 줄바꿈으로 나란히 두면 됩니다."),
    ("진로탐색 & 매칭 넣기", "문구(4번)로 제목·설명·3단계 카드를 만들고, 그 아래에 Add → Embed Code → Embed HTML → Code 탭을 열어 <code>embed/career-matching.html</code> 파일 전체를 붙여 넣습니다. 상자 높이는 데스크톱 약 1100px, 모바일 약 1700px로 시작해 맞춥니다(결과가 가장 길게 나올 때 기준). 영문은 코드 맨 아래 <code>lang: \"ko\"</code>를 <code>\"en\"</code>으로 바꾸고, <code>contactHref</code>·<code>programHref</code>에는 Wix 사이트 주소(예: <code>https://내사이트주소/#contact</code>)를 넣습니다."),
    ("문의 폼", "Add → Contact & Forms(연락처/폼)에서 문의 폼을 넣고, 필드는 이름 · 이메일 · 문의 내용(7번)으로 맞춥니다. 알림 받을 이메일을 <code>info@thescholaredu.com</code> 으로 설정하고, 폼을 직접 한 번 제출해 메일이 오는지 확인합니다."),
    ("이미지 교체", "히어로와 멘토 프로필에 사용할 이미지를 올립니다. 사용 허용 범위(웹사이트·상업 이용)를 구매 전에 확인합니다."),
    ("모바일 확인", "상단의 모바일 보기로 전환해 글 줄바꿈, 버튼, 임베드 상자 높이를 확인합니다. 모바일은 따로 조정이 필요합니다."),
    ("SEO · 공유 이미지", "SEO 설정에 0번 제목·설명을 넣고, 소셜 공유 이미지에는 세로형 로고(<code>scholar-logo-dark.png</code>)나 대표 사진을 지정합니다."),
    ("한글/영문 두 언어", "두 언어 사이트가 필요하면 Wix의 다국어(Multilingual) 기능을 사용합니다. 이 문서의 영문 열을 영어 페이지에 붙여 넣으면 됩니다. 사용 조건과 요금은 Wix 안내에서 확인하세요."),
    ("도메인 · 플랜", "무료 플랜은 wixsite.com 주소와 Wix 광고가 붙습니다. thescholaredu.com 을 연결하려면 유료 플랜과 도메인 연결이 필요합니다. 이미 info@thescholaredu.com 메일을 쓰고 있다면, 도메인 DNS를 바꿀 때 메일 설정(MX 레코드)이 유지되는지 먼저 확인하세요."),
    ("게시", "Publish(게시)를 눌러 공개한 뒤, 휴대폰과 PC에서 로고 · 문의 · 임베드 · 링크가 모두 동작하는지 확인합니다."),
]


def md():
    out = ["# 더 스칼라 에듀 · Wix 복붙용 문구 (한글 / English)", "",
           "각 칸의 문구를 그대로 복사해 Wix에 붙여 넣으세요. 줄바꿈이 있는 문구는 줄바꿈까지 포함입니다.", "",
           "## Wix 가입 이후 진행 순서", ""]
    for i, (t, d) in enumerate(STEPS, 1):
        txt = d.replace("<b>", "**").replace("</b>", "**").replace("<code>", "`").replace("</code>", "`")
        out.append(f"{i}. **{t}**: {txt}")
    out.append("")
    for title, where, rows in SECTIONS:
        out += [f"## {title}", f"_{where}_", "", "| 항목 | 한글 | English |", "|---|---|---|"]
        for label, ko, en in rows:
            out.append(f"| {label} | {ko.replace(chr(10), '<br>')} | {en.replace(chr(10), '<br>')} |")
        out.append("")
    return "\n".join(out) + "\n"


def head_html():
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wix Copy Sheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#f7f4ec; --surface:#ffffff; --text:#14233a; --muted:#5f6879; --border:#e3dfd2; --accent:#9a7632; --btn-bg:#14233a; --btn-fg:#f7f4ec; --soft:#f1e8d3; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0e1a2d; --surface:#16253d; --text:#f3efe4; --muted:#a3abbd; --border:#2b3a55; --accent:#c9a45f; --btn-bg:#c9a45f; --btn-fg:#14233a; --soft:#2b3140; color-scheme: dark; }} }}
  :root[data-theme="dark"] {{ --bg:#0e1a2d; --surface:#16253d; --text:#f3efe4; --muted:#a3abbd; --border:#2b3a55; --accent:#c9a45f; --btn-bg:#c9a45f; --btn-fg:#14233a; --soft:#2b3140; color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--text); font: 16px/1.65 "Noto Sans KR", -apple-system, "Malgun Gothic", sans-serif; word-break: keep-all; }}
  .page {{ max-width: 1040px; margin: 0 auto; padding: 28px 16px 64px; }}
  h1 {{ margin: 0 0 6px; font-size: 1.7rem; letter-spacing: -0.02em; }}
  .intro {{ margin: 0 0 24px; color: var(--muted); }}
  h2 {{ margin: 36px 0 2px; font-size: 1.2rem; }}
  .where {{ margin: 0 0 10px; color: var(--muted); font-size: .88rem; }}
  ol.steps {{ margin: 0; padding: 0; list-style: none; counter-reset: s; display: grid; gap: 8px; }}
  ol.steps li {{ counter-increment: s; display: grid; grid-template-columns: 2rem 1fr; gap: 2px 8px; padding: 12px 14px; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; }}
  ol.steps li::before {{ content: counter(s); grid-row: span 2; font-weight: 700; color: var(--accent); }}
  ol.steps li span {{ color: var(--muted); font-size: .94rem; }}
  code {{ background: var(--soft); padding: 1px 6px; border-radius: 6px; font-size: .88em; }}
  .row {{ display: grid; grid-template-columns: 9.5rem 1fr 1fr; gap: 8px; padding: 8px 0; border-top: 1px solid var(--border); align-items: start; }}
  .row.head {{ border-top: 0; color: var(--muted); font-size: .8rem; font-weight: 700; letter-spacing: .06em; padding-bottom: 2px; }}
  .lbl {{ color: var(--muted); font-size: .88rem; padding-top: 2px; min-width: 0; }}
  .cell {{ display: flex; gap: 8px; align-items: flex-start; justify-content: space-between; min-width: 0; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 8px 10px; }}
  .cell p {{ margin: 0; min-width: 0; overflow-wrap: anywhere; user-select: all; }}
  .copy {{ flex: none; border: 0; background: var(--btn-bg); color: var(--btn-fg); border-radius: 999px; padding: 3px 12px; font: inherit; font-size: .82rem; font-weight: 500; cursor: pointer; }}
  .copy:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
  .copy.done {{ background: var(--accent); color: var(--bg); }}
  @media (max-width: 760px) {{ .row {{ grid-template-columns: 1fr; gap: 6px; }} .row.head {{ display: none; }} .lbl {{ font-weight: 700; padding-top: 8px; }} }}
</style>
"""


def html_doc():
    steps = "".join(f"<li><div><b>{t}</b><br><span>{d}</span></div></li>" for t, d in STEPS)
    body = [f'<div class="page"><h1>더 스칼라 에듀 · Wix 복붙용 문구</h1>',
            '<p class="intro">각 칸의 <b>복사</b> 버튼을 누르고 Wix에 붙여 넣으세요. 복사가 안 되면 문구를 한 번 클릭하면 전체가 선택됩니다. 한글 열은 한국어 사이트, English 열은 영어 사이트나 영문 병기에 씁니다.</p>',
            f'<h2>Wix 가입 이후 진행 순서</h2><p class="where">메뉴 이름은 Wix 화면 업데이트에 따라 조금 다를 수 있습니다.</p><ol class="steps">{steps}</ol>']
    for title, where, rows in SECTIONS:
        trs = []
        for label, ko, en in rows:
            def cell(txt, lang):
                return (f'<div class="cell"><p lang="{lang}">{H.escape(txt).replace(chr(10), "<br>")}</p>'
                        f'<button type="button" class="copy" data-text="{H.escape(txt, quote=True)}">복사</button></div>')
            trs.append(f'<div class="row"><div class="lbl">{H.escape(label)}</div>{cell(ko, "ko")}{cell(en, "en")}</div>')
        body.append(f'<section><h2>{H.escape(title)}</h2><p class="where">{H.escape(where)}</p>'
                    f'<div class="row head"><div></div><div>한글</div><div>English</div></div>{"".join(trs)}</section>')
    body.append("</div>")
    script = """<script>
document.addEventListener("click", async (e) => {
  const b = e.target.closest(".copy");
  if (!b) return;
  const text = b.dataset.text;
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    const p = b.parentElement.querySelector("p");
    const r = document.createRange(); r.selectNodeContents(p);
    const s = getSelection(); s.removeAllRanges(); s.addRange(r);
    b.textContent = "Ctrl+C";
    setTimeout(() => (b.textContent = "복사"), 1800);
    return;
  }
  b.textContent = "복사됨"; b.classList.add("done");
  setTimeout(() => { b.textContent = "복사"; b.classList.remove("done"); }, 1400);
});
</script>"""
    return head_html() + "</head>\n<body>\n" + "\n".join(body) + "\n" + script + "\n</body>\n</html>\n"


if __name__ == "__main__":
    doc = html_doc()
    if len(sys.argv) > 2 and sys.argv[1] == "--fragment":
        out = pathlib.Path(sys.argv[2])
        out.write_text(to_fragment(doc), encoding="utf-8")
    else:
        (ROOT / "wix-copy.md").write_text(md(), encoding="utf-8")
        out = ROOT / "wix-copy.html"
        out.write_text(doc, encoding="utf-8")
    print("wrote", out)
