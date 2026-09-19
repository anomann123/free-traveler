---
description: prepare-task가 READY_TO_IMPLEMENT를 반환한 Task 하나를 Expected Files 안에서만 구현한다
---

`traveler-project-pipeline` Skill을 로드해 이 저장소의 공통 제약(§3 DB 6개 테이블, §1의 금지 인프라 목록 등)을 확인한 뒤 이 명령을 실행한다. 이 명령은 **Task 하나만** 구현한다 — 여러 Task를 한 번에 처리하지 않는다.

## 0. 착수 전제

1. 이번 세션에서 이 `TASK_ID`에 대해 `/prepare-task`를 실행해 `READY_TO_IMPLEMENT`를 받았는지 확인한다. 받지 않았거나 오래되었으면(그 사이 다른 파일이 바뀌었을 수 있음) **먼저 `/prepare-task WAVE_ID TASK_ID`를 실행**하고, 그 결과가 `READY_TO_IMPLEMENT`가 아니면 이 명령을 진행하지 않고 해당 `BLOCKED_*` 상태와 이유를 그대로 보고한 뒤 중단한다.
2. `TASKS/TASK-<TASK_ID>.md`를 처음부터 끝까지 다시 읽는다(요약이나 이전 대화 기억으로 대체하지 않는다).

## 1. 구현 범위 — Expected Files 안에서만 작업

- `TASKS/TASK-<TASK_ID>.md`의 `Expected Files` 목록에 있는 파일만 생성·수정한다.
- 구현 중 그 목록 밖의 파일을 고쳐야 할 필요가 발견되면(예: 공용 타입 정의 누락) **직접 확장하지 말고** 작업을 멈추고 사용자에게 "Expected Files 확장이 필요하다"고 보고한다 — Task 상세를 스스로 다시 쓰지 않는다.
- "신규 생성"으로 표시된 파일은 새로 만들고, "기존 파일 수정"으로 표시된 파일만 편집한다(그 외 기존 파일에 손대지 않는다).

## 2. AC(Functional/Visual/Security) 충족

- `Functional AC`, `Visual AC`, `Security/Privacy AC`의 각 항목을 구현이 끝나는 대로 하나씩 충족시키고, 충족 여부를 스스로 점검한다(체크박스 형식이면 실제로 만족하는 항목만 완료로 간주한다).
- AC 중 하나라도 이 Task의 Expected Files만으로는 충족할 수 없는 것이 드러나면(예: 의존 데이터가 아직 없음) 구현을 멈추지 말고 나머지 AC를 진행하되, 완료 보고(§8)에서 "충족하지 못한 AC"로 명시한다 — 충족한 것처럼 보고하지 않는다.
- `Forbidden` 절에 적힌 항목은 절대 만들지 않는다.

## 3. Page Owner Task — 조립만, 신규 Component 금지

- Category가 `PAGE`인 Task는 해당 Screen의 Page Entry(`page.tsx`)에서 **이미 완료된 Component를 import해 실제로 조립하는 것**만 한다.
- 이 과정에서 새 Component 파일을 만들지 않는다. 조립에 필요한 Component가 아직 없다면(즉 그 Component Task가 완료되지 않았다면) 이는 `/prepare-task`의 Depends On 검사를 통과하지 못했어야 할 상황이므로, 구현을 진행하지 말고 그 사실을 보고하고 중단한다.
- `PAGE-SCR001`은 `create-next-app` 기본 Starter 마크업(로고, 기본 문구, 기본 링크)을 이 시점에 완전히 제거한다.
- `PAGE-SCR003`은 항공/숙소/동행 구하기 3개 탭이 전부 실제 콘텐츠로 연결되어 있는지 확인한다(하나라도 자리표시자면 미완료로 보고한다).
- `PAGE-SCR005`는 Guest/Member/Admin 역할별 조립과 "역할에 없는 탭은 렌더링하지 않음"을 확인한다.

## 4. Unit Test 실행

