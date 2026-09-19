---
version: D-001
name: Free-Traveler-design-canonical
status: LOCKED
description: Traveler 전용 디자인 정본. Airbnb 참고본(design-reference/vendor/airbnb/DESIGN.md)에서 레이아웃 문법(카드 밀도, 1단계 그림자, 여백 리듬)만 인용하고 상표·구매/예약·결제 UI는 일체 배제한다. 흰 캔버스(#FFFFFF) 위 짙은 회색 잉크(#242424)와 단일 코랄 포인트(#F0603F)로 구성되며, 오류·경고·안전정보는 코랄과 구분되는 별도 semantic 색을 쓴다. Inter + OS 기본 한글 폰트만 사용하고 별도 웹폰트 파일을 배포하지 않는다. SCR-001~005(Desktop) 및 SCR-001·SCR-003(Mobile) 승인 화면(STITCH_VALIDATION_REPORT.md 기준)에서 검증된 규칙만 반영한다.

colors:
  primary: "#F0603F"
  primary-active: "#D1492C"
  primary-tint: "#FDE3DB"
  ink: "#242424"
  body: "#4A4A4A"
  muted: "#6E6E6E"
  muted-soft: "#96938E"
  hairline: "#E4E1DC"
  hairline-soft: "#EDEBE6"
  border-strong: "#C7C5C0"
  canvas: "#FFFFFF"
  surface-soft: "#F7F6F4"
  surface-strong: "#F0EEEA"
  on-primary: "#FFFFFF"
  danger: "#C6362A"
  danger-bg: "#FBEAE8"
  warning: "#B0570A"
  warning-bg: "#FCEFDD"
  safety-info: "#1D5FBF"
  safety-info-bg: "#E7EFFB"
  success: "#1F7A4D"
  success-bg: "#E7F4EC"
  scrim: "#000000"

typography:
  display-xl:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: 0
  display-lg:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  display-md:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 20px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  title-md:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  title-sm:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  body-md:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  body-sm:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: 0
  caption:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: 0
  button:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: 0
  nav-link:
    fontFamily: "Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: 0

rounded:
  none: 0px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 20px
  full: 9999px

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  base: 16px
  md: 24px
  lg: 32px
  xl: 48px
  section-desktop-min: 64px
  section-desktop-max: 96px
  section-mobile-min: 40px
  section-mobile-max: 64px

elevation:
  flat: none
  card-hover: "0 2px 6px rgba(0,0,0,0.08)"
  drawer-modal: "0 2px 6px rgba(0,0,0,0.08)"

breakpoints:
  desktop: 1440px
  mobile: 390px
  container-max-desktop: "1200–1280px"

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 14px 24px
    height: 48px
  button-secondary:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: 13px 23px
    height: 48px
  search-bar-pill:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.full}"
    padding: 14px 24px
    height: 56px
  chip:
    backgroundColor: "{colors.surface-strong}"
    textColor: "{colors.ink}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 8px 16px
  chip-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    padding: 8px 16px
  destination-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
  mate-card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
  stat-card:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.display-md}"
    rounded: "{rounded.md}"
    padding: 24px
  badge-safety-info:
    backgroundColor: "{colors.safety-info-bg}"
    textColor: "{colors.safety-info}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 4px 10px
  badge-warning:
    backgroundColor: "{colors.warning-bg}"
    textColor: "{colors.warning}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: 4px 10px
  banner-danger:
    backgroundColor: "{colors.danger-bg}"
    textColor: "{colors.danger}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    padding: 16px
  toast-success:
    backgroundColor: "{colors.success-bg}"
    textColor: "{colors.success}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.sm}"
    padding: 12px 16px
  text-input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.body-md}"
    rounded: "{rounded.sm}"
    padding: 14px 12px
    height: 56px
  top-nav:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.nav-link}"
    height: 72px
  footer-light:
    backgroundColor: "{colors.surface-soft}"
    textColor: "{colors.ink}"
    typography: "{typography.body-sm}"
    padding: 48px 80px
