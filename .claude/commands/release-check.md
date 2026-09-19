---
description: 출시 전 Task·Wave·CI·Playwright·Supabase·Preview·EXCLUDED 상태를 종합해 RELEASE_READY/RELEASE_BLOCKED를 판정한다(읽기 전용)
---

이 명령은 **읽기 전용**이다. 코드·설정·상태 파일을 수정하지 않고, 이미 만들어진 산출물(`TASKS/*`, `docs/*`, CI/Vercel 상태)을 모아 출시 가능 여부만 판정한다. 부족한 부분을 발견해도 스스로 구현하거나 상태를 고쳐 쓰지 않는다 — 그것은 `/run-wave`·`/implement-task`의 몫이다.

## 검사 7개 (전부 실제로 확인, 짐작하지 않음)

### 1. Task·Wave 상태
- `TASKS/WAVE_STATE.md`를 **실제로 Read**한다. 파일이 없으면 "Wave 실행 기록이 없음"으로 기록하고 이 검사를 실패로 처리한다.
- 있으면 전체 Task 중 `DONE` 개수, `BLOCKED_*`/`IN_PROGRESS`/`PENDING`/`READY`로 남아 있는 Task 목록을 집계한다.
- `TASKS/00_TASK_LIST.md`의 구현 Task 전체(§0 요약의 총 개수)와 `WAVE_STATE.md`에 등장하는 Task 수를 대조해, `WAVE_PLAN.md`/`WAVE_STATE.md`에 아예 등록되지 않은 Task가 있으면 그것도 미완료로 간주한다.
- `DONE`이 아닌 Task가 하나라도 있으면 이 검사는 실패다.

### 2. 5개 Page Owner DONE
- `WAVE_STATE.md`에서 `PAGE-SCR001`~`PAGE-SCR005` 5개 행을 찾는다.
- 5개 전부 `DONE`이어야 통과다. 하나라도 없거나 `DONE`이 아니면 실패로 기록하고 어떤 Screen이 남았는지 구체적으로 남긴다.

### 3. CI PASS
- 가능하면 `gh run list`/`gh pr checks`(GitHub CLI)로 main 브랜치 또는 최신 관련 PR의 최근 CI 실행 결과를 확인한다. `gh`를 쓸 수 없거나 원격 저장소가 없으면, `TASKS/TASK-CI-LINT-BUILD.md`의 상태(`WAVE_STATE.md`상 `DONE`)와 사용자에게 "최근 CI 실행이 실제로 성공했는지" 직접 확인을 요청한다 — 확인받지 못하면 이 검사를 통과로 처리하지 않는다.
- TypeScript strict, ESLint, Unit Test가 모두 실패 없이 끝났다는 근거(로그·`gh` 결과·사용자 확인)가 있어야 통과다.

### 4. Playwright Smoke PASS
- `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH`(또는 현재 `TASKS/00_TASK_LIST.md`에 정의된 `E2E-*` 전체) 각각이 `WAVE_STATE.md`에서 `DONE`인지 확인한다.
- 각 Task가 Chromium 프로젝트로 실제 실행되어 통과했다는 근거(`/implement-task` 완료 보고, CI 로그 등)가 있는지 확인한다. 근거 없이 "DONE으로 표시돼 있으니 통과"로 단정하지 않는다 — 근거가 불명확하면 실패로 기록하고 재확인을 요청한다.

### 5. Supabase 6개 Table·기본 RLS 확인 기록
- `docs/ops/supabase-checklist.md`(`DEPLOY-SUPABASE-CHECK` Task 산출물)가 존재하고, 그 안에 6개 테이블(`user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_url_setting`)이 실제 운영 Supabase 프로젝트에 생성되어 있다는 확인 기록과, `docs/ARCHITECTURE.md` §7.3의 기본 RLS 원칙(공개 읽기/본인 쓰기/작성자 처리/Admin 전용)이 적용되어 있다는 확인 기록이 있는지 본다.
- 파일이 없거나, 있어도 "확인함"이라는 서술 없이 체크리스트 항목만 비어 있으면 실패로 기록한다.

