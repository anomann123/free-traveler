---
description: Wave 하나를 pending Task 순서대로 prepare→implement하고 상태를 추적한다(자동 Branch·PR·Merge·다음 Wave 진행 없음)
---

`traveler-project-pipeline` Skill을 로드한다. 이 명령은 **자동 Branch 생성·PR 생성·Merge를 절대 포함하지 않는다.** Commit 여부는 각 Task 구현 시 `/implement-task` §9 규칙(기본 미수행, 사용자가 명시적으로 요청할 때만 Task 단위 Commit)을 그대로 따른다.

## 0. 입력

```
/run-wave <WAVE_ID> [--dry-run] [--resume] [--status]
```

- `WAVE_ID`: `TASKS/WAVE_PLAN.md`/`TASKS/WAVE_STATE.json`에 실제로 존재하는 Wave ID(예: `W06`). `--status`는 `WAVE_ID`를 생략하면 전체 Wave를 요약한다.
- 옵션은 서로 배타적이다(동시에 여러 개를 주면 `--status` > `--dry-run` > `--resume` 우선순위로 하나만 따른다).
- 옵션이 없으면 **기본 동작**(§3)을 수행한다.

## 1. 상태 파일

이 명령은 두 파일을 근거로 삼는다. 둘 다 없으면 **Wave를 실행하지 않는다** — 존재하지 않는 계획을 있는 것처럼 가정하지 않는다. `python scripts/build_waves.py`를 먼저 실행해 달라고 사용자에게 요청한다.

- **`TASKS/WAVE_PLAN.md`**: Wave별 Task ID 목록과 Preview Checkpoint 여부(요약 표의 `Preview Checkpoint` 열, 상세 표의 각 행). Wave 순서(어느 Wave가 "이전 Wave"인지)는 이 문서에 등장하는 순서(`scripts/build_waves.py`가 그룹 순서대로 W01, W02, … 순차 부여) 그대로 따른다.
- **`TASKS/WAVE_STATE.json`**: `schema_version: traveler-wave-state-v1`. 최상위에 `waves[]`가 있고 각 항목은 다음 필드를 갖는다.

  ```json
  {
    "wave_id": "W06",
    "title": "SCR-001 메인 Component와 Page Owner",
    "task_ids": ["CMP-SCR001-HERO", "..."],
    "status": "pending",
    "checkpoint_required": false,
    "checkpoint_result": null,
    "tasks": [
      { "task_id": "CMP-SCR001-HERO", "status": "PENDING", "updated_at": null, "note": "" }
    ]
  }
  ```

  `tasks[]`는 `scripts/build_waves.py`가 아직 만들지 않는 **확장 필드**다. 어떤 Wave 항목에 `tasks[]`가 없으면, 이 명령이 그 Wave의 `task_ids` 전부를 `status: "PENDING"`, `updated_at: null`, `note: ""`로 최초 생성한 뒤 파일에 다시 쓴다(다른 필드는 건드리지 않는다).

  **Task별 `status` 값**: `PENDING`(아직 시작 전) · `READY`(Depends On 전부 DONE, 착수 가능) · `IN_PROGRESS`(구현 중) · `DONE` · `BLOCKED_INPUT`/`BLOCKED_DEPENDENCY`/`BLOCKED_DIRTY_TREE`/`BLOCKED_SCOPE`(`/prepare-task` 판정 그대로).

  **Wave `status` 값(4가지, 이 스키마에 고정)**: `pending`(모든 Task가 PENDING) · `in_progress`(하나 이상 IN_PROGRESS/DONE이지만 전부 DONE은 아니고 BLOCKED도 없음) · `blocked`(하나 이상 BLOCKED_*) · `completed`(모든 Task DONE이고, `checkpoint_required=true`면 `checkpoint_result`도 사람이 확인 완료로 기록됨). 이 4개 값 외의 문자열을 넣지 않는다.

  READY 판정: 해당 Task의 `TASKS/TASK-<ID>.md` `Depends On`에 나열된 모든 ID가 (이 Wave 안이든 이전 Wave든) `WAVE_STATE.json`에 `DONE`으로 기록되어 있으면 `READY`.

## 2. `--status` — 읽기 전용 상태 조회

- 코드나 상태 파일을 바꾸지 않는다.
- `WAVE_STATE.json`이 없으면 "아직 어떤 Wave도 시작되지 않았다"고 보고한다.
- `WAVE_ID` 없이 호출하면: 전체 Wave를 표로 요약(Wave ID·제목·Task 수·Wave status·Checkpoint 필요 여부·Checkpoint 결과), 그리고 `blocked`이거나 Checkpoint 대기 중인 Wave를 강조해서 보고한다.
- `WAVE_ID`를 주면: 그 Wave의 각 Task ID·status·`updated_at`·`note`를 표로 보여준다.