---

## Overview

Free Traveler는 여행지 탐색·여행 도구·동행 매칭·안전정보를 하나로 묶는 여행 준비 허브다. 이 문서(D-001)는 `design-reference/vendor/airbnb/DESIGN.md`(Airbnb 참고본)에서 **레이아웃 문법**(카드 밀도, 단일 그림자 티어, 여백 리듬, 이미지 우선 카드 구조)만 인용하고, Airbnb의 상표·워드마크·색상(Rausch)·폰트(Cereal)·예약/결제 UI는 일절 사용하지 않는다. 이 문서는 `docs/04_UIUX_PLAN.md`의 화면 설계와 `docs/STITCH_VALIDATION_REPORT.md`에서 PASS 판정을 받은 SCR-001~005(Desktop) 및 SCR-001·SCR-003(Mobile) 승인 화면을 기준으로 고정(LOCKED)한 정본이다.

---

## 1. Visual Theme

- **톤:** 흰 캔버스 + 짙은 회색 잉크 + 단일 코랄 포인트. 사진(여행지·인물·동행 콘텐츠)이 시각적 무게를 담당하고, 타이포그래피는 20~32px 대역에서 절제된 굵기(600~700)만 사용한다.
- **코랄의 용도 제한:** Primary CTA, 활성 탭 밑줄, 즐겨찾기 On 상태에만 코랄을 쓴다. 오류·경고·안전정보·성공 알림에는 코랄을 쓰지 않고 §2의 semantic 색을 쓴다.
- **형태 언어:** 버튼·입력필드 8px, 카드 12px, Hero 이미지·Drawer 20px, 검색창·Chip·아바타는 완전 원형(pill). 하드 코너는 그리드 컨테이너 외에는 없다.
- **입체감:** 그림자는 단 1단계(`{elevation.card-hover}`)만 존재하며 카드 hover와 열린 Drawer/Modal에만 적용한다. 그 외 모든 면은 평면(flat)이다.

## 2. Color Token

| 토큰 | 값 | 용도 |
|---|---|---|
| `color.canvas` | `#FFFFFF` | 페이지 기본 배경 |
| `color.surface-soft` | `#F7F6F4` | 카드 그리드 교차 배경, Footer, Stat Card |
| `color.surface-strong` | `#F0EEEA` | Chip 배경, 아이콘 버튼 배경 |
| `color.ink` | `#242424` | 제목·본문 텍스트(순검정 금지) |
| `color.body` | `#4A4A4A` | 긴 설명문 |
| `color.muted` | `#6E6E6E` | 카드 메타(지역·기간·상태) |
| `color.muted-soft` | `#96938E` | 비활성 텍스트 |
| `color.hairline` / `hairline-soft` | `#E4E1DC` / `#EDEBE6` | 카드·헤더/푸터 1px 구분선 |
| `color.border-strong` | `#C7C5C0` | 폼 아웃라인 |
| `color.primary`(Coral) | `#F0603F` | Primary CTA, 활성 탭, 즐겨찾기 |
| `color.primary-active` | `#D1492C` | 코랄 버튼 press |
| `color.primary-tint` | `#FDE3DB` | 코랄 비활성/연한 배지 배경 |
| `color.on-primary` | `#FFFFFF` | 코랄 배경 위 텍스트 |
| `color.danger` / `danger-bg` | `#C6362A` / `#FBEAE8` | 폼 검증 실패, 외부 이동 실패 |
| `color.warning` / `warning-bg` | `#B0570A` / `#FCEFDD` | 중대 여행경보, 동행 안전 경고 |
| `color.safety-info` / `safety-info-bg` | `#1D5FBF` / `#E7EFFB` | 최종 확인일, 비전달 고지, 정보성 배지 |
| `color.success` / `success-bg` | `#1F7A4D` / `#E7F4EC` | 완료 Toast, 승인 상태 |
| `color.scrim` | `#000000`(40% opacity) | Drawer/Modal 배경 스크림 |

