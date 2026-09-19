# CMP-SCR004-DETAIL — 목록·상세 분할 패널

- Seq: 44
- Category: CMP
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 44, Category CMP)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "목록·상세 분할 패널"을(를) 다룬다. 대상 Screen은 동행 조회(`/mates`)이며 Route는 `/mates`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-033(연계), REQ-FUNC-040)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-033
- REQ-FUNC-040

## Screen / Route / Page Entry

- Screen: SCR-004
- Route: `/mates`
- Page Entry: `src/app/mates/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 동행 조회(`/mates`) 절

## Depends On

- CMP-SCR004-LIST
- DB-ACCESS

## Expected Files

- 신규 생성: `src/app/_components/scr004/detail-panel.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] 제목·작성자 정보(연락처 없음)·조건·설명 표시
- [ ] 작성자 정보 영역에 "차단하기" 텍스트 액션을 제공한다. 선택 시 확인 다이얼로그 후 해당 작성자를 차단하고, 이후 동행 목록·상세·필터 어디에서도 서로의 글·프로필·요청이 노출되지 않는다(REQ-FUNC-040, `DB-ACCESS`의 차단 접근 함수 사용)
- [ ] 이미 차단한 작성자의 글은 목록·상세 진입 이전에 필터링되어 상세 패널 자체가 열리지 않는다

## Visual AC

- [ ] Desktop 좌40/우60 분할, Mobile 하단 Drawer
- [ ] "차단하기" 액션은 "신고"와 시각적으로 구분된 위치(작성자 정보 하단)에 텍스트 버튼으로 배치하고, 실행 즉시 `toast-success`가 아닌 완료 안내(차단됨) 문구를 표시한다

## Security/Privacy AC

- [ ] 비공개 필드는 RLS로만 노출
- [ ] 차단 관계는 본인만 생성·조회·해제할 수 있다(`user_block`, `DB-RLS-BASE`)

## Test Cases

- TC-FUNC-033: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-040: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-033, TC-FUNC-040

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-033, REQ-FUNC-040)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-033, TC-FUNC-040)가 통과한다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
