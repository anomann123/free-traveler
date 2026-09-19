---
description: TASKS/00_TASK_LIST.md의 각 Task에 대해 1:1 상세 파일을 생성하고 audit_tasks.py로 검증한다
---

`traveler-project-pipeline` Skill을 로드한 뒤 그 규칙에 따라 `TASKS/TASK-<ID>.md` 상세 파일을 생성/갱신한다. `TASKS/00_TASK_LIST.md`가 없으면 먼저 `/gen-tasklist`를 실행하라고 안내하고 중단한다. **이 명령은 `TASKS/TASK-*.md` 계획 문서만 만들며, 소스 코드·마이그레이션·설정 파일 등 실제 구현 코드는 만들지 않는다.**

## 실행 순서

1. `TASKS/00_TASK_LIST.md`를 **실제로 Read**하여 전체 Task ID 목록·각 Task의 필드(Requirement Ref, Screen/Route/Page Entry, Depends On, Expected Files, AC 등)를 확인한다.
2. `TASKS/` 아래 이미 존재하는 `TASK-*.md` 파일 목록을 확인한다. 이미 존재하고 내용이 최신 Task List 행과 일치하는 파일은 건드리지 않는다(Skill §17 — 상세 생성 전 중복 파일을 만들지 않는다).
3. 아직 상세 파일이 없거나 최신 Task List 행과 어긋나는 Task마다 실제 파일 트리를 다시 확인한 뒤(Skill §5), `TASKS/TASK-<TASK-ID>.md`를 Skill §6에 정의된 13개 절 순서(Context, Project Scope, Requirement Ref, Screen / Route / Page Entry, Design Ref, Depends On, Expected Files, Functional AC, Visual AC, Security/Privacy AC, Test Cases, Verify, Definition of Done, Forbidden)로 생성한다.
4. 각 Task의 `Forbidden` 절에 "Expected Files 목록 밖의 파일을 수정하지 않는다"를 항상 포함한다.
5. 모든 상세 파일 생성 후 `python scripts/audit_tasks.py`를 **반드시** 실행한다(이 환경에서 `python3`이 정상 동작하지 않으면 `python`으로 대체하고 그 사실을 보고에 남긴다).
6. 출력이 `AUDIT_FAIL`이면 위반 목록을 그대로 확인하고, 해당 Task 상세만 최소 수정한 뒤 다시 감사를 실행한다 — **위반을 숨기거나 무시하고 통과했다고 보고하지 않는다.** `AUDIT_PASS`가 나올 때까지 이 과정을 반복한다.

## Page Owner(`PAGE-`) Task 전용 필수 AC (Skill §6)

- Screen의 Section 순서와 각 Section 최소 콘텐츠 수(카드/타임라인/갤러리 수 등)를 `design-reference/UI_CONTRACT.md`·`design-reference/D-001/DESIGN.md` §18에서 그대로 옮겨 적는다.
- "큰 빈 영역을 만들지 않는다", "Lorem ipsum/준비 중/정보 확인 필요 금지" 조건을 명시한다.
- 데이터 없음 상태에도 안내 문장+이용 방법+CTA가 있는 완성형 Empty State 조건을 명시한다.
- `PAGE-SCR001`: Next.js Starter 마크업 완전 제거 AC 추가.
- `PAGE-SCR003`: 항공편/숙소/동행 구하기 3탭 실제 조립 + 탭 간 상태 독립 AC 추가.
- `PAGE-SCR005`: Guest/Member/Admin 3개 역할 상태 실제 조립 + 역할에 없는 탭 미노출 AC 추가.
- Page Owner Task 상세는 **Component를 새로 만드는 내용을 담지 않는다** — 이미 완료된 Component를 Page Entry에서 조립하는 것만 범위로 한다(Skill §1-5).

## 금지 사항

- 항공·숙소 입력값을 서버/DB/외부 URL/로그/분석으로 보내는 Acceptance Criteria를 쓰지 않는다 — 오히려 "보내지 않는다"를 AC로 명시한다.
- DB Task 상세에 Skill §3의 6개 테이블 외 테이블을 추가하지 않는다.
- `E2E-` Task 상세에 Chromium 외 브라우저나 시각적 회귀/성능 테스트를 포함하지 않는다.
- 자동 Merge Runner, EC2, AWS 관련 내용을 어떤 Task 상세에도 넣지 않는다.
- EXCLUDED Requirement만으로 구성된 Task 상세 파일을 만들지 않는다(Skill §1-16, §1-18).
- 이 명령 실행 중 `TASKS/*.md` 이외의 파일(소스 코드, 설정 파일 등)을 생성하거나 수정하지 않는다.

## 완료 조건

- `TASKS/00_TASK_LIST.md`의 모든 구현 Task ID에 대해 `TASKS/TASK-<TASK-ID>.md`가 정확히 하나씩 존재한다(1:1).
- `TASKS/`에 Task List에 없는 고아 상세 파일이 없다.
- `python scripts/audit_tasks.py`가 `AUDIT_PASS`로 종료 코드 0을 반환한다. **`AUDIT_FAIL`이면 이 작업을 완료로 보고하지 않는다.**

완료 후 `TASKS/TASK_AUDIT_REPORT.md`의 요약(통과/위반 건수)을 그대로 사용자에게 보고한다.
