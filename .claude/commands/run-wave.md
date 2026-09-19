---
description: Wave 단위로 Task를 prepare-task→implement-task 순서로 순차 실행하고 상태를 추적한다(자동 Branch·PR·Merge 없음)
---

`traveler-project-pipeline` Skill을 로드한다. 이 명령은 **자동 Branch 생성·PR 생성·Merge를 절대 포함하지 않는다.** Commit 여부는 각 Task 구현 시 `/implement-task` §9 규칙(기본 미수행, 사용자가 명시적으로 요청할 때만 Task 단위 Commit)을 그대로 따른다.

## 상태 파일

이 명령은 두 파일을 근거로 삼는다. 둘 다 없으면 **Wave를 실행하지 않는다** — 존재하지 않는 계획을 있는 것처럼 가정하지 않는다.

- **`TASKS/WAVE_PLAN.md`**: Wave별로 포함되는 Task ID 목록과, 그 Wave 안에서 사람의 Preview 확인이 필요한 지점(Preview Checkpoint)을 정의한다. 형식(없으면 `/run-wave`가 사용자에게 먼저 만들어 달라고 요청한다):

  ```markdown
  | Wave | Task ID | Preview Checkpoint |
  |---|---|---|
  | W03 | CMP-SCR001-HERO | |
  | W03 | CMP-SCR001-DEST-DOMESTIC | |
  | W03 | PAGE-SCR001 | Y |
  ```
  `Preview Checkpoint`가 `Y`인 행의 Task가 `DONE`이 되면, 같은 Wave에 이후 Task가 남아 있어도 자동으로 이어가지 않고 `WAITING_FOR_PREVIEW`로 멈춘다(`CLAUDE.md` 규칙 22).

- **`TASKS/WAVE_STATE.md`**: 각 (Wave, Task) 쌍의 현재 상태를 기록한다. 파일이 없으면 이 명령이 `TASKS/WAVE_PLAN.md`의 모든 행을 `PENDING` 상태로 처음 생성한다.

  ```markdown
  | Wave | Task ID | Status | Updated | Note |
  |---|---|---|---|---|
  | W03 | CMP-SCR001-HERO | DONE | 2026-09-19T10:00:00 | |
  | W03 | CMP-SCR001-DEST-DOMESTIC | IN_PROGRESS | 2026-09-19T10:05:00 | |
  | W03 | PAGE-SCR001 | PENDING | | Depends On 미충족 |
  ```
  Status 값: `PENDING`(아직 READY 아님) · `READY`(Depends On 전부 DONE) · `IN_PROGRESS`(구현 중) · `DONE` · `BLOCKED_INPUT`/`BLOCKED_DEPENDENCY`/`BLOCKED_DIRTY_TREE`/`BLOCKED_SCOPE`(`/prepare-task` 결과 그대로).

READY 판정: 해당 Task의 `TASKS/TASK-<ID>.md` `Depends On`에 나열된 모든 ID가 (같은 Wave 안에서든 이전 Wave에서든) `WAVE_STATE.md`에 `DONE`으로 기록되어 있으면 `READY`, 아니면 `PENDING`.

## 지원하는 호출 형태

### `/run-wave <WAVE_ID>` (예: `/run-wave W03`)

1. `TASKS/WAVE_PLAN.md`와 `TASKS/WAVE_STATE.md`를 **실제로 Read**한다. `WAVE_PLAN.md`에 `<WAVE_ID>`가 없으면 실행하지 않고 그 사실만 보고한다.
2. `WAVE_STATE.md`를 최신 `Depends On` 정보(`TASKS/00_TASK_LIST.md`)로 다시 계산해 각 Task의 Status를 `PENDING`/`READY`로 갱신한다(이미 `DONE`/`IN_PROGRESS`/`BLOCKED_*`인 행은 건드리지 않는다).
3. 이 Wave의 `READY` Task 중 `TASKS/00_TASK_LIST.md`의 `Depends On` 순서(위상 순서)상 가장 먼저 와야 하는 것 **하나만** 선택한다. `READY` Task가 없으면:
   - 모든 Task가 `DONE`이면 §"Wave 종료" 참조.
   - 하나 이상 `BLOCKED_*`이면 그 Task들과 사유를 보고하고 종료한다(자동으로 건너뛰지 않는다).
   - 그 외(전부 `PENDING`이지만 `DONE`도 아님)면 순환 의존 등 이상 상태이므로 실행을 멈추고 보고한다.
