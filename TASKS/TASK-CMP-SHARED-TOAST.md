# CMP-SHARED-TOAST — 전역 Toast 컴포넌트

- Seq: 11
- Category: CMP
- Implementation Status: IMPLEMENT(대체)
- Priority: P1

## Context

`TASKS/00_TASK_LIST.md`(Seq 11, Category CMP)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "전역 Toast 컴포넌트"을(를) 다룬다. 5개 Screen 전체에서 공용으로 재사용되는 요소를 다룬다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT(대체)**다. `PROJECT_SCOPE.md`에 따라 원래 채널(이메일 등) 대신 대체 구현(Toast/화면 상태 등)으로 충족한다. 이 Task에 결부된 Requirement(REQ-FUNC-043)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-043

## Screen / Route / Page Entry

- Screen: 전역
- Route: 공통(전 Route)
- Page Entry: `src/app/layout.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 공통 절
- `design-reference/D-001/DESIGN.md` §12 Alert·Toast

## Depends On

- 없음

## Expected Files

- 신규 생성: `src/app/_components/shared/toast.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] 참가 요청 접수·승인·거절·신고 처리 결과를 이메일 대신 Toast로 1분 이내 표시

## Visual AC

- [ ] `toast-success`/배너 톤 준수, 코랄과 구분된 semantic 색 사용

## Security/Privacy AC

- [ ] 이메일 발송 실패로 상태 변경이 롤백되지 않음

## Test Cases

- TC-FUNC-043: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-043

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-043)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-043)가 통과한다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
