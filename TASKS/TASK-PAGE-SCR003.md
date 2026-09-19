# PAGE-SCR003 — SCR-003 통합 여행 준비 페이지 조립

- Seq: 40
- Category: PAGE
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 40, Category PAGE)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "SCR-003 통합 여행 준비 페이지 조립"을(를) 다룬다. 대상 Screen은 통합 여행 준비(`/travel-tools`)이며 Route는 `/travel-tools`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-054, REQ-FUNC-080, REQ-NF-017)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-011
- REQ-FUNC-012
- REQ-FUNC-013
- REQ-FUNC-014
- REQ-FUNC-015
- REQ-FUNC-016
- REQ-FUNC-017
- REQ-FUNC-018
- REQ-FUNC-019
- REQ-FUNC-020
- REQ-FUNC-021
- REQ-FUNC-022
- REQ-FUNC-023
- REQ-FUNC-024
- REQ-FUNC-025
- REQ-FUNC-026
- REQ-FUNC-031
- REQ-FUNC-032
- REQ-FUNC-054
- REQ-FUNC-080
- REQ-NF-017

## Screen / Route / Page Entry

- Screen: SCR-003
- Route: `/travel-tools`
- Page Entry: `src/app/travel-tools/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 통합 여행 준비(`/travel-tools`) 절
- `design-reference/D-001/DESIGN.md` §13 Loading·Empty·Error 상태, §19 완성형 Empty State·Placeholder 금지 규칙

## Depends On

- CMP-SCR003-INTRO
- CMP-SCR003-TABS
- CMP-SCR003-FLIGHT-FORM
- CMP-SCR003-HOTEL-FORM
- CMP-SCR003-TIPS
- CMP-SCR003-MATE-WRITE
- CMP-SCR003-MATE-LOGIN-PROMPT
- CMP-SHARED-HEADER-FOOTER
- CMP-SHARED-TOAST
- AUTH-ADULT-VERIFICATION

## Expected Files

- 신규 생성: `src/app/travel-tools/page.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] Section 순서: Intro(3단계 안내) → Tab(항공편/숙소/동행 구하기) → 조건 입력 Form → 요약+외부 이동 Action Card → 비전달 고지+Tip 3개 → 동행 로그인 안내 또는 작성 Form+안전 안내
- [ ] **항공편/숙소/동행 구하기 3개 탭이 모두 실제 콘텐츠로 조립된다.** 자리표시자로 남겨진 탭이 없다
- [ ] 3개 탭의 입력·검증·완료 상태는 서로 완전히 독립적으로 유지된다(한 탭의 값이 다른 탭에 영향을 주지 않는다)
- [ ] 항공·숙소 조건 입력값은 브라우저 상태로만 유지하며 서버 DB·서버 로그·분석 이벤트에 저장하지 않는다
- [ ] 외부 이동은 설정된 URL을 새 탭(`noopener,noreferrer`)으로 열고 목적지·날짜 쿼리를 붙이지 않는다
- [ ] 동행 작성 Form 제출 시 연락처 패턴이 감지되면 제출을 차단하고 수정 안내를 표시한다

## Visual AC

- [ ] Hero/Intro가 화면 전체를 채우지 않고 다음 Section(탭)이 바로 이어진다
- [ ] Desktop 폼 2열 그리드 → Mobile 1열, Mobile 승인 Screen ID `3e4e85ab173c49debea20fb05e92a92f` 기준 3탭 가로 균등 배치(가로 스크롤 금지) 유지
- [ ] 큰 빈 영역·Lorem ipsum·"준비 중"·"정보 확인 필요" 금지
- [ ] 비로그인 상태의 동행 탭은 빈 화면이 아니라 "로그인하고 동행을 구해보세요" 완성형 안내 카드(이용 방법+로그인 CTA 포함)를 표시한다

## Security/Privacy AC

- [ ] REQ-NF-017: 항공·호텔 원시 입력값이 네트워크 요청·서버 로그·DB 어디에도 나타나지 않는다(빌드 후 네트워크 탭 확인)
- [ ] 동행 작성 폼은 REQ-FUNC-032 연락처 탐지를 통과해야 저장된다

## Test Cases

- TC-FUNC-011~026: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-031: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-032: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-054: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-080: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-NF-017: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-011~026, TC-FUNC-031, TC-FUNC-032, TC-FUNC-054, TC-FUNC-080, TC-NF-017 + `E2E-TRAVEL-TOOLS`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-054, REQ-FUNC-080, REQ-NF-017)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-011~026, TC-FUNC-031, TC-FUNC-032, TC-FUNC-054, TC-FUNC-080, TC-NF-017)가 통과한다.
- [ ] Depends On의 모든 Component/Data/Auth/DB Task가 완료된 뒤 이 Screen에 실제로 조립되어 있다(신규 Component 생성 아님).
- [ ] 항공/숙소/동행 구하기 3탭이 전부 실제 콘텐츠로 조립되어 있다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
- 항공/숙소/동행 구하기 탭 중 어느 하나라도 자리표시자로 남기지 않는다.
- 항공·숙소 입력값을 서버 DB·로그·외부 URL 쿼리로 전송하지 않는다.
- 입력값에 목적지·날짜 쿼리 파라미터를 붙여 외부 URL로 전달하지 않는다.