### 6. Vercel Preview Checkpoint
- `TASKS/WAVE_PLAN.md`에서 `Preview Checkpoint = Y`로 표시된 모든 행을 찾는다.
- 각 Checkpoint 이후 Wave 실행이 실제로 `WAITING_FOR_PREVIEW`로 멈췄다가 사람이 확인 후 재개된 이력이 있는지 `WAVE_STATE.md`의 `Note` 열이나 사용자 확인으로 판단한다.
- 아직 사람이 Preview를 확인하지 않은 Checkpoint가 하나라도 남아 있으면 실패로 기록한다.
- `docs/ops/vercel-checklist.md`(`DEPLOY-VERCEL` Task 산출물)가 존재하고 환경변수 등록·배포 확인이 기록되어 있는지도 함께 본다.

### 7. EXCLUDED 목록
- `docs/PROJECT_SCOPE.md`와 `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register를 비교해, EXCLUDED로 분류된 Requirement가 그 사이 임의로 구현되지 않았는지 확인한다(`python scripts/audit_tasks.py`를 실행해 검사 #18 결과를 재사용한다 — 이 스크립트는 검증만 하고 코드를 만들지 않으므로 이 명령의 읽기 전용 원칙을 어기지 않는다).
- `scripts/audit_tasks.py`가 `AUDIT_PASS`가 아니면 이 검사는 실패이며, 그 즉시 다른 검사 결과와 무관하게 `RELEASE_BLOCKED`의 핵심 사유로 보고한다.
- EXCLUDED 목록 자체는 출시를 막는 사유가 아니다 — 오히려 이 검사의 목적은 "출시본이 EXCLUDED 범위를 넘지 않았다"는 것과 "무엇이 의도적으로 빠져 있는지"를 릴리스 노트용으로 명확히 남기는 것이다. 최종 보고서에 EXCLUDED 38건 요약을 그대로 첨부한다.

## 판정

- 위 7개 검사가 **전부** 통과해야 `RELEASE_READY`다.
- 하나라도 실패하면 `RELEASE_BLOCKED`이며, 실패한 검사 번호·구체적 사유·무엇을 하면 해결되는지(예: "`/run-wave W05`로 남은 Task 진행", "`docs/ops/supabase-checklist.md` 확인 기록 추가 요청")를 함께 보고한다.
- 일부만 통과했다고 "부분 통과"나 "거의 준비됨" 같은 중간 판정을 만들지 않는다 — 반드시 `RELEASE_READY` 또는 `RELEASE_BLOCKED` 둘 중 하나로만 결론짓는다.

## 보고 형식

```
판정: RELEASE_READY | RELEASE_BLOCKED

1. Task·Wave 상태: <통과/실패 + 근거>
2. 5개 Page Owner DONE: <통과/실패 + 근거>
3. CI PASS: <통과/실패 + 근거>
4. Playwright Smoke PASS: <통과/실패 + 근거>
5. Supabase 6개 Table·기본 RLS 확인 기록: <통과/실패 + 근거>
6. Vercel Preview Checkpoint: <통과/실패 + 근거>
7. EXCLUDED 목록: <통과/실패 + AUDIT_PASS 여부> / EXCLUDED 요약 <건수, 출처>

RELEASE_BLOCKED인 경우 다음 조치:
- <검사 번호>: <무엇을 하면 해결되는지>
```

## 금지 사항

- 이 명령 실행 중 어떤 소스 코드·설정·`TASKS/WAVE_STATE.md`도 수정하지 않는다.
- `RELEASE_READY`를 만들기 위해 검사를 완화하거나 근거 없이 통과 처리하지 않는다.
- 실제 배포(Vercel Production 배포 트리거, Git Merge 등)를 수행하지 않는다 — 이 명령은 판정만 하고, 실제 배포 실행은 사람이 한다.