**규칙:** 이 표에 없는 임의 색상을 신규 추가하지 않는다. 새 의미가 필요하면 반드시 이 문서에 토큰을 먼저 등록한 뒤 화면에 적용한다.

## 3. Typography

- **폰트:** `Inter, 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif`. 영문·숫자는 Inter, 한글은 OS 기본 한글 폰트로 자연 대체한다. **Proprietary 폰트 파일(Airbnb Cereal 등)을 다운로드·번들하지 않는다.**

| 토큰 | 크기/굵기 | 용도 |
|---|---|---|
| `display-xl` | 32px/700 | 메인·About Hero 헤드라인 |
| `display-lg` | 24px/600 | Section 제목(전 화면 공통) |
| `display-md` | 20px/600 | Drawer/Modal 제목, Stat Card 수치 |
| `title-md` | 18px/600 | 카드 제목(여행지명, 모집글 제목) |
| `title-sm` | 16px/600 | 폼 라벨, Chip 라벨 |
| `body-md` | 16px/400 | 본문 문단 |
| `body-sm` | 14px/400 | 카드 메타, 캡션 |
| `caption` | 13px/500 | 배지, 타임스탬프 |
| `button` | 16px/600 | 버튼 라벨 |
| `nav-link` | 15px/600 | Header 내비게이션 |

## 4. Spacing

기본 단위 4px. `xxs`4·`xs`8·`sm`12·`base`16·`md`24·`lg`32·`xl`48px. Section 상하 여백은 Desktop **64~96px**, Mobile **40~64px** 범위에서만 정한다(§10 참조). 카드 그리드 내부 간격은 16px(base)를 기본으로 한다.

## 5. Radius

`none`0 · `xs`4 · `sm`8(버튼·입력) · `md`12(카드) · `lg`20(Hero 이미지·Drawer) · `full`9999px(검색창·Chip·아바타). 인터랙티브 컨트롤에 하드 코너를 쓰지 않는다.

## 6. Shadow

단일 티어만 존재: `0 2px 6px rgba(0,0,0,0.08)`. 적용 대상은 (1) 카드 hover, (2) 열린 Drawer/Modal 두 가지뿐이다. Hero·Section 배경·Footer 등 정적 면에는 그림자를 쓰지 않는다. 단계적(다층) 그림자를 추가하지 않는다.

## 7. Header·Footer (5개 Screen 공통)

- **Header:** Desktop 72px / Mobile 56px, 흰 배경 + 하단 1px hairline. 좌측 "Free Traveler" 텍스트 워드마크(코랄 점 아이콘 1개), 중앙/우측에 여행지·여행 도구·동행 찾기·대표 소개 내비게이션(활성 항목은 `color.ink` + 하단 2px 코랄 밑줄), 우측 끝에 로그인/계정 버튼. Mobile은 로고+햄버거로 축약.
- **Footer:** `surface-soft` 배경, 서비스/정책/안내 3컬럼(Desktop) → 1열 스택(Mobile). 정책 컬럼에 이용약관·개인정보 처리방침·동행 안전수칙·콘텐츠 면책 안내를 반드시 포함한다. Legal band에 "예약은 외부 사이트에서 진행되며 본 서비스는 결과를 제공하지 않습니다" 고지와 안전정보 출처 고지 문구를 고정 배치한다.

## 8. Search·Filter

- **전역 검색창(SCR-001 Hero):** `search-bar-pill`, 완전 원형, 56px 높이, 1px hairline.
- **Filter Chip(테마·연령대·스타일 등):** `chip`/`chip-active`. 비활성은 `surface-strong` 배경 + `ink` 텍스트, 활성은 코랄 배경 + 흰 텍스트.
- **동행 Filter 패널(SCR-004):** Desktop은 좌측 sticky 패널, Mobile은 상단 접이식 시트. 필터 변경 시 결과 카드가 즉시 갱신되고 "조건에 맞는 결과 N건" 요약 텍스트를 함께 표시한다.
- **빈 결과:** §14 Empty State 규칙을 따른다.

