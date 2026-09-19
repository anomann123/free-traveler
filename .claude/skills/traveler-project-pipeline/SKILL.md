---
name: traveler-project-pipeline
description: Free Traveler 프로젝트의 Task 생성 파이프라인. 승인된 5개 Screen(SCREEN_ROUTE_CONTRACT.json)과 SRS/PROJECT_SCOPE의 114개 Requirement를 입력으로 TASKS/00_TASK_LIST.md와 Task 상세 파일을 생성·검증한다. "/gen-tasklist", "/gen-task-details", "/audit-tasks" 명령이 이 Skill을 사용한다. Traveler 저장소에서 Task를 새로 만들거나 감사할 때 로드한다. 이 Skill은 계획 문서만 만들며 구현 코드를 생성하지 않는다.
---

# Traveler Project Task Pipeline

이 Skill은 Free Traveler 저장소에서 **Task를 생성·검증하는 유일한 절차**를 정의한다. 여기 적힌 규칙과 다른 방식으로 Task List나 Task 상세를 만들지 않는다. 이 Skill이 다루는 세 명령(`/gen-tasklist`, `/gen-task-details`, `/audit-tasks`) 중 어느 것도 **구현 코드(소스 파일, 마이그레이션 SQL 등)를 작성하지 않는다** — 오직 계획 문서(`TASKS/*.md`)와 감사 산출물(`TASKS/TASK_MANIFEST.csv`, `TASKS/TASK_AUDIT_REPORT.md`)만 만든다.

## 0. 파이프라인 개요

```
scripts/validate_inputs.py   (입력 문서·계약 검증)
        ↓
/gen-tasklist                 (TASKS/00_TASK_LIST.md 생성/갱신)
        ↓
/gen-task-details              (TASKS/TASK-<TASK-ID>.md 생성/갱신, 1:1)
        ↓
scripts/audit_tasks.py        (= /audit-tasks, 18개 항목 검증 + 산출물 생성)
```

