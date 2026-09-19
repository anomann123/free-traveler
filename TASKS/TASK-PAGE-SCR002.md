# PAGE-SCR002 — SCR-002 대표 소개 페이지 조립

- Seq: 32
- Category: PAGE
- Implementation Status: IMPLEMENT
- Priority: P1

## Context

`TASKS/00_TASK_LIST.md`(Seq 32, Category PAGE)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "SCR-002 대표 소개 페이지 조립"을(를) 다룬다. 대상 Screen은 대표 소개(`/about`)이며 Route는 `/about`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-061, REQ-FUNC-062, REQ-FUNC-063)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-057
- REQ-FUNC-058
- REQ-FUNC-059
- REQ-FUNC-060
- REQ-FUNC-061
- REQ-FUNC-062
- REQ-FUNC-063

## Screen / Route / Page Entry

- Screen: SCR-002
- Route: `/about`
- Page Entry: `src/app/about/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 대표 소개(`/about`) 절
- `design-reference/D-001/DESIGN.md` §13 Loading·Empty·Error 상태, §19 완성형 Empty State·Placeholder 금지 규칙

## Depends On

- CMP-SCR002-HERO
- CMP-SCR002-STATS
- CMP-SCR002-INTRO
- CMP-SCR002-COUNTRIES
- CMP-SCR002-TIMELINE
- CMP-SCR002-GALLERY
- CMP-SCR002-CONTACT-LINKS
- CMP-SCR002-TOP-PICKS
- CMP-SHARED-HEADER-FOOTER
- DATA-REPRESENTATIVE
- DATA-DESTINATIONS

## Expected Files

- 신규 생성: `src/app/about/page.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] Section 순서: Profile Hero → 여행 지표(50+ Trips/30+ Countries) → 소개·철학(2~4문단) → 여행 Timeline(6개 시점 이상) → 방문 국가 Chip(권역별, 30개국) → Gallery(사진 8장 이상) → 기억에 남는 여행지 4개+CTA
- [ ] Section별 데이터 출처: Hero/지표/소개/Timeline/국가/Gallery/문의링크 = `DATA-REPRESENTATIVE`, 추천 여행지 4개 = `DATA-DESTINATIONS`(대표 프로필의 추천 slug 참조)
- [ ] 추천 여행지 카드 클릭 시 SCR-001의 해당 여행지 상세 Drawer로 이동한다

## Visual AC

- [ ] Timeline 6개 이상, 방문 국가 정확히 30개(권역별 그룹), Gallery 8장 이상, 추천 여행지 정확히 4개 — 최소 수량 미달 시 게시하지 않는다(`D-001/DESIGN.md` §18)
- [ ] Hero 높이 Desktop 기준 화면의 약 55%로 제한해 다음 Section 시작이 보인다
- [ ] Desktop 콘텐츠 최대 폭 1200~1280px, Section 여백 Desktop 64~96px/Mobile 40~64px
- [ ] 큰 빈 영역·Lorem ipsum·"준비 중"·"정보 확인 필요" 금지
- [ ] 전량 정적 콘텐츠라 데이터 없음 상태는 발생하지 않지만, Gallery 개별 이미지 로드 실패 시에는 플레이스홀더 아이콘+"이미지를 불러오지 못했습니다" 완성형 대체 문구를 표시한다

## Security/Privacy AC

- [ ] 대표 인물 사진이 특정 서비스의 보증·인증으로 오인되지 않도록 문구를 제한한다(PROJECT_SCOPE EX-MEDIA 원칙 계승, 라이선스 승인 워크플로 자체는 EXCLUDED)

## Test Cases

- TC-FUNC-057~063: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-057~063 + 수동 QA(정적 콘텐츠 완전성 체크리스트)

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-061, REQ-FUNC-062, REQ-FUNC-063)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-057~063)가 통과한다.
- [ ] Depends On의 모든 Component/Data/Auth/DB Task가 완료된 뒤 이 Screen에 실제로 조립되어 있다(신규 Component 생성 아님).
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