## 9. Destination Card / Mate Post Card

- **Destination Card:** 4:3 또는 1:1 사진 + `rounded.md` 클리핑, `title-md` 제목, `body-sm` 메타(지역·테마) 1~2줄. 안전정보 카드는 국가명 + 최종 확인일 배지(`badge-safety-info`, stale 시 `badge-warning`)를 포함한다.
- **Mate Post Card:** 제목(`title-md`), 국가·지역·기간(`body-sm`), 여행 스타일 Chip, 모집 상태 배지(모집중/마감, 색상+텍스트 병기). 연락처·이메일 등 공개 개인정보는 카드·상세 어디에도 노출하지 않는다.
- 두 카드 모두 hover 시에만 `{elevation.card-hover}` 적용, 평상시는 1px hairline 테두리만 유지한다.

## 10. Form·Tabs

- **Form 필드(`text-input`):** 흰 배경, 1px hairline, 8px radius, 56px 높이. 포커스 시 2px 코랄 테두리로 전환(글로우 없음). 오류 시 필드 하단에 `color.danger` 텍스트 + `banner-danger`.
- **Tabs(SCR-003 항공/숙소/동행 구하기):** 가로 균등 분할, 활성 탭은 `ink` 텍스트 + 하단 2px 코랄 밑줄, 비활성은 `muted`. 세 탭의 입력·검증·완료 상태는 서로 독립적으로 유지한다(한 탭에서 값이 남아도 다른 탭에 영향 없음).
- **계정 탭(SCR-005):** 좌측 세로 탭 메뉴(Desktop) / 상단 가로 스크롤 탭(Mobile). 역할(Guest/Member/Admin)에 없는 탭은 DOM에서 아예 제거한다.

## 11. Drawer·Modal

- 여행지 상세·안전정보 상세는 SCR-001 위에서 **Drawer/Modal**로 연다(별도 페이지 이동 없음). Desktop은 우측에서 슬라이드, Mobile은 하단에서 올라오는 전체 높이 Drawer.
- 배경 스크림은 `color.scrim` 40% 불투명도.
- Drawer/Modal 상단 모서리에만 `rounded.lg`(20px)를 적용하고, 열림 상태에서 `{elevation.drawer-modal}` 그림자를 준다.
- 동행 상세(SCR-004)는 Desktop에서 좌 40%/우 60% 화면 내 분할 패널로, Mobile에서는 카드 탭 시 Drawer로 연다.

## 12. Alert·Toast

- **Toast(성공/완료):** `toast-success`, 화면 하단 또는 상단에 짧게 노출, 이메일 발송 대신 참가 요청·승인·거절·신고 결과를 안내하는 유일한 채널이다.
- **Banner(정보/경고/오류):** 항상 아이콘 + 텍스트 라벨을 병기하고 색상만으로 의미를 구분하지 않는다.
  - 정보/비전달 고지 → `safety-info-bg`
  - 중대 경보/안전 수칙 → `warning-bg`
  - 검증 실패/외부 이동 실패 → `danger-bg`

## 13. Loading·Empty·Error 상태

| 상태 | 규칙 |
|---|---|
| Loading | 카드/목록/상세 영역에 제목·이미지 자리만 회색 블록으로 표시하는 스켈레톤. 스피너 단독 사용은 버튼 내부(외부 이동 대기)에 한정 |
| Empty | §14 완성형 Empty State 규칙을 따른다 |
| Error | "무엇이 실패했는지" 한 문장 + 재시도 또는 대체 행동 버튼을 항상 포함한다. 원인 없이 "오류가 발생했습니다"만 표시하지 않는다 |
| Unauthorized | 탭/기능이 없을 땐 렌더링 자체를 생략하고, 직접 접근 시에는 "권한이 없어요" 안내 + 로그인/홈 이동 CTA를 제공한다 |

