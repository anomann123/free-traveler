# DB-ACCESS — 데이터 접근 계층

- Seq: 6
- Category: DB
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 6, Category DB)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "데이터 접근 계층"을(를) 다룬다. 특정 Screen에 종속되지 않는 데이터/인프라/검증 계층 Task다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-037, REQ-FUNC-038, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-077, REQ-NF-014, REQ-NF-015)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-030
- REQ-FUNC-031
- REQ-FUNC-032
- REQ-FUNC-033
- REQ-FUNC-034
- REQ-FUNC-035
- REQ-FUNC-036
- REQ-FUNC-037
- REQ-FUNC-038
- REQ-FUNC-039
- REQ-FUNC-040
- REQ-FUNC-041
- REQ-FUNC-077
- REQ-NF-014
- REQ-NF-015

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

- 해당 없음(비-UI Task) — 단, 이 Task의 산출물을 소비하는 CMP/PAGE Task는 위 Design Ref를 따른다.

## Depends On

- DB-SCHEMA-BASE
- DB-RLS-BASE

## Expected Files

- 신규 생성: `src/lib/db/mate.ts`, `src/lib/db/report.ts`, `src/lib/db/outbound-url.ts`, `src/lib/db/block.ts`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] Server Action/Route Handler로 CRUD 제공, 입력 검증·이스케이프 적용
- [ ] `src/lib/db/block.ts`는 `user_block` 생성(차단)·삭제(해제)·목록 조회 함수를 제공하고, 동행 목록/상세 조회 함수(`mate.ts`)가 이를 참조해 차단 관계에 있는 상대의 글을 결과에서 제외한다(REQ-FUNC-040)

## Visual AC

- [ ] 해당 없음

## Security/Privacy AC

- [ ] CSRF 방어(Server Actions 기본), 저장 XSS 차단

## Test Cases

- TC-NF-014: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-NF-015: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-NF-014, TC-NF-015

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-037, REQ-FUNC-038, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-077, REQ-NF-014, REQ-NF-015)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-NF-014, TC-NF-015)가 통과한다.
- [ ] 스키마에 정의된 테이블이 정확히 6개(또는 그 하위 마이그레이션 단계)이며 그 외 테이블이 없다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- 정의된 6개 테이블(`user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_url_setting`) 외 신규 테이블을 만들지 않는다.
- 여행지·안전정보·대표 소개를 DB 테이블로 만들지 않는다(정적 데이터로만 관리).
