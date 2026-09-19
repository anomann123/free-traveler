# DB-SCHEMA-BASE — 핵심 테이블 스키마

- Seq: 4
- Category: DB
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 4, Category DB)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "핵심 테이블 스키마"을(를) 다룬다. 특정 Screen에 종속되지 않는 데이터/인프라/검증 계층 Task다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-028, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-077)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-028
- REQ-FUNC-031
- REQ-FUNC-034
- REQ-FUNC-039
- REQ-FUNC-040
- REQ-FUNC-077

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

- 해당 없음(비-UI Task) — 단, 이 Task의 산출물을 소비하는 CMP/PAGE Task는 위 Design Ref를 따른다.

## Depends On

- 없음

## Expected Files

- 신규 생성: `supabase/migrations/0001_schema_base.sql`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] 정확히 6개 테이블만 생성: `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_url_setting`(§3 상한 준수)

## Visual AC

- [ ] 해당 없음

## Security/Privacy AC

- [ ] PK/FK/CHECK 제약으로 무결성 확보(예: `mate_application` 유니크 제약)

## Test Cases

- 수동 QA: Functional AC/Visual AC 항목을 체크리스트로 순회하며 확인한다.

## Verify

- 수동 스키마 리뷰

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-028, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-077)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] 스키마에 정의된 테이블이 정확히 6개(또는 그 하위 마이그레이션 단계)이며 그 외 테이블이 없다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- 정의된 6개 테이블(`user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_url_setting`) 외 신규 테이블을 만들지 않는다.
- 여행지·안전정보·대표 소개를 DB 테이블로 만들지 않는다(정적 데이터로만 관리).
