# PAGE-SCR001 — SCR-001 메인 페이지 조립

- Seq: 23
- Category: PAGE
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 23, Category PAGE)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "SCR-001 메인 페이지 조립"을(를) 다룬다. 대상 Screen은 메인(`/`)이며 Route는 `/`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-046, REQ-FUNC-057, REQ-FUNC-068, REQ-NF-026)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-001
- REQ-FUNC-004
- REQ-FUNC-006
- REQ-FUNC-046
- REQ-FUNC-057
- REQ-FUNC-068
- REQ-NF-026

## Screen / Route / Page Entry

- Screen: SCR-001
- Route: `/`
- Page Entry: `src/app/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 메인(`/`) 절
- `design-reference/D-001/DESIGN.md` §13 Loading·Empty·Error 상태, §19 완성형 Empty State·Placeholder 금지 규칙

## Depends On

- CMP-SCR001-HERO
- CMP-SCR001-DEST-DOMESTIC
- CMP-SCR001-DEST-OVERSEAS
- CMP-SCR001-DEST-DRAWER
- CMP-SCR001-THEME-CHIPS
- CMP-SCR001-SAFETY-GRID
- CMP-SCR001-SAFETY-DRAWER
- CMP-SCR001-RECENT-MATES
- CMP-SCR001-FOUNDER-SUMMARY
- CMP-SCR001-FAVORITES
- CMP-SHARED-HEADER-FOOTER
- DATA-DESTINATIONS
- DATA-SAFETY
- DATA-REPRESENTATIVE

## Expected Files

- 기존 파일 수정: `src/app/page.tsx`(현재 `create-next-app` 기본 템플릿 내용)
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] Section 순서: Hero(검색+`/travel-tools` CTA) → 국내 여행지 Card Grid 6 → 해외 여행지 Card Grid 6 → 여행 동기 Chip 6 → 국가별 주의사항 Card Grid 6 → 최근 동행글 Card 3 또는 완성형 Empty State → free_traveler 요약(50+/30+)+`/about` CTA
- [ ] 각 Section의 데이터 출처: 국내/해외 카드 = `DATA-DESTINATIONS`, 주의사항 카드 = `DATA-SAFETY`, 대표 요약 = `DATA-REPRESENTATIVE`, 최근 동행글 = `mate_post`(DB-ACCESS) 최신 3건
- [ ] 여행지 카드 클릭 시 같은 화면에서 상세 Drawer/Modal이 열린다(별도 페이지 이동 없음)
- [ ] 안전정보 카드 클릭 시 같은 화면에서 안전정보 Drawer/Modal이 열린다
- [ ] `create-next-app` 기본 Starter 마크업(Next.js 로고, "Get started by editing", 기본 문서/배포 링크)이 **완전히 제거**되었다

## Visual AC

- [ ] `create-next-app` 기본 히어로/로고/링크가 화면 어디에도 남아 있지 않다
- [ ] Hero 높이는 Desktop 1440px 기준 화면의 55~60%로 제한되어, 스크롤 없이 다음 Section(국내 여행지) 상단이 보인다(`D-001/DESIGN.md` §16)
- [ ] Desktop 콘텐츠 최대 폭 1200~1280px, Section 상하 여백 Desktop 64~96px / Mobile 40~64px(`D-001/DESIGN.md` §15)
- [ ] Card Grid는 Desktop 3열 → Mobile 1열로 열 수만 축소(행 재배열 금지), Mobile은 승인된 Stitch Screen ID `9f862d3f881f4bb7950e3e529b7d93f1`과 동일한 Section 순서·수량 유지
- [ ] 큰 빈 영역을 만들지 않는다. Lorem ipsum·"준비 중"·"정보 확인 필요" 문구를 어디에도 쓰지 않는다
- [ ] 최근 동행글이 0건이면: "아직 등록된 동행글이 없어요" 같은 안내 문장 + 이용 방법 한 줄 + "동행 글 작성하기"(비로그인 시 로그인 유도) CTA를 갖춘 완성형 Empty State를 표시하고, 내용 없는 빈 카드를 두지 않는다

## Security/Privacy AC

- [ ] 검색·필터 입력은 클라이언트 상태로만 처리하고 원문을 서버 로그에 남기지 않는다
- [ ] 안전정보 Drawer의 외교부 링크는 `target=_blank rel="noopener noreferrer"`를 사용한다

## Test Cases

- TC-FUNC-001: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-004: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-006: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-046: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-057: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-068: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-001, TC-FUNC-004, TC-FUNC-006, TC-FUNC-046, TC-FUNC-057, TC-FUNC-068 + `E2E-PUBLIC-SMOKE`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-046, REQ-FUNC-057, REQ-FUNC-068, REQ-NF-026)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-001, TC-FUNC-004, TC-FUNC-006, TC-FUNC-046, TC-FUNC-057, TC-FUNC-068)가 통과한다.
- [ ] Depends On의 모든 Component/Data/Auth/DB Task가 완료된 뒤 이 Screen에 실제로 조립되어 있다(신규 Component 생성 아님).
- [ ] `create-next-app` 기본 템플릿 흔적이 전혀 남아 있지 않다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
- `create-next-app` 기본 Starter 마크업을 일부라도 남겨두지 않는다.