4. 선택한 Task에 `/prepare-task <WAVE_ID> <TASK_ID>`와 동일한 8개 검사를 적용한다.
   - `READY_TO_IMPLEMENT`가 아니면 `WAVE_STATE.md`의 해당 행을 그 `BLOCKED_*` 상태로 갱신하고, 이 Task 처리를 멈춘 뒤 **같은 Wave의 다른 READY Task로 넘어가지 않고** 바로 멈춰서 보고한다(의존 순서를 건너뛰어 뒤 Task를 먼저 처리하지 않는다).
5. `READY_TO_IMPLEMENT`면 `WAVE_STATE.md`를 `IN_PROGRESS`로 갱신하고 `/implement-task`와 동일한 규칙으로 이 Task 하나를 구현한다(Expected Files 안에서만, AC 충족, Page Owner는 조립만, 관련 Unit Test, Category가 PAGE/E2E일 때만 Playwright).
6. 구현 후 관련 검증(Unit Test, 해당하면 Playwright Smoke)이 **전부 PASS**하면 `WAVE_STATE.md`를 `DONE`으로 갱신하고 완료 보고(§`/implement-task` 형식)를 남긴다. 하나라도 FAIL이면 `DONE`으로 바꾸지 않고 실패 내용과 함께 멈춘다 — 임의로 다음 Task로 넘어가지 않는다.
7. 방금 `DONE`이 된 Task가 `TASKS/WAVE_PLAN.md`에서 `Preview Checkpoint = Y`이면, 같은 Wave에 남은 Task가 있어도 여기서 멈추고 상태를 **`WAITING_FOR_PREVIEW`**로 보고한다. 아니면 이 Wave의 다음 `READY` Task를 찾아 3번부터 반복한다.
8. 이 Wave의 모든 Task가 `DONE`이면 **Wave 종료**로 보고한다(`WAVE_COMPLETE`). 자동으로 다음 Wave를 시작하지 않는다.

### `/run-wave status`

- 코드나 상태 파일을 바꾸지 않는다(읽기 전용).
- `TASKS/WAVE_STATE.md`가 없으면 "아직 어떤 Wave도 시작되지 않았다"고 보고한다.
- 있으면 Wave별로 Task 수, 각 Status별 개수, 마지막으로 갱신된 Task와 시각, 있다면 현재 `WAITING_FOR_PREVIEW`/`BLOCKED_*` 상태의 Task를 표로 요약해 보고한다.

### `/run-wave resume`

- `TASKS/WAVE_STATE.md`를 읽어 `IN_PROGRESS` 상태로 남아 있는 Task가 있는지 확인한다(이전 실행이 중간에 끊긴 경우).
  - 있으면: 그 Task의 실제 파일 상태(`git status`/Expected Files 존재 여부)를 다시 확인해 어디까지 되어 있는지 보고한 뒤, 사용자에게 "이어서 구현할지, `PENDING`으로 되돌리고 다시 `/prepare-task`부터 할지" 확인한다 — 임의로 이어서 구현하지 않는다.
  - 없으면: 가장 최근에 사람이 `WAITING_FOR_PREVIEW`로 멈춘 Wave를 찾아 "Preview를 확인했다면 `/run-wave <WAVE_ID>`로 계속 진행하라"고 안내한다. `WAITING_FOR_PREVIEW`도 없으면 다음으로 `READY` Task가 있는 Wave를 안내한다.

### `/run-wave dry-run <WAVE_ID>` (예: `/run-wave dry-run W03`)

- `/run-wave <WAVE_ID>`와 동일하게 1~3단계(상태 파일 읽기, READY 계산, 다음 실행 대상 선택)까지만 수행한다.
- 4단계 이후(`/prepare-task`·`/implement-task` 실질 검사·구현)는 **실행하지 않는다.**
- 이 Wave를 지금 `/run-wave <WAVE_ID>`로 실행하면 어떤 순서로 어떤 Task가 처리될지 예상 순서 목록과, 각 Task가 Preview Checkpoint인지 여부만 출력한다.
- 어떤 파일도 쓰지 않는다(`WAVE_STATE.md`도 갱신하지 않는다).

## 공통 금지 사항

- 이 명령은 어떤 호출 형태에서도 Git Branch를 새로 만들거나, PR을 생성하거나, Merge를 수행하지 않는다.
- 한 Wave 안에서 여러 Task를 동시에(병렬로) 처리하지 않는다(`docs/DECISION_LOG.md` DEC-011).
- `Depends On` 순서를 건너뛰고 뒤 순서 Task를 먼저 구현하지 않는다.
- `BLOCKED_*`나 검증 실패를 만나면 계속 진행하지 않고 그 자리에서 멈춰 보고한다.
- `TASKS/WAVE_PLAN.md`가 없는 상태에서 Wave 구성을 임의로 추측해 만들지 않는다 — 사용자에게 먼저 작성을 요청한다.