## 3. 기본 동작(옵션 없음) — pending Task를 하나씩 prepare + implement

1. **이전 Wave 완료 확인(규칙 1)**: `WAVE_PLAN.md`에 등장하는 순서 기준으로 `WAVE_ID`보다 앞선 모든 Wave의 `status`가 `completed`인지 확인한다. 하나라도 `completed`가 아니면 **이 Wave를 시작하지 않고**, 어느 Wave가 어떤 상태(`pending`/`in_progress`/`blocked`)인지 구체적으로 보고한 뒤 종료한다.
2. `WAVE_STATE.json`을 최신 `Depends On` 정보(`TASKS/00_TASK_LIST.md` 또는 `TASK_MANIFEST.csv`)로 다시 계산해 이 Wave의 각 Task `status`를 `PENDING`/`READY`로 갱신한다(이미 `DONE`/`IN_PROGRESS`/`BLOCKED_*`인 항목은 건드리지 않는다).
3. 이 Wave의 Task를 **Task ID 오름차순으로** 순회하며, `status`가 `READY`인 첫 Task 하나를 선택한다.
   - `READY` Task가 없고 전부 `DONE`이면 §6 "Wave 완료 처리"로 간다.
   - `READY` Task가 없고 하나 이상 `BLOCKED_*`이면 그 Task와 사유를 보고하고 멈춘다(규칙 2 — 이미 `blocked`로 기록되어 있을 것이다).
   - 그 외(전부 `PENDING`이지만 `DONE`도 아닌 상태)면 순환 의존 등 이상 상태이므로 실행을 멈추고 보고한다.
4. 선택한 Task에 `/prepare-task <WAVE_ID> <TASK_ID>`와 동일한 8개 검사를 적용한다.
   - `READY_TO_IMPLEMENT`가 아니면: 그 Task의 `status`를 해당 `BLOCKED_*` 값으로, 이 **Wave의 `status`를 `blocked`로** 기록하고(규칙 2) 즉시 멈춘다. 같은 Wave의 다른 Task로 건너뛰지 않는다.
5. `READY_TO_IMPLEMENT`면 Task `status`를 `IN_PROGRESS`로 갱신하고 `/implement-task`와 동일한 규칙으로 이 Task 하나를 구현한다(Expected Files 안에서만, AC 충족, Page Owner는 조립만).
6. **최소 검증 실행(규칙 3)**: Category에 따라 관련 Unit Test(있으면), Category가 `PAGE`/`E2E`일 때만 Playwright Chromium Smoke를 실행한다(그 외 Category는 Playwright를 실행하지 않는다 — `/implement-task` §4~§5와 동일).
7. 검증이 **전부 PASS**하면 Task `status`를 `DONE`으로, `updated_at`을 현재 시각으로 갱신한다. 하나라도 FAIL이면 `DONE`으로 바꾸지 않고 실패 내용과 함께 멈춘다 — 임의로 다음 Task로 넘어가지 않는다.
8. 방금 `DONE`이 된 Task가 이 Wave의 **Page Owner Task**이고 이 Wave의 `checkpoint_required=true`이면(규칙 4 — `build_waves.py`가 Page Owner를 해당 화면 그룹의 마지막 Wave에 단독 배치하므로 보통 이 Task가 Wave의 마지막 Task다): 이 Wave를 더 진행하지 않고 Wave `status`를 `in_progress`로 유지한 채(=아직 `completed`로 표시하지 않음) 사람에게 Browser Preview 확인을 요청하며 멈춘다(규칙 5). `checkpoint_result`는 사람이 실제로 확인하고 이 명령을 통해 그렇다고 답하기 전까지 `null`로 둔다.
9. Checkpoint 대상이 아니면 이 Wave의 다음 `READY` Task를 찾아 3번부터 반복한다.

## 4. `--dry-run` — 아무것도 바꾸지 않고 실행 계획만 보여준다

1~3단계(상태 파일 읽기·READY 계산·다음 실행 대상 선택)까지만 수행하고, 4단계 이후(`/prepare-task`·`/implement-task` 실질 검사·구현·검증)는 **실행하지 않는다**. 다음을 출력한다.

- 이 Wave에서 지금 `/run-wave <WAVE_ID>`를 실행하면 처리될 다음 Task ID(READY 기준)
- 그 Task의 `Expected Files` 목록(`TASKS/TASK-<ID>.md`에서 그대로 인용)
- 그 Task에 적용될 최소 검증(Unit Test 대상, Playwright 대상 여부)
- 이 Wave가 `checkpoint_required`인지, 그렇다면 어느 Task 완료 시 Browser Checkpoint가 걸리는지
- 이전 Wave가 전부 `completed`인지 여부(아니라면 그 사실도 함께 경고)