## 14. Desktop·Mobile 규칙

- 기준 폭: **Desktop 1440px**, **Mobile 390px**.
- 카드 그리드는 Desktop 2~3열 → Mobile 1열로 **열 수만 줄이고 행을 재배열하지 않는다**(Airbnb 참고본의 "reduce columns, never reflow rows" 원칙을 계승).
- 터치 영역 최소 44×44px, 키보드 포커스 링은 `2px solid color.primary` + 2px 오프셋을 모든 인터랙티브 요소에 적용한다.
- 여행지/안전정보 상세는 Desktop=Drawer(우측), Mobile=Drawer(하단)로 형태만 바뀌고 콘텐츠 구조는 동일하게 유지한다.

## 15. Page Section 최대 폭과 상하 여백

- **Desktop 콘텐츠 최대 폭:** 1200~1280px(1440px 캔버스 중앙 정렬, 좌우 거터는 여백으로 흡수).
- **Section 상하 여백:** Desktop 64~96px, Mobile 40~64px 범위 안에서만 정한다. 이 범위를 벗어나는 과도한 여백(빈 공간)이나 지나치게 좁은 여백을 만들지 않는다.
- **Mobile Card 배치:** 모든 Card Grid를 1열로 배치하고 카드 사이 간격은 `spacing.base`(16px)를 기본으로 한다.

## 16. Hero 높이와 다음 Section 노출 규칙

- Hero는 Desktop 1440px 기준 화면 전체 높이를 차지하지 않는다. **화면 높이의 약 55~60%**로 제한해, 스크롤 없이도 다음 Section의 시작(제목 일부 또는 카드 상단)이 보이도록 한다.
- Mobile Hero도 동일 원칙을 따르되 검색창·CTA가 세로로 스택되어도 다음 Section이 뷰포트 하단에 살짝 보이는 높이를 유지한다.
- Hero 내부에는 헤드라인, 보조 설명 1문장, 핵심 액션(검색창 또는 CTA 버튼) 외의 장식성 빈 여백을 두지 않는다.

## 17. Section 계층과 시각적 리듬

모든 Section은 다음 계층을 순서대로 갖는다.

1. **제목**(`display-lg`, 24px/600) — 자연스러운 한국어 완성 문장 또는 명사구
2. **설명**(`body-md`, 1~3문장) — 이 Section이 왜 존재하는지, 무엇을 할 수 있는지
3. **본문**(Card Grid / 좌우 분할 / Chip 목록 / 3단계 안내 / CTA Banner / Form 중 하나)
4. **CTA 또는 다음 행동**(있는 경우) — 버튼 또는 링크

**리듬 규칙:** 같은 유형(Card Grid 등)이 연속 배치될 때는 배경 톤(`canvas` ↔ `surface-soft`)이나 배지·콘텐츠 성격을 달리해 반복감을 낮춘다. 한 화면 안에서 Hero, Card Grid, 좌우 분할, Chip 목록, 3단계 안내, CTA Banner 중 최소 3가지 이상의 유형을 교차 사용한다.

## 18. 화면별 Section 순서와 최소 콘텐츠 수 (승인 기준)

`docs/04_UIUX_PLAN.md` 및 `docs/STITCH_VALIDATION_REPORT.md`에서 PASS 판정된 구조를 그대로 고정한다.

