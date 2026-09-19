# Free Traveler — Project State

**Document ID:** STATE-TRAVEL-001
**최종 갱신:** 2026-09-19
**갱신 방법:** 현재는 수동으로 유지한다. `/run-wave`, `/release-check`가 실행될 때마다 이 문서의 해당 필드를 그 결과로 갱신해야 한다(자동 갱신 스크립트는 아직 없음). 실제로 확인되지 않은 값을 추정해서 채우지 않는다 — 모르면 `UNKNOWN` 또는 `NOT_STARTED`로 남긴다.

---

## 상태 요약

| 필드 | 값 | 근거 |
|---|---|---|
| **Harness Schema** | `traveler-screen-route-v1` | `design-reference/SCREEN_ROUTE_CONTRACT.json` `schema_version` |
| **Design Version** | `D-001`(Status: LOCKED) | `design-reference/DESIGN_MANIFEST.md` |
| **Scope Mode** | MVP — `docs/PROJECT_SCOPE.md` 기준 REQ-FUNC 64 IMPLEMENT / 16 EXCLUDED, REQ-NF 12 IMPLEMENT / 22 EXCLUDED(총 114건 중 76 IMPLEMENT / 38 EXCLUDED) | `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md` |
| **Current Wave** | `NONE` — `TASKS/WAVE_PLAN.md`가 아직 작성되지 않아 어떤 Wave도 시작되지 않았다 | `TASKS/` 디렉터리 확인(2026-09-19) |
| **Current Task** | `NONE` | 상동 |
| **Completed Tasks** | `0/64` — `TASKS/00_TASK_LIST.md`에 정의된 구현 Task 64개 중 `DONE`은 0개(추적 파일 자체가 없음) | `TASKS/00_TASK_LIST.md` §0 |
| **Blocked Tasks** | `NONE`(아직 어떤 Task도 `/prepare-task`를 통과 시도하지 않아 BLOCKED 판정 자체가 존재하지 않음) | — |
| **Latest CI** | `NOT_RUN` — `.github/workflows/ci.yml` 미생성(`CI-LINT-BUILD` Task 미착수) | `docs/ARCHITECTURE.md` §12(착수 차단), 저장소 실측 |
| **Supabase State** | `NOT_CONFIGURED` — `supabase/` 디렉터리·`.env.local` 없음, 6개 테이블(`user_profile`/`mate_post`/`mate_application`/`user_block`/`report`/`outbound_url_setting`) 미생성, RLS 정책 미적용 | `docs/ARCHITECTURE.md` §7, §11 |
| **Vercel Preview URL** | `NONE` | 배포 이력 없음(`DEPLOY-VERCEL` Task 미착수) |
| **Screen Checkpoints** | 아래 표 참조 | `TASKS/00_TASK_LIST.md` §1(Page Owner), `design-reference/SCREEN_ROUTE_CONTRACT.json` |
| **Playwright State** | `NOT_INSTALLED` — `package.json`에 `@playwright/test` 없음, `tests/e2e/` 없음 | `package.json`, 저장소 실측 |
| **Deferred Items** | EXCLUDED 38건(REQ-FUNC 16 + REQ-NF 22) + 범위 자체를 제외한 영역(CMS, 외부 이메일 공급자, Monitoring, EC2/AWS, 자동 Merge, Prisma/ORM) | `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md` §8, `docs/ARCHITECTURE.md` §10 |
| **Next Action** | 아래 "다음 행동" 절 참조 | — |

---

## Screen Checkpoints

| Screen | Route | 상태 | 비고 |
|---|---|---|---|
| SCR-001 | `/` | `PENDING` | Page Owner `PAGE-SCR001` 미착수. 완료 조건: Next.js Starter 제거 + 7개 Section 조립 + `E2E-PUBLIC-SMOKE` 통과 |
| SCR-002 | `/about` | `PENDING` | Page Owner `PAGE-SCR002` 미착수 |
| SCR-003 | `/travel-tools` | `PENDING` | Page Owner `PAGE-SCR003` 미착수. 완료 조건: 항공/숙소/동행 3탭 전부 조립 + `E2E-TRAVEL-TOOLS` 통과 |
| SCR-004 | `/mates` | `PENDING` | Page Owner `PAGE-SCR004` 미착수 |
| SCR-005 | `/account` | `PENDING` | Page Owner `PAGE-SCR005` 미착수. 완료 조건: Guest/Member/Admin 3역할 조립 + `E2E-MATE-AUTH` 통과 |
| **FINAL** | — | `PENDING` | `/release-check`가 `RELEASE_READY`를 판정할 때만 `DONE`으로 갱신한다 |

각 Screen Checkpoint 상태 값의 의미: `PENDING`(미착수) → `IN_PROGRESS`(해당 Page Owner Task가 `WAVE_STATE.md`에서 `IN_PROGRESS`) → `WAITING_FOR_PREVIEW`(Page Owner `DONE` 후 사람 Preview 대기 중, `/run-wave` §Preview Checkpoint) → `DONE`(사람이 Preview를 확인하고 다음 Wave로 진행 승인).

---

## 다음 행동 (Next Action)

1. `TASKS/WAVE_PLAN.md`를 작성해 64개 Task를 Wave 단위로 나누고 Screen별 Page Owner 완료 지점에 Preview Checkpoint를 표시한다(`docs/DECISION_LOG.md` DEC-010 참조 — 아직 이 계획 자체가 없다).
2. Wave 계획이 준비되면 `/run-wave <첫 Wave ID>`로 착수한다. 각 Task는 `/prepare-task` → `/implement-task` 순서를 거친다.
3. 착수 전 `docs/ARCHITECTURE.md` §11의 착수 차단 항목(`src/data`·`src/lib`·`supabase`·`tests`·`.github/workflows` 디렉터리, `@supabase/supabase-js`·`vitest`·`@playwright/test` 설치, `.env.local` 및 환경변수)을 먼저 해소해야 하는 Task(`DB-SCHEMA-BASE`, `AUTH-SUPABASE-SETUP` 등)부터 순서대로 처리한다.
4. 각 Screen의 Page Owner Task가 `DONE`되고 Preview 확인이 끝날 때마다 이 문서의 "Screen Checkpoints" 표를 갱신한다.
5. 5개 Screen이 모두 `DONE`이면 `/release-check`를 실행해 `RELEASE_READY`/`RELEASE_BLOCKED`를 판정하고, 그 결과로 이 문서의 나머지 필드(Latest CI, Supabase State, Vercel Preview URL, Playwright State, FINAL Checkpoint)를 갱신한다.
