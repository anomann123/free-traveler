---
description: 특정 Wave·Task의 착수 가능 여부를 8개 항목으로 점검하고 READY_TO_IMPLEMENT/BLOCKED_* 상태를 보고한다(코드 수정 없음)
---

`traveler-project-pipeline` Skill을 로드한 뒤 이 명령을 실행한다. **이 명령은 어떤 코드·설정 파일도 수정하지 않는다.** `TASKS/00_TASK_LIST.md`, `TASKS/TASK-<ID>.md`, 그 밖의 참조 문서를 읽고 상태만 판정해 보고한다.

## 입력

- `WAVE_ID` — 사용자가 지정한 Wave 식별자(예: `W01`). 인자로 주어지지 않으면 사용자에게 물어본다.
- `TASK_ID` — 점검할 Task ID(예: `PAGE-SCR001`, `CMP-SCR003-FLIGHT-FORM`). 인자로 주어지지 않으면 사용자에게 물어본다.
- 선택된 상세 Task 파일 — `TASKS/TASK-<TASK_ID>.md`. `TASK_ID`로부터 경로를 유도한다.

두 인자 중 하나라도 없으면 다른 검사를 시작하지 말고 즉시 `BLOCKED_INPUT`으로 보고한다.

## 검사 8개 (순서대로 전부 수행)

### 1. Working Tree 상태
`git status --porcelain`을 실행한다.
- 이 저장소가 아직 Git 저장소가 아니거나 명령이 실패하면: "Working Tree 상태를 확인할 수 없음"으로 기록하고 이 검사를 **통과로 간주하지 않는다**(→ `BLOCKED_INPUT` 후보).
- 변경 사항이 있는데 그 파일들이 전부 이번 `TASK_ID`의 Expected Files(검사 4)에 속하면 통과로 본다(이전 시도의 부분 작업으로 간주).
- Expected Files 밖의 파일에 추적되지 않은 변경이 있으면 `BLOCKED_DIRTY_TREE` 후보로 기록한다.

### 2. Task가 현재 Wave에 포함되는지
- `TASKS/00_TASK_LIST.md`에서 `TASK_ID`가 실제로 존재하는지 확인한다. 없으면 `BLOCKED_INPUT`.
- Wave-Task 매핑을 관리하는 문서(예: `TASKS/WAVE_PLAN.md`)가 저장소에 있으면 그 문서에서 `WAVE_ID`에 `TASK_ID`가 포함되는지 확인한다.
- 그런 문서가 아직 없으면(2026-09-19 기준 이 저장소에는 없음), Wave 분할은 아직 문서화되지 않은 상태다(`docs/DECISION_LOG.md` DEC-010 참조). 이 경우 **사용자가 이번 대화에서 직접 지정한 Wave-Task 매핑**만 근거로 인정하고, 그 근거가 없거나 모호하면 `BLOCKED_INPUT`으로 보고하며 "Wave 분할표가 아직 없어 이 Task가 해당 Wave에 속하는지 문서로 확인할 수 없다"고 명시한다 — 임의로 포함된다고 가정하지 않는다.

### 3. Depends On 완료 여부
`TASKS/TASK-<TASK_ID>.md`의 `Depends On` 절에 나열된 각 Task ID에 대해:
- 그 Task의 `TASKS/TASK-<의존 ID>.md`를 열어 `Expected Files`를 확인한다.
- "신규 생성" 파일이 실제로 저장소에 존재하고 내용이 placeholder가 아니면 완료로 간주한다. "기존 파일 수정"인 경우, 현재 파일 내용이 그 Task의 Functional AC를 충족하는 것으로 보이면 완료로 간주한다.
- 이 휴리스틱은 완벽하지 않다(공식 완료 기록 파일이 아직 없음). 판단이 애매하면 완료로 단정하지 말고 사용자에게 "이 의존 Task가 완료되었는지 확인해 달라"고 명시적으로 묻는다.
- 하나라도 미완료이거나 확인 불가면 `BLOCKED_DEPENDENCY`.

### 4. Expected Files
- `TASKS/TASK-<TASK_ID>.md`의 `Expected Files` 목록을 그대로 추출해 보고서에 옮긴다.
- 각 경로가 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `page_entry`(Page Owner Task인 경우)와 일치하는지 대조한다.
- 각 파일의 실제 존재 여부(신규 생성 대상인지 기존 수정 대상인지)를 다시 확인해 Task 상세 설명과 어긋나면 그 사실을 보고서에 남긴다(치명적 차단은 아니며 구현자가 참고할 정보).

### 5. SRS·Scope·Design·Screen Ref
- `TASKS/TASK-<TASK_ID>.md`의 `Requirement Ref`에 나열된 각 ID가 `docs/06_SRS_UIUX_REVISED.md`/`docs/PROJECT_SCOPE.md`에 실제로 존재하는지 확인한다.
- `Design Ref`에 인용된 절 번호(`design-reference/D-001/DESIGN.md` §N)가 실제로 그 문서에 존재하는지 확인한다.
- `Screen / Route / Page Entry`가 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 해당 Screen 정의와 일치하는지 확인한다.
- 불일치가 있으면 `BLOCKED_INPUT`으로 기록하고 구체적으로 어떤 참조가 어긋나는지 남긴다.

