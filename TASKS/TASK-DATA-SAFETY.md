# DATA-SAFETY — 국가 안전정보 정적 데이터

- Seq: 2
- Category: DATA
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 2, Category DATA)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "국가 안전정보 정적 데이터"을(를) 다룬다. 특정 Screen에 종속되지 않는 데이터/인프라/검증 계층 Task다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-046, REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-052, REQ-FUNC-053, REQ-NF-027, REQ-NF-028)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-046
- REQ-FUNC-047
- REQ-FUNC-048
- REQ-FUNC-052
- REQ-FUNC-053
- REQ-NF-027
- REQ-NF-028

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

- 해당 없음(비-UI Task) — 단, 이 Task의 산출물을 소비하는 CMP/PAGE Task는 위 Design Ref를 따른다.

## Depends On

- DATA-DESTINATIONS

## Expected Files

- 신규 생성: `src/data/country-safety.ts`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] 소개 해외국가 전원 커버리지, 8개 카테고리, `scope_type`/`scope_text`, 긴급연락처, `verified_at` 포함

## Visual AC

- [ ] 해당 없음

## Security/Privacy AC


## Test Cases

- TC-FUNC-046~048: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-NF-027: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-NF-028: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-046~048, TC-NF-027, TC-NF-028

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-046, REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-052, REQ-FUNC-053, REQ-NF-027, REQ-NF-028)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-046~048, TC-NF-027, TC-NF-028)가 통과한다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
