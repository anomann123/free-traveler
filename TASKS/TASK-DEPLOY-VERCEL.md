# DEPLOY-VERCEL — Vercel 배포 설정 확인

- Seq: 63
- Category: DEPLOY
- Implementation Status: IMPLEMENT
- Priority: P1

## Context

`TASKS/00_TASK_LIST.md`(Seq 63, Category DEPLOY)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "Vercel 배포 설정 확인"을(를) 다룬다. 특정 Screen에 종속되지 않는 데이터/인프라/검증 계층 Task다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-NF-016, REQ-NF-034)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-NF-016
- REQ-NF-034

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

- 해당 없음(비-UI Task) — 단, 이 Task의 산출물을 소비하는 CMP/PAGE Task는 위 Design Ref를 따른다.

## Depends On

- CI-LINT-BUILD

## Expected Files

- 신규 생성: `docs/ops/vercel-checklist.md`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] Vercel 프로젝트 환경변수(Supabase 키, 외부 URL 등) 등록 확인, 무료/최소 티어로 월 비용 100,000원 이하 목표 확인. **EC2·AWS 인프라를 만들지 않는다**

## Visual AC

- [ ] 해당 없음

## Security/Privacy AC

- [ ] 해당 없음

## Test Cases

- TC-NF-016: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-NF-034: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-NF-016, TC-NF-034

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-NF-016, REQ-NF-034)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-NF-016, TC-NF-034)가 통과한다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- 자동 Merge Runner, EC2, AWS 인프라를 추가하지 않는다.