- 입력 문서(모두 **실제로 읽는다** — 요약이나 기억에 의존하지 않는다): `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `package.json`, 실제 `src/app` 파일 트리.
- 출력 위치(고정 경로, 임의 변경 금지):
  - Task List: `TASKS/00_TASK_LIST.md`
  - Task 상세: `TASKS/TASK-<TASK-ID>.md` (Task List의 행 하나당 파일 하나, 예: Task ID `PAGE-SCR001` → `TASKS/TASK-PAGE-SCR001.md`)
  - 감사 산출물: `TASKS/TASK_MANIFEST.csv`, `TASKS/TASK_AUDIT_REPORT.md`

## 1. 핵심 규칙 (전부 강제)

1. **HARNESS_SCHEMA는 `traveler-screen-route-v1`이다.** `SCREEN_ROUTE_CONTRACT.json`의 `schema_version`이 이 값과 다르면 파이프라인을 중단한다.
2. **Screen 목록의 정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`이다.** `docs/04_UIUX_PLAN.md`나 다른 문서의 Screen 서술이 다르면 JSON을 우선한다.
3. **정확히 5개 Screen(SCR-001~005) 각각에 Page Owner Task(`PAGE-SCR001`~`PAGE-SCR005`)를 하나씩 만든다.** 6개 이상 또는 4개 이하를 만들지 않는다.
4. **Expected Files를 쓰기 전 실제 `src/app`(및 관련) 파일 트리를 확인한다.** 이미 존재하는 파일은 "생성"이 아니라 "수정/확장"으로 기술하고, 존재하지 않는 파일만 "신규 생성"으로 기술한다.
5. **Page Owner Task와 Component Task를 구분한다.** Page Owner는 해당 Screen의 Page Entry(`page.tsx`)에서 **이미 만들어진 Component를 실제로 조립하는 것만** 책임지며, Page Owner Task 안에서 새 Component를 만들지 않는다. Component Task는 그 안에 들어가는 개별 Section/컴포넌트(Hero, Card Grid, Filter, Form, Drawer 등)를 만든다.
6. **Page Owner는 같은 Screen의 모든 Component Task에 의존(Depends On)한다.** Page Owner Task는 자신의 Component Task가 전부 완료된 뒤에만 착수 가능하도록 의존 관계를 명시한다.
7. **`PAGE-SCR001`(SCR-001, `/`) Owner는 Next.js Starter 제거를 Acceptance Criteria로 갖는다.** `create-next-app` 기본 히어로/로고/링크 마크업이 완전히 제거되고 SCR-001 계약으로 대체되었는지 확인하는 AC를 반드시 포함한다.
8. **`PAGE-SCR003`(SCR-003, `/travel-tools`) Owner는 항공·숙소·동행 구하기 3개 탭을 실제로 조립한다.** 탭 중 하나만 만들고 나머지를 자리표시자로 남기지 않는다.
9. **`PAGE-SCR005`(SCR-005, `/account`) Owner는 Guest·Member·Admin 3개 역할 상태를 실제로 조립한다.** 역할별 조건부 렌더링(없는 탭은 DOM 미노출)을 AC로 명시한다.
10. **DB는 정확히 6개 테이블(§3)로 제한한다.** 그 표에 없는 테이블을 추가하는 Task를 만들지 않는다. `DB-SCHEMA-BASE`(스키마), `DB-RLS-BASE`(RLS 정책), `DB-ACCESS`(접근 계층), `DB-SEED-BASE`(시드 데이터) 4종 Task를 모두 만든다.
11. **여행지·안전정보·대표 소개 콘텐츠는 DB Task가 아니라 정적 데이터(`src/data`) Task(`DATA-DESTINATIONS`, `DATA-SAFETY`, `DATA-REPRESENTATIVE`)로 만든다.** Editor/Admin CRUD Task를 만들지 않는다(`PROJECT_SCOPE.md` EX-CMS).
12. **항공·숙소 입력값을 서버·DB·URL·로그·분석으로 전송하는 Task를 만들지 않는다.** 관련 Task의 AC에 "Client Component의 일시 상태로만 유지, 서버 미저장" 조건을 명시한다.
13. **Playwright Task(`E2E-` 접두어)는 Chromium Smoke Test만 1~3개로 만든다.** Firefox/WebKit 프로젝트, 시각적 회귀, 성능 테스트 Task를 만들지 않는다. RLS 등 Playwright가 아닌 통합 테스트는 `TEST-` 접두어를 쓰고 Chromium 제약을 적용하지 않는다.
14. **자동 Merge Runner, EC2, AWS 관련 Task를 만들지 않는다.** `PROJECT_SCOPE.md`의 EX-OPS 범위를 그대로 따른다. PR·Merge 승인은 항상 사람이 수행한다.
15. **REQ-FUNC-001~080(80개)과 REQ-NF-001~034(34개), 총 114개 Requirement 전부에 IMPLEMENT 또는 EXCLUDED 상태를 기록한다.** 어느 하나도 누락하지 않는다. `docs/UIUX_TRACEABILITY.md`가 1차 근거이며, `docs/PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 판정과 모순되지 않아야 한다(감사 시 `PROJECT_SCOPE.md`를 기준으로 교차검증한다).
16. **EXCLUDED Requirement는 상세 구현 Task를 만들지 않되, `TASKS/00_TASK_LIST.md`의 "## 8. NON_IMPLEMENTATION Register" 섹션에서 삭제하지 않고 그대로 유지한다(Requirement | 근거(Source) | 후속 방향 형식).** 어떤 Task의 Requirement Ref도 EXCLUDED 항목만으로 구성되어서는 안 된다.
17. **Task List와 상세 파일은 1:1이어야 한다.** Task List에 있는 모든 구현 Task ID는 `TASKS/TASK-<ID>.md` 상세 파일이 정확히 하나 있어야 하고, Task List에 없는 상세 파일(고아 파일)이 있어서는 안 된다.
18. **`/gen-task-details` 실행 후 반드시 `python scripts/audit_tasks.py`를 실행하고 `AUDIT_PASS`를 확인한다.** 감사를 통과하지 못하면(`AUDIT_FAIL`) 완료로 보고하지 않는다 — 실패를 무시하거나 임의로 통과 처리하지 않는다.
19. **Page Owner Acceptance Criteria에는 해당 Screen의 Section 순서와 최소 콘텐츠 수(카드/타임라인/갤러리 등)를 `design-reference/UI_CONTRACT.md`·`design-reference/D-001/DESIGN.md` §18 기준으로 그대로 옮겨 적는다.**
20. **Page Owner AC는 큰 빈 영역과 Placeholder 문구(Lorem ipsum, 준비 중, 정보 확인 필요)를 금지하고, 데이터가 없을 때도 안내 문장·이용 방법·CTA를 갖춘 완성형 Empty State를 요구한다.**

## 2. Task 분류 체계

| Type | 접두어 | 개수 규칙 | 의존 관계 |
|---|---|---|---|
| Page Owner | `PAGE-` | 정확히 5개(`PAGE-SCR001`~`PAGE-SCR005`) | 같은 Screen의 모든 `CMP-` Task에 의존 |
| Component | `CMP-` | Screen당 여러 개(해당 Screen의 Section·컴포넌트 수만큼), 공용은 `CMP-SHARED-*` | 없음 또는 같은 Screen/공용의 다른 `CMP-` |
| 정적 데이터 | `DATA-` | `DATA-DESTINATIONS`, `DATA-SAFETY`, `DATA-REPRESENTATIVE` 3개 | 없음(독립) — 이 콘텐츠를 쓰는 `CMP-`/`PAGE-`가 의존 |
| DB/스키마 | `DB-` | §3의 6개 테이블 범위 내, `DB-SCHEMA-BASE`/`DB-RLS-BASE`/`DB-ACCESS`/`DB-SEED-BASE` 4개 | 없음(독립) — 이를 쓰는 `CMP-`/`PAGE-`/`AUTH-`가 의존 |
| 인증/인프라 | `AUTH-` | Supabase Auth 연동, 성인 확인 게이트 등 필요한 만큼 | `DB-`에 의존 가능 |
| 단위 테스트 | `UNIT-` | 날짜 검증·연락처 탐지·상태 전이 등 필요한 만큼 | 검증 대상 `CMP-`에 의존 |
| 통합 테스트 | `TEST-` | RLS 등 Playwright가 아닌 통합 테스트, 필요한 만큼 | `DB-RLS-BASE` 등에 의존 |
| E2E(Playwright) | `E2E-` | Chromium Smoke **1~3개** | 관련 `PAGE-` Task 전체에 의존(구현 완료 후 실행) |
| CI | `CI-` | Lint/Build/Test 파이프라인 1개 | 전 `UNIT-`/`TEST-`/`E2E-`에 의존 |
| 배포 확인 | `DEPLOY-` | Vercel·Supabase 배포 확인 각 1개 | `CI-`/`DB-RLS-BASE`/`AUTH-`에 의존 |

## 3. DB 테이블 상한(6개, 고정)

`PROJECT_SCOPE.md`의 IMPLEMENT 범위와 SCR-004/005 매핑 요구사항만 DB로 다룬다. 아래 6개 외의 테이블을 만드는 Task를 생성하지 않는다.

| # | 테이블 | 근거 Requirement |
|---|---|---|
| 1 | `user_profile` | REQ-FUNC-028, 029, 066 |
| 2 | `mate_post` | REQ-FUNC-031~033, 037~038, 080 |
| 3 | `mate_application` | REQ-FUNC-034~036 |
| 4 | `user_block` | REQ-FUNC-040 |
| 5 | `report` | REQ-FUNC-039, 041 |
| 6 | `outbound_url_setting` | REQ-FUNC-077 |

여행지(`destination`)·안전정보(`country_safety`)·대표 소개(`representative_profile`)는 이 표에 포함하지 않는다 — §1-11 규칙에 따라 `src/data/*.ts` 정적 데이터 Task로만 만든다. 감사 시 이 6개를 넘는 테이블 식별자가 소폭(2개 이하) 발견되면 통과, 그보다 많으면 실패로 처리한다(`scripts/audit_tasks.py` 검사 #12).

## 4. `TASKS/00_TASK_LIST.md` 작성 규칙

- Page Owner 5개는 `필드 | 내용` 세로형 표(Task 1개당 표 1개)로, 그 외(Component/Data/DB/Auth/Unit/Test/E2E/CI/Deploy)는 `Task ID`를 헤더에 포함한 가로형 표(여러 Task를 행으로 나열)로 작성한다. 두 형식 모두 `scripts/audit_tasks.py`가 파싱한다.
- 각 Task 레코드에는 최소한 `Task ID`, `제목`, `Implementation Status`, `Requirement Ref`, `Screen`(없으면 `N/A`), `Route`, `Page Entry`, `Depends On`, `Expected Files`, `Priority`를 포함한다.
- `Requirement Ref`는 `docs/UIUX_TRACEABILITY.md`/`docs/PROJECT_SCOPE.md`의 ID를 **범위 축약 없이 하나씩 전부** 나열한다(예: "REQ-FUNC-011~018"처럼 쓰지 않고 "REQ-FUNC-011, REQ-FUNC-012, ..., REQ-FUNC-018"로 쓴다) — 축약형은 기계적 커버리지 검증을 깨뜨린다.
- 하나의 Requirement가 여러 Task에 걸치는 것은 허용하되, IMPLEMENT Requirement가 **어떤 Task에도 연결되지 않는 것**은 금지한다.
- EXCLUDED Requirement는 Task 행이 아니라 문서 하단 "## 8. NON_IMPLEMENTATION Register" 표에 `Requirement | 근거(Source) | 후속 방향` 형식으로만 기록한다.

## 5. Expected Files 작성 규칙

1. `/gen-tasklist` 또는 `/gen-task-details` 실행 시점의 실제 파일 트리를 다시 확인한다(캐시된 이전 결과를 쓰지 않는다).
2. 이미 존재하는 파일은 `기존 파일 수정: <path>`로 표기한다.
3. 존재하지 않는 파일은 `신규 생성: <path>`로 표기한다.
4. `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `page_entry`와 다른 경로를 Page Owner의 Expected Files에 쓰지 않는다(`scripts/audit_tasks.py` 검사 #6이 이를 대조한다).
5. Task를 실행하는 것이 아니라 **계획**하는 단계이므로, 이 파이프라인 자체는 Expected Files에 적힌 파일을 실제로 만들거나 고치지 않는다.

## 6. `TASKS/TASK-<ID>.md` 상세 파일 필수 절

모든 상세 파일은 다음 13개 절을 이 순서로 포함한다: `Context`, `Project Scope`, `Requirement Ref`, `Screen / Route / Page Entry`, `Design Ref`, `Depends On`, `Expected Files`, `Functional AC`, `Visual AC`, `Security/Privacy AC`, `Test Cases`, `Verify`, `Definition of Done`, `Forbidden`.

Page Owner Task 상세는 위에 더해 다음을 **모두** 포함해야 한다.

1. 해당 Screen의 Section 순서(제목까지)와 각 Section의 최소 콘텐츠 수 — `design-reference/UI_CONTRACT.md` 및 `design-reference/D-001/DESIGN.md` §18의 표를 그대로 인용.
2. "큰 빈 영역을 만들지 않는다"와 "Lorem ipsum/준비 중/정보 확인 필요 금지" 조항.
3. 데이터가 없는 경우에도 안내 문장 + 이용 방법 + CTA를 갖춘 완성형 Empty State 조건.
4. `PAGE-SCR001`에는 추가로: "`create-next-app` 기본 Starter 마크업(로고, 기본 링크, 기본 문구)이 완전히 제거되었는지" AC.
5. `PAGE-SCR003`에는 추가로: "항공편/숙소/동행 구하기 3개 탭이 모두 실제 콘텐츠로 조립되고 서로 독립된 상태를 유지하는지" AC.
6. `PAGE-SCR005`에는 추가로: "Guest/Member/Admin 상태가 각각 실제로 조립되고, 역할에 없는 탭은 렌더링되지 않는지" AC.

## 7. 검증 스크립트 사용법

- `python scripts/validate_inputs.py` — Task 생성 **전** 입력 문서·계약 정합성을 검증한다. 실패 시 `/gen-tasklist`를 진행하지 않는다.
- `python scripts/audit_tasks.py` — `TASKS/00_TASK_LIST.md`, `TASKS/TASK-*.md`, `docs/PROJECT_SCOPE.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`을 입력으로 18개 최종 감사 항목(1:1 대응, 중복 0, Depends On 누락 0, Dependency Cycle 0, Page Owner 5개, Route/Page Entry/Expected Files 일치, Component-only Screen 0, SCR-001/003/005 AC 존재, DB Schema·RLS·Access·Seed 존재, DB Table 상한, 외부 입력 비저장 AC, Auth·성인·RLS AC, Playwright Chromium Task, AWS/EC2/자동 Merge 0, Requirement 114개 전량 계정, EXCLUDED 전용 Task 없음)을 검증하고 `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md`를 생성한다.
- 통과 시 `AUDIT_PASS`와 통과 검사 수를 출력(종료 코드 0)하고, 실패 시 `AUDIT_FAIL`과 위반 목록을 출력한다(종료 코드 1). **`AUDIT_FAIL`을 무시하고 완료로 보고하지 않는다.**
- 두 스크립트 모두 표준 라이브러리만 사용한다. 이 환경에서 `python3`는 정상 동작하지 않을 수 있으므로(Microsoft Store 스텁으로 리디렉션) `python`으로 대체 실행하고 그 사실을 보고에 남긴다.

## 8. Task 개수에 대한 태도

45~65개 정도가 예상되며 현재 확정본은 64개다. **개수 자체는 완료 조건이 아니다.** §1의 20개 규칙과 §7의 두 스크립트(특히 `AUDIT_PASS`)를 모두 통과하는 것이 유일한 완료 조건이다. 규칙을 지키기 위해 개수가 범위를 벗어나도 무리하게 합치거나 쪼개지 않는다.
