# PAGE-SCR004 — SCR-004 동행 조회 페이지 조립

- Seq: 48
- Category: PAGE
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 48, Category PAGE)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "SCR-004 동행 조회 페이지 조립"을(를) 다룬다. 대상 Screen은 동행 조회(`/mates`)이며 Route는 `/mates`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-030, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-037, REQ-FUNC-039, REQ-FUNC-040)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-030
- REQ-FUNC-033
- REQ-FUNC-034
- REQ-FUNC-035
- REQ-FUNC-037
- REQ-FUNC-039
- REQ-FUNC-040

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: `/mates`
- Page Entry: `src/app/mates/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 동행 조회(`/mates`) 절
- `design-reference/D-001/DESIGN.md` §13 Loading·Empty·Error 상태, §19 완성형 Empty State·Placeholder 금지 규칙

## Depends On

- CMP-SCR004-INTRO
- CMP-SCR004-FILTER
- CMP-SCR004-LIST
- CMP-SCR004-DETAIL
- CMP-SCR004-APPLICATION
- CMP-SCR004-REPORT
- CMP-SCR004-SAFETY-NOTICE
- CMP-SHARED-HEADER-FOOTER
- CMP-SHARED-TOAST
- DB-ACCESS

## Expected Files

- 신규 생성: `src/app/mates/page.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] Section 순서: Intro+작성 CTA → Filter(국가·지역·기간·모집 상태)+결과 요약 → 동행글 Card 목록(데이터가 있으면 최대 8건 우선 노출) → 목록·상세 분할(Desktop) 또는 상세 Drawer(Mobile) → 신청 방법 3단계 안내 → 안전·신고·차단 안내+`/travel-tools` CTA
- [ ] 목록 데이터 출처: `mate_post`(DB-ACCESS), 종료일이 지난 글은 조회 시점에 CLOSED로 계산해 표시(배치 없음)
- [ ] 참가 메시지 제출은 500자 이내, 중복 PENDING/ACCEPTED 요청을 차단한다
- [ ] 신고 제출 시 사유 코드+설명을 받고 접수 ID를 3초 이내 표시한다
- [ ] 상세 패널에서 "차단하기"를 실행하면 즉시 목록·필터·상세 어디에서도 해당 작성자의 글이 노출되지 않는다(REQ-FUNC-040, `CMP-SCR004-DETAIL`)

## Visual AC

- [ ] Desktop은 목록(좌 40%)+상세(우 60%) 화면 내 분할, Mobile은 카드 탭 시 하단 Drawer로 상세를 연다(페이지 이동 없음)
- [ ] Desktop 콘텐츠 최대 폭 1200~1280px, Section 여백 Desktop 64~96px/Mobile 40~64px
- [ ] 조건에 맞는 글이 없으면: "조건에 맞는 동행글이 아직 없어요" 안내 문장 + 필터 초기화 버튼 + "새 동행글 작성" CTA + 이용 방법 한 줄을 갖춘 완성형 Empty State를 표시하고, 내용 없는 빈 카드를 두지 않는다
- [ ] Lorem ipsum·"준비 중"·"정보 확인 필요" 금지

## Security/Privacy AC

- [ ] 모집글·상세 어디에도 이메일·전화번호 등 공개 연락처를 노출하지 않는다(REQ-FUNC-033)
- [ ] 비공개 데이터(참가 메시지, 신고 상세)는 RLS로 작성자·요청자·Admin만 조회 가능하다(`DB-RLS-BASE`에 의존)

## Test Cases

- TC-FUNC-030: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-033~035: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-037: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-039: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-040: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-030, TC-FUNC-033~035, TC-FUNC-037, TC-FUNC-039, TC-FUNC-040 + `E2E-MATE-AUTH`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-030, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-037, REQ-FUNC-039, REQ-FUNC-040)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-030, TC-FUNC-033~035, TC-FUNC-037, TC-FUNC-039, TC-FUNC-040)가 통과한다.
- [ ] Depends On의 모든 Component/Data/Auth/DB Task가 완료된 뒤 이 Screen에 실제로 조립되어 있다(신규 Component 생성 아님).
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
