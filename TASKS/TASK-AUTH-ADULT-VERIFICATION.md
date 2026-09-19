# AUTH-ADULT-VERIFICATION — 성인 확인·쓰기 게이트

- Seq: 9
- Category: AUTH
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 9, Category AUTH)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "성인 확인·쓰기 게이트"을(를) 다룬다. 특정 Screen에 종속되지 않는 데이터/인프라/검증 계층 Task다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-027, REQ-FUNC-028)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-027
- REQ-FUNC-028

## Screen / Route / Page Entry

- Screen: N/A
- Route: N/A
- Page Entry: N/A

## Design Ref

- 해당 없음(비-UI Task) — 단, 이 Task의 산출물을 소비하는 CMP/PAGE Task는 위 Design Ref를 따른다.

## Depends On

- AUTH-SUPABASE-SETUP

## Expected Files

- 신규 생성: `src/lib/auth/adult-gate.ts`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] 미인증/미성년 사용자의 쓰기 요청을 401 또는 로그인 리다이렉트로 차단, 정확한 생년월일 미저장

## Visual AC

- [ ] 해당 없음

## Security/Privacy AC

- [ ] 서버 측에서 재검증(클라이언트 우회 방지)

## Test Cases

- TC-FUNC-027: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.
- TC-FUNC-028: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-027, TC-FUNC-028

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-027, REQ-FUNC-028)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-027, TC-FUNC-028)가 통과한다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- 정확한 생년월일을 저장하지 않는다(`is_adult`/`adult_verified_at`만 저장).
