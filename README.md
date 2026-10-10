# 더 스칼라 에듀 (The Scholar Edu) 웹사이트

진로교육 · 글로벌교육 컨설팅. 대표 Liz Yum. 문의 `info@thescholaredu.com`

## 파일 안내

| 파일 | 용도 |
|---|---|
| `scholaredu-preview.html` | **링크 · 미리보기용 단일 파일.** 더블클릭하면 열리고 다른 파일 없이 그대로 공유할 수 있습니다. |
| `index.html` `style.css` `script.js` | 사이트 **원본**. 내용을 고칠 때는 여기를 고칩니다. |
| `matching.js` `matching.css` | **진로탐색 & 매칭 위젯** (흥미 유형 → 직업군 · 프로그램 연결). 유형 · 직업군 · 프로그램 표가 `matching.js` 맨 위에 있습니다. |
| `embed/career-matching.html` | 위 위젯을 파일 하나로 합친 Wix 「HTML 임베드」용 코드 (`python3 tools/build_embed.py`로 생성, 한글/영문 전환 가능) |
| `wix-copy.html` `wix-copy.md` | Wix에 붙여 넣을 한글/영문 문구 + 가입 이후 진행 순서 |
| `card.html` | 명함 시안 (인쇄용 이미지는 `logo/card-front.png`, `logo/card-back.png`) |
| `images/` | 프로그램 그림 3개 (`program-biotech` · `program-health` · `program-career`, SVG + PNG). 직접 그린 원본 일러스트라 저작권 걱정 없이 쓸 수 있습니다. |
| `logo/` | 로고 SVG · PNG (`light`=밝은 배경용, `dark`=네이비 배경용) |
| `tools/` | 단일 파일 · 문구 정리본 · 로고 · 프로그램 그림을 다시 만드는 스크립트 |

## 내용을 수정하는 방법

### 방법 1. Claude에게 요청 (가장 쉬움)
이 저장소를 열어 두고 “히어로 문구를 이렇게 바꿔줘”, “명함 전화번호를 +61 …로 바꿔줘”처럼 말하면 원본 수정 → 단일 파일 재생성 → 저장까지 해 줍니다.

### 방법 2. 직접 수정
1. `index.html`을 메모장/VS Code로 열어 글을 고칩니다. 색은 `style.css` 맨 위 `:root`에 모여 있습니다.
2. 아래 명령으로 단일 파일을 다시 만듭니다. Windows는 `python` 대신 `py`를 쓰세요.
   ```
   python3 tools/build_preview.py      # scholaredu-preview.html 갱신
   python3 tools/build_embed.py        # embed/career-matching.html 갱신
   python3 tools/gen_wix_copy.py       # wix-copy.html / wix-copy.md 갱신
   ```
3. `scholaredu-preview.html`을 열어 확인합니다.

### 방법 3. Wix로 옮긴 뒤
Wix 편집기에서 직접 고칩니다. 이 저장소는 디자인·문구의 기준 자료로 보관하세요. Wix 쪽 수정은 저장소에 자동 반영되지 않습니다.

## 자주 바꾸는 항목

| 바꿀 것 | 위치 |
|---|---|
| 히어로 · 소개 문구 | `index.html` (`class="hero"` 부분) |
| 이메일 | `index.html` 문의 섹션 (`info@thescholaredu.com` 두 곳) · `card.html` |
| 명함 연락처 | `card.html`의 `.contact` (이메일 · 전화 `+61 415 732 723`) |
| 사이트 색상 | `style.css` 맨 위 `:root` (먹색 `#1e1e1a`, 노랑 `#ffda00`, 연보라 `#ca92fc`, 민트 `#2aceaa`, 크림 `#faf6f0`). 로고 · 명함은 네이비 `#14233a` · 골드 `#b08d4c` |
| 명함 PNG 다시 만들기 | `card.html`을 브라우저에서 열어 앞면/뒷면을 1050×600px로 캡처 |
| 로고 모양 | `tools/logo/gen_logo.py` (설명은 파일 맨 위) |
| 직업군 · 프로그램 매칭 내용 | `matching.js` 맨 위의 `JOBS`(유형별 직업군), `PROGRAMS`(프로그램별 가중치) |
| Wix 문구 | `tools/gen_wix_copy.py`의 `SECTIONS` 목록 → 스크립트 재실행 |

## 아직 채워야 할 것
- 멘토 프로필 사진 (지금은 `LY` 이니셜 원)
- 멘토 소개의 프로필 사진
- 호주한인상공회의소의 공식 영문 명칭과 직함(사무국위원장)
- 사이트 영어 소개 문구가 서비스에 맞는지 최종 확인
- 진로탐색 & 매칭은 샘플입니다. 검사 결과를 자동으로 가져오는 정식 연동은 아직 없습니다 (아래 ‘정식 연동 방법’ 참고)

## 진로탐색 & 매칭: 정식 연동으로 키우는 방법
현재는 사용자가 무료 검사(O*NET Interest Profiler)를 한 뒤 **결과의 유형 코드를 직접 고르는** 반자동 방식입니다. 완전한 자동 연동은 다음 순서로 확장할 수 있습니다.

1. **Wix 안에서 자체 검사 만들기** — `matching.js`에 문항을 추가해 점수를 계산하면 외부 검사 없이 한 화면에서 끝납니다.
2. **검사 → 직업 매칭 API 연결** — O*NET Web Services의 Interest Profiler 관련 기능을 쓰면 문항과 직업 매칭 결과를 서버에서 받아올 수 있습니다(무료 등록, 사용 조건은 등록 시 확인). Wix에서는 Velo 백엔드 코드가 필요합니다.
3. **한국/호주 직업 정보 연결** — 직업군 이름에 커리어넷(한국), myfuture · Job Outlook(호주)의 직업 정보 링크를 붙입니다.

## 그림을 실제 사진으로 바꾸는 방법
지금 프로그램 그림은 직접 그린 일러스트입니다. 사진을 쓰고 싶다면:
1. 상업적 이용이 허용되는 무료 사진(Unsplash · Pexels · Pixabay 등)이나 구매한 사진을 받습니다. 핀터레스트 이미지는 대부분 작성자에게 저작권이 있어 사이트에 그대로 쓸 수 없습니다.
2. 파일을 `images/`에 넣습니다 (예: `images/biotech.jpg`, 가로 1200px 이상, 3:2 비율 권장).
3. `index.html`에서 `class="art"`인 `<img>` 3곳의 `src`를 새 파일 이름으로 바꾸고, `python3 tools/build_preview.py`를 다시 실행합니다.

검색어 예시: 바이오공학 — `biotechnology laboratory`, `DNA research` / 의료·보건 — `nursing`, `healthcare students` / 커리어 전환 — `adult learner`, `career change student`. 사용 전에 각 사이트의 라이선스 문구를 확인하세요.