- 이 Task와 관련된 Unit Test(`UNIT-*` Task, 예: 날짜 검증·연락처 탐지·모집글 상태 전이)가 존재하면 실행한다. 아직 테스트 러너(Vitest)가 설치되어 있지 않으면 설치가 이 Task의 Expected Files 범위에 포함되는지 확인하고, 범위 밖이면 그 사실을 제약사항으로 보고한다(§8).
- 이 Task 자체가 `UNIT-` Task라면 그 테스트 파일을 작성/실행하는 것이 곧 구현이다.
- 관련 없는 Unit Test 전체 스위트를 억지로 통과시키려 하지 않는다 — 이 Task 범위의 테스트만 확인한다.

## 5. Playwright Smoke — Page Owner·E2E Task일 때만

- 이 Task의 Category가 **`PAGE` 또는 `E2E`일 때만** 관련 Playwright Chromium Smoke를 실행한다.
  - `PAGE-*` Task 완료 후에는 `TASKS/00_TASK_LIST.md`에서 이 Screen에 의존하는 `E2E-*` Task를 찾아 그 Smoke를 실행한다(예: `PAGE-SCR001` → `E2E-PUBLIC-SMOKE`).
  - `E2E-*` Task 자체를 구현할 때는 해당 Smoke 파일을 Chromium 프로젝트로 실행한다.
- 그 외 Category(`CMP`/`DATA`/`DB`/`AUTH`/`UNIT`/`TEST`/`CI`/`DEPLOY`)에서는 Playwright를 실행하지 않는다.
- Firefox·WebKit 프로젝트, 시각적 회귀, 성능 테스트는 어떤 경우에도 추가하거나 실행하지 않는다.

## 6. 금지 사항 (예외 없음)

- **AWS·EC2**를 추가하지 않는다(인프라는 Vercel+Supabase로 한정).
- **ORM(Prisma 등)**을 추가하지 않는다. Supabase JS 클라이언트를 직접 사용한다.
- **자동 Merge** 관련 코드·워크플로(예: auto-merge GitHub Action, Merge Queue 자동 승인)를 추가하지 않는다.
- 그 외 이 Task의 `Forbidden` 절, `docs/PROJECT_SCOPE.md`의 EXCLUDED 항목, `docs/ARCHITECTURE.md` §10(CMS·외부 이메일 공급자·Monitoring 제외)도 함께 지킨다.
- 항공·숙소 입력값을 서버·DB·URL·로그·분석으로 보내는 코드를 작성하지 않는다(Client 일시 상태로만 유지).
- Service Role Key를 `NEXT_PUBLIC_` 환경변수나 Client Component에 노출하지 않는다.

## 7. Diff 확인

구현이 끝나면 `git status`/`git diff`로 실제 변경 파일 목록을 확인하고, Expected Files 목록과 정확히 일치하는지 대조한다. 목록 밖의 파일이 바뀌어 있으면 완료 보고 전에 원인을 확인하고(의도치 않은 변경이면 되돌리고) 보고서에 그 경위를 남긴다.

## 8. 완료 보고 (필수 형식)

```
TASK_ID: <ID>
상태: 완료 | 부분 완료(사유)

변경 파일:
- <path> (신규 생성 | 수정)

검증 결과:
- Unit Test: <실행한 파일과 결과, 또는 "해당 없음">
- Playwright Smoke: <실행 여부와 결과, 또는 "이 Task 범위 아님(Category=...)">
- AC 충족 여부: <Functional/Visual/Security AC 중 충족/미충족 항목>

남은 제약사항:
- <예: 환경변수 미설정으로 실제 Supabase 연결 미검증, 의존 라이브러리 미설치 등>
```

"완료했습니다"만 말하지 않는다. 무엇을 바꿨는지, 무엇을 확인했는지, 아직 안 되는 것은 무엇인지 항상 함께 보고한다(`CLAUDE.md` 규칙 23).

## 9. Commit·Push·PR

- 이 명령은 **기본적으로 Commit·Push·PR을 자동 수행하지 않는다.** 구현 산출물을 워킹 트리에 남긴 채 완료 보고로 끝낸다.
- 사용자가 명시적으로 요청한 경우에만, 이 Task의 Expected Files만 스테이징한 **Task 단위 Commit 하나**까지 수행할 수 있다(`git add <Expected Files>` → `git commit`). 이때도 Push나 PR 생성은 별도로 요청받지 않는 한 수행하지 않는다.
- Commit 메시지에는 `TASK_ID`와 한 줄 요약을 포함한다.
