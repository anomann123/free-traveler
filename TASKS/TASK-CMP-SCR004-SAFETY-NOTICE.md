# CMP-SCR004-SAFETY-NOTICE — 신청 방법+안전 안내

- Seq: 47
- Category: CMP
- Implementation Status: IMPLEMENT
- Priority: P1

## Context

`TASKS/00_TASK_LIST.md`(Seq 47, Category CMP)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "신청 방법+안전 안내"을(를) 다룬다. 대상 Screen은 동행 조회(`/mates`)이며 Route는 `/mates`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(구조적(안전 고지))는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- 구조적(안전 고지)

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: `/mates`
- Page Entry: `src/app/mates/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 동행 조회(`/mates`) 절
- `design-reference/D-001/DESIGN.md` §12 Alert·Toast

## Depends On

- CMP-SCR004-REPORT

## Expected Files

- 신규 생성: `src/app/_components/scr004/safety-notice.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] "모집글 확인→참가 메시지 전송→작성자 승인 대기" 3단계+연락처 공유 금지·신고/차단 방법 요약+`/travel-tools` CTA

## Visual AC

- [ ] 3단계 안내+경고 톤 Banner

## Security/Privacy AC


## Test Cases

- 수동 QA: Functional AC/Visual AC 항목을 체크리스트로 순회하며 확인한다.

## Verify

- 수동 QA

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(구조적(안전 고지))가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