| Screen | Section 수 | 순서 및 최소 콘텐츠 수 |
|---|---|---|
| **SCR-001** `/` | 7 | Hero(검색+CTA) → 국내 인기 여행지 **6장** → 해외 인기 여행지 **6장** → 여행 동기 Chip **6개** → 국가별 주의사항 **6장** → 최근 동행글 **3건**(또는 완성형 Empty) → free_traveler 소개(50+/30+ 지표 + CTA) |
| **SCR-002** `/about` | 7 | Hero → 여행 지표(50+/30+) → 소개·철학(2~4문단) → Timeline **6개 시점 이상** → 방문 국가 Chip **30개국**(권역별) → Gallery **8장 이상** → 기억에 남는 여행지 **4개** + CTA |
| **SCR-003** `/travel-tools` | 6 | Intro(3단계 안내) → 탭(항공/숙소/동행 구하기 **3개 모두**) → 조건 입력 Form(4필드) → 요약+외부이동 CTA → 비전달 고지+Tip **3개** → 동행 로그인 안내 또는 작성 Form+안전 안내 |
| **SCR-004** `/mates` | 6 | Intro+작성 CTA → Filter+결과 요약 → 목록(데이터 있으면 최대 **8건** 우선 노출) → 목록·상세 분할(Desktop) / Drawer(Mobile) → 신청 방법 **3단계** → 안전·신고·차단 안내+CTA |
| **SCR-005** `/account` | 역할별 가변 | Guest: Intro+로그인/가입/재설정 Card+로그인 후 기능 안내+보안 안내 · Member: 프로필+내 활동(내 글/참가요청/차단)+새 글 CTA · Admin: 관리 Intro+신고 상태 필터·변경(목록형)+외부 URL(HTTPS만) 설정 Form — **역할에 없는 영역은 렌더링하지 않는다** |
| **Mobile 변형** | SCR-001, SCR-003 | Desktop과 동일한 Section 순서·최소 수량을 1열로 재배치. 열 수만 줄이고 Section을 생략하지 않는다 |

## 19. 완성형 Empty State와 Placeholder 문구 금지 규칙

- **금지 문구:** `Lorem ipsum`, `준비 중`, `정보 확인 필요`, 내용 없는 빈 카드, 의미 없는 반복 문구.
- **완성형 Empty State 3요소:**
  1. 무엇이 없는지 한국어 완성 문장으로 설명
  2. 이용 방법 또는 이유 한 줄
  3. 다음 행동 CTA(예: "동행 글 작성하기", "필터 초기화")
  - 예시: *"아직 등록된 동행글이 없어요. 원하는 국가와 기간으로 첫 모집글을 작성해 보세요."* + "동행 글 작성하기" 버튼.
- **이미지 alt 텍스트:** 실제 장소·구도를 설명하는 문장만 사용한다("이미지", "사진1" 등 placeholder 금지).

## 20. Do / Do Not

### Do
- 코랄(`#F0603F`)은 Primary CTA·활성 탭·즐겨찾기에만 쓴다.
- 오류·경고·안전정보에는 §2의 semantic 색(danger/warning/safety-info)을 코랄과 분리해 쓴다.
- 모든 Section에 제목·설명·본문·CTA 4계층을 갖춘다.
- Hero는 화면의 55~60%로 제한해 다음 Section이 보이게 한다.
- 빈 데이터 상태에도 안내+이용 방법+CTA를 갖춘 완성형 Empty State를 그린다.
- Desktop→Mobile 전환 시 카드 그리드는 열 수만 줄인다.
- 새로운 의미가 필요하면 이 문서에 토큰을 먼저 등록한 뒤 사용한다.
- Inter + OS 기본 한글 폰트만 사용한다.

### Do Not
- Airbnb의 로고·워드마크·문구·Rausch 색상·Cereal 폰트를 복제하지 않는다.
- 구매·예약·결제(가격 표시, 결제 수단 선택, 발권/체크아웃) UI를 만들지 않는다.
- Proprietary 폰트 파일을 다운로드·번들하지 않는다.
- 이 문서의 Color Token 표에 없는 임의 색상을 추가하지 않는다.
- 실시간 항공권·호텔 가격, 별점, 광고 배너를 넣지 않는다.
- Lorem ipsum, "준비 중", "정보 확인 필요", 빈 카드, 과도한 빈 여백을 두지 않는다.
- 그림자를 2단계 이상 겹쳐 쓰지 않는다(§6 단일 티어 원칙).
- 역할에 없는 탭(Guest에게 관리자 탭 등)을 렌더링하지 않는다.
