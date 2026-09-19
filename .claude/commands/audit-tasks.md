---
description: TASKS/00_TASK_LIST.md와 TASKS/TASK-*.md를 traveler-project-pipeline 규칙(18개 검사)으로 감사한다
---

`traveler-project-pipeline` Skill을 로드한 뒤, 생성된 Task List와 Task 상세를 재검증할 때 사용한다. Task를 새로 만들거나 구현 코드를 작성하지 않고 **기존 산출물만 검사**한다.

## 실행 순서

1. `python scripts/audit_tasks.py`를 실행한다(`python3`이 이 환경에서 정상 동작하지 않으면 `python`으로 대체 실행하고 그 사실을 보고에 남긴다). 이 스크립트는 `TASKS/00_TASK_LIST.md`, `TASKS/TASK-*.md`, `docs/PROJECT_SCOPE.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`을 **실제로 읽어** 18개 항목을 검사하고 `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK_AUDIT_REPORT.md`를 생성한다.
2. `TASKS/00_TASK_LIST.md` 또는 `TASKS/TASK-*.md`가 없으면 스크립트가 그 사실을 보고한다(종료 코드 1) — 이 경우 `/gen-tasklist`와 `/gen-task-details`를 먼저 실행하라고 안내하고 종료한다.
3. 결과가 `AUDIT_FAIL`이면 위반 목록을 요약 없이 그대로 사용자에게 전달한다. **위반이 없다고 임의로 재작성하거나, 실패를 무시한 채 완료로 보고하지 않는다.**
4. 결과가 `AUDIT_PASS`이면 통과한 검사 수(예: `AUDIT_PASS 18/18`)와 `TASKS/TASK_AUDIT_REPORT.md` 경로를 사용자에게 보고한다.
5. 사용자가 위반 수정을 요청하면 `traveler-project-pipeline` Skill §1의 해당 규칙 번호를 인용해 어떤 Task 상세를 최소 수정해야 하는지 안내한다(직접 수정은 `/gen-task-details` 재실행 또는 개별 편집으로 처리하며, 이 명령 자체는 수정하지 않는다).

## 이 명령이 하지 않는 것

- Task List나 Task 상세 파일을 새로 생성하지 않는다(그 책임은 `/gen-tasklist`, `/gen-task-details`에 있다).
- `TASKS/*.md`, `TASKS/TASK_MANIFEST.csv`, `TASKS/TASK_AUDIT_REPORT.md` 외의 파일을 만들거나 수정하지 않는다 — 구현 코드를 작성하지 않는다.
- 감사를 통과시키기 위해 검증 로직(스크립트)을 완화하지 않는다.
- `AUDIT_FAIL`을 발견했는데도 "문제 없음"으로 보고하지 않는다.