### 6. 필요한 환경변수 이름
- Task의 `Expected Files`/`Functional AC`/`Security/Privacy AC` 내용을 훑어 Supabase, 외부 URL(항공·숙소), 인증 등과 관련된 항목이면 `docs/ARCHITECTURE.md` §11.3의 환경변수 목록(`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `FLIGHT_OUTBOUND_URL`, `HOTEL_OUTBOUND_URL`) 중 이 Task에 필요한 이름만 골라 보고서에 나열한다.
- 이 검사는 **정보 제공용**이다 — 로컬에 `.env.local`이 없어 값이 비어 있다는 사실만으로 착수를 차단하지 않는다(값 설정은 구현 단계의 몫). 다만 이름조차 특정할 수 없을 만큼 Task 설명이 불충분하면 `BLOCKED_INPUT`으로 기록한다.

### 7. Secret 하드코딩 위험
- Expected Files 중 이미 존재하는 파일이 있으면 그 내용을 읽어 다음과 같은 패턴을 훑는다: `sk-`로 시작하는 문자열, `SUPABASE_SERVICE_ROLE`이 문자열 리터럴로 박혀 있는 경우, `NEXT_PUBLIC_`이 아닌 비밀 키가 클라이언트 파일(`"use client"` 또는 `src/app/**/page.tsx`)에 리터럴로 등장하는 경우, 30자 이상의 영숫자 토큰이 따옴표 안에 그대로 들어있는 경우.
- 하나라도 발견되면 `BLOCKED_INPUT`으로 기록하고("Secret 하드코딩 위험") 위치를 남긴다 — 이 명령은 코드를 고치지 않으므로 직접 제거하지 않는다.
- 발견되지 않으면 통과로 기록한다(아직 코드가 없는 Task라면 "해당 없음 — 아직 파일 없음"으로 남긴다).

### 8. EXCLUDED 범위 침범 여부
- `TASKS/TASK-<TASK_ID>.md`의 `Requirement Ref`에 있는 모든 ID를 `docs/PROJECT_SCOPE.md`의 상태와 대조한다.
- 하나라도 `EXCLUDED`면 `BLOCKED_SCOPE`로 기록한다(`scripts/audit_tasks.py` 검사 #18과 동일한 원칙 — EXCLUDED Requirement만으로 이루어진 Task는 애초에 존재해서는 안 되지만, 혼합된 경우도 착수 전에 반드시 표시한다).
- Functional AC나 Expected Files가 `docs/PROJECT_SCOPE.md` §3(EX-CMS/EX-MEDIA/EX-AUDIT/EX-OPS/EX-EMAIL)에 명시된 제외 범위(Editor/Admin CRUD, 미디어 업로드 승인, 범용 감사 로그, 자동 백업/모니터링, 외부 이메일 발송 등)를 침범하는 내용을 포함하면 마찬가지로 `BLOCKED_SCOPE`.

## 출력 상태 판정 순서

검사를 전부 수행한 뒤, 아래 우선순위로 **하나의 상태**만 최종 보고한다(여러 항목이 동시에 걸려도 가장 우선순위가 높은 것 하나만 출력하되, 나머지 위반도 보고서 본문에는 전부 남긴다).

1. **BLOCKED_INPUT** — WAVE_ID/TASK_ID 누락, Task 미존재, Wave 소속 미확인, 참조 문서 불일치, 환경변수 이름조차 특정 불가, Secret 하드코딩 위험 발견 중 하나라도 해당(검사 1[확인 불가 포함]·2·5·6·7).
2. **BLOCKED_DIRTY_TREE** — Expected Files 밖에 추적되지 않은 변경이 있음(검사 1).
3. **BLOCKED_DEPENDENCY** — Depends On 중 미완료/확인 불가 존재(검사 3).
4. **BLOCKED_SCOPE** — EXCLUDED Requirement 연결 또는 제외 범위 침범(검사 8).
5. **READY_TO_IMPLEMENT** — 위 네 가지 어디에도 해당하지 않음. 검사 4·6의 정보는 참고용으로 보고서에 포함하되 착수를 막지 않는다.

## 보고 형식

다음을 반드시 포함해 보고한다:

```
WAVE_ID: <입력값>
TASK_ID: <입력값>
상태: READY_TO_IMPLEMENT | BLOCKED_INPUT | BLOCKED_DEPENDENCY | BLOCKED_DIRTY_TREE | BLOCKED_SCOPE

1. Working Tree: <통과/문제 내용>
2. Wave 소속: <통과/문제 내용>
3. Depends On: <목록과 각각의 완료 여부>
4. Expected Files: <목록>
5. SRS·Scope·Design·Screen Ref: <통과/불일치 내용>
6. 필요한 환경변수: <목록 또는 "해당 없음">
7. Secret 하드코딩 위험: <통과/발견 내용>
8. EXCLUDED 범위 침범 여부: <통과/침범 내용>
```

`BLOCKED_*` 상태를 보고할 때는 무엇을 해결해야 `READY_TO_IMPLEMENT`가 되는지 한 줄로 함께 안내한다. 이 명령은 여기서 끝난다 — 문제를 발견했다고 해서 스스로 고치거나 다음 단계(구현)로 넘어가지 않는다.
