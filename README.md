# 더 스칼라 에듀 (The Scholar Edu) 웹사이트

진로교육 · 글로벌교육 컨설팅. 대표 Liz Yum. 문의 `info@thescholaredu.com`

## 파일 안내

| 파일 | 용도 |
|---|---|
| `scholaredu-preview.html` | **링크 · 미리보기용 단일 파일.** 더블클릭하면 열리고 다른 파일 없이 그대로 공유할 수 있습니다. |
| `index.html` `style.css` `script.js` | 사이트 **원본**. 내용을 고칠 때는 여기를 고칩니다. |
| `embed/self-discovery.html` | Wix 「HTML 임베드」에 붙이는 관심사 테스트 (한글/영문 전환 가능) |
| `wix-copy.html` `wix-copy.md` | Wix에 붙여 넣을 한글/영문 문구 + 가입 이후 진행 순서 |
| `card.html` | 명함 시안 (인쇄용 이미지는 `logo/card-front.png`, `logo/card-back.png`) |
| `logo/` | 로고 SVG · PNG (`light`=밝은 배경용, `dark`=네이비 배경용) |
| `tools/` | 단일 파일 · 문구 정리본 · 로고를 다시 만드는 스크립트 |

## 내용을 수정하는 방법

### 방법 1. Claude에게 요청 (가장 쉬움)
이 저장소를 열어 두고 “히어로 문구를 이렇게 바꿔줘”, “명함 전화번호를 +61 …로 바꿔줘”처럼 말하면 원본 수정 → 단일 파일 재생성 → 저장까지 해 줍니다.

### 방법 2. 직접 수정
1. `index.html`을 메모장/VS Code로 열어 글을 고칩니다. 색은 `style.css` 맨 위 `:root`에 모여 있습니다.
2. 아래 명령으로 단일 파일을 다시 만듭니다. Windows는 `python` 대신 `py`를 쓰세요.
   ```
   python3 tools/build_preview.py      # scholaredu-preview.html 갱신
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
| 색상 | `style.css` 맨 위 `:root` (네이비 `#14233a`, 골드 `#b08d4c`, 크림 `#f7f4ec`) |
| 명함 PNG 다시 만들기 | `card.html`을 브라우저에서 열어 앞면/뒷면을 1050×600px로 캡처 |
| 로고 모양 | `tools/logo/gen_logo.py` (설명은 파일 맨 위) |
| Wix 문구 | `tools/gen_wix_copy.py`의 `SECTIONS` 목록 → 스크립트 재실행 |

## 아직 채워야 할 것
- 체험 카드 4개 이미지와 히어로 이미지 (구매한 이미지를 `images/`에 넣고 연결)
- 멘토 소개의 프로필 사진
- 호주한인상공회의소의 공식 영문 명칭과 직함(사무국위원장)
- 사이트 영어 소개 문구가 서비스에 맞는지 최종 확인
- 협력 후보 기관 목록은 확정된 파트너십이 아니므로, 실제로 확인되면 문구를 바꿀 것