어떤 파일도 쓰지 않는다(`WAVE_STATE.json`도 갱신하지 않는다).

## 5. `--resume` — 첫 pending 또는 blocked Task부터 다시 시작

1. `WAVE_STATE.json`에서 이 Wave의 Task를 Task ID 오름차순으로 보고, `IN_PROGRESS`로 남아 있는 Task가 있는지 먼저 확인한다(이전 실행이 중간에 끊긴 경우).
   - 있으면: 그 Task의 실제 파일 상태(`git status`/Expected Files 존재 여부)를 다시 확인해 어디까지 되어 있는지 보고한 뒤, 사용자에게 "이어서 구현할지, `PENDING`으로 되돌리고 다시 `/prepare-task`부터 할지" 확인한다 — 임의로 이어서 구현하지 않는다.
2. `IN_PROGRESS`가 없으면, Task ID 오름차순으로 **가장 먼저 나오는 `PENDING` 또는 `BLOCKED_*` Task**를 이번 실행의 시작점으로 삼아 §3의 3번부터 이어간다(그 앞의 `DONE` Task는 다시 실행하지 않는다).
3. 이 Wave에 `PENDING`/`BLOCKED_*` Task가 전혀 없고 Checkpoint만 남아 있으면(§3-8 상태), 사람의 Preview 확인 여부를 묻는다 — 확인됐다고 답하면 `checkpoint_result`를 기록하고 §6 Wave 완료 처리로 간다.

## 6. Wave 완료 처리

- 이 Wave의 모든 Task가 `DONE`이고, `checkpoint_required=false`이거나(`checkpoint_required=true`이고 사람이 Preview 확인을 명시적으로 확인해줬다면) → Wave `status`를 `completed`로 갱신하고 **`WAVE_COMPLETE`**로 보고한다.
- `checkpoint_required=true`인데 아직 사람 확인 전이면 → `status`는 `in_progress`로 두고 `WAITING_FOR_PREVIEW`로 보고한다.
- 어느 경우든 **자동으로 다음 Wave를 시작하지 않는다**(규칙 5). 다음 Wave 실행은 사람이 별도로 `/run-wave <다음 WAVE_ID>`를 호출해야 한다.

## 7. 종료 보고(필수 형식)

```
WAVE_ID: <ID>
상태: WAVE_COMPLETE | WAITING_FOR_PREVIEW | BLOCKED | (진행 중 중단 사유)

완료 Task:
- <TASK_ID> (<상태 변경 시각>)

변경 파일:
- <path> (신규 생성 | 수정) — <TASK_ID> 소속

통과한 검사:
- <TASK_ID>: Unit Test <결과> / Playwright <결과 또는 "해당 없음">

남은 수동 Browser 확인:
- <있다면 어느 Screen/URL을 사람이 Vercel Preview 등에서 확인해야 하는지, 없으면 "없음">

다음에 입력할 명령:
- <예: "/run-wave W06 --resume", "/run-wave W07", "docs/preview-checks/SCR-001.md 작성 후 /run-wave W06 재실행">
```

`--status`/`--dry-run`은 위 형식 대신 각각 §2/§4에서 정의한 조회 결과만 출력한다.

## 공통 금지 사항

- 이 명령은 어떤 호출 형태에서도 Git Branch를 새로 만들거나, PR을 생성하거나, Merge를 수행하지 않는다(규칙 6).
- 한 Wave 안에서 여러 Task를 동시에(병렬로) 처리하지 않는다(`docs/DECISION_LOG.md` DEC-011). Task ID 오름차순으로 한 번에 하나씩만 진행한다.
- `Depends On` 순서를 건너뛰고 뒤 순서 Task를 먼저 구현하지 않는다.
- 이전 Wave가 `completed`가 아닌데 다음 Wave를 시작하지 않는다(규칙 1).
- Page Owner가 있는 Wave의 Checkpoint를 사람 확인 없이 임의로 `completed`/확인됨으로 처리하지 않는다(규칙 4·5).
- `BLOCKED_*`나 검증 실패를 만나면 계속 진행하지 않고 그 자리에서 멈춰 보고한다(규칙 2).
- `TASKS/WAVE_PLAN.md`/`TASKS/WAVE_STATE.json`이 없는 상태에서 Wave 구성을 임의로 추측해 만들지 않는다 — 사용자에게 `python scripts/build_waves.py` 실행을 먼저 요청한다.
