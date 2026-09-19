---
description: Traveler 5개 Screen과 114개 Requirement로부터 TASKS/00_TASK_LIST.md를 생성·갱신한다
---

`traveler-project-pipeline` Skill을 로드한 뒤 그 규칙에 따라 `TASKS/00_TASK_LIST.md`를 생성하거나 갱신한다. **이 명령은 구현 코드를 만들지 않는다** — `TASKS/00_TASK_LIST.md` 한 파일만 쓰거나 갱신한다.

## 실행 순서

1. `python scripts/validate_inputs.py`를 실행한다. 실패(0이 아닌 종료 코드)하면 위반 내용을 그대로 보고하고 **여기서 중단**한다. 임의로 통과 처리하지 않는다.
2. 다음 입력을 **실제로 Read 도구로 열어서** 다시 확인한다(요약이나 이전 대화 기억만으로 진행하지 않는다): `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `package.json`.
3. `src/app`(및 이미 존재한다면 `src/data`, `src/lib`, `supabase`, `tests`, `.github`) 디렉터리를 Glob/Read로 실제 확인해 현재 파일 트리를 파악한다(Skill §5).
4. `design-reference/SCREEN_ROUTE_CONTRACT.json`을 정본으로 삼아 SCR-001~005 각각에 Page Owner Task(`PAGE-SCR001`~`PAGE-SCR005`)를 정확히 하나씩 만든다.
5. 각 Screen의 `design-reference/UI_CONTRACT.md` 영역 순서를 근거로 Component Task(`CMP-<SCREEN>-<이름>`, 공용은 `CMP-SHARED-*`)를 나눈다. Section을 생략하는 분해는 금지한다.
6. 여행지·안전정보·대표 소개 콘텐츠는 `DATA-DESTINATIONS`/`DATA-SAFETY`/`DATA-REPRESENTATIVE` 3개 Task로 만든다(Skill §1-11).
7. Skill §3의 6개 테이블 범위 내에서 `DB-SCHEMA-BASE`/`DB-RLS-BASE`/`DB-ACCESS`/`DB-SEED-BASE` 4개 Task를 만든다. 6개를 초과하는 테이블을 요구하는 Task를 만들지 않는다.
8. Supabase Auth 연동·성인 확인 게이트는 `AUTH-` Task로 만든다.
9. 단위 테스트는 `UNIT-` Task(날짜 검증, 연락처 탐지, 모집글/신청 상태 전이 등)로, RLS 등 Playwright가 아닌 통합 테스트는 `TEST-` Task로 만든다.
10. `E2E-` Task는 Playwright Chromium Smoke만 1~3개로 만든다(핵심 5~7개 흐름을 2~3개로 묶는다).
11. `CI-` Task 1개(Lint/Build/Test 파이프라인)와 `DEPLOY-` Task(Vercel·Supabase 배포 확인)를 만든다.
12. `docs/UIUX_TRACEABILITY.md`(및 `docs/PROJECT_SCOPE.md`와 모순되지 않는지)의 114개 Requirement를 전부 순회하며, IMPLEMENT 계열은 반드시 하나 이상의 Task에 연결하고, EXCLUDED는 문서 하단 "## 8. NON_IMPLEMENTATION Register"에 `Requirement | 근거(Source) | 후속 방향` 형식으로 기록한다(Skill §4). Requirement ID는 범위 축약("~") 없이 하나씩 전부 나열한다.
13. `TASKS/00_TASK_LIST.md`를 Skill §4 형식(Page Owner는 세로형 표, 나머지는 Task ID를 헤더에 포함한 가로형 표)으로 작성하고, 상단에 총 Task 수와 Type별 개수 요약을 넣는다.
14. 자동 Merge Runner, EC2, AWS와 관련된 Task를 만들지 않았는지, 항공·숙소 입력값을 서버/DB/URL/로그로 보내는 Task가 없는지 스스로 다시 확인한다.

## 완료 조건

- Task List에 정확히 5개의 `PAGE-` Task가 존재하고 SCR-001~005와 1:1 대응한다.
- Route/Page Entry가 `SCREEN_ROUTE_CONTRACT.json`과 정확히 일치한다.
- 114개 Requirement 전부가 Task 또는 NON_IMPLEMENTATION Register 어느 한쪽에 정확히 등장한다(누락·중복 없음, 축약 표기 없음).
- Task 총 개수는 45~65개가 자연스러운 범위이지만 이 숫자 자체를 pass/fail 기준으로 쓰지 않는다.
- 이 단계에서는 `TASKS/TASK-*.md` 상세 파일을 만들지 않는다(그것은 `/gen-task-details`의 책임) — **어떤 구현 코드도 만들지 않는다.**

작업이 끝나면 생성/갱신된 Task 수, Type별 개수, NON_IMPLEMENTATION Register 건수를 요약해 보고한다.
