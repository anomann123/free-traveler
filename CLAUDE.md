# CLAUDE.md — Free Traveler

이 파일은 이 저장소(`traveler/app`)에서 작업하는 모든 Agent가 지켜야 할 규칙을 담은 단일 정본이다. 다른 Agent 규칙 파일을 참조하지 않는다 — 필요한 규칙은 전부 이 파일 안에 직접 적혀 있다.

---

## Harness Marker

```
HARNESS_SCHEMA=traveler-screen-route-v1
DESIGN_PATH=design-reference/D-001/DESIGN.md
SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json
PROJECT_SCOPE=docs/PROJECT_SCOPE.md
PLAYWRIGHT_ENABLED=true
PLAYWRIGHT_SCOPE=chromium-smoke
AUTO_MERGE=false
AWS_ENABLED=false
```

---

## 필수 규칙 (전부 강제)

1. **작업 전 `package.json`과 현재 Next.js 문서를 확인한다.** 버전을 가정하지 않는다.
2. **SRS 정본은 `docs/06_SRS_UIUX_REVISED.md`다.** 요구사항 원문·Route 통합 매핑이 다른 문서와 다르면 이 문서를 우선한다.
3. **Scope 분류 정본은 `docs/PROJECT_SCOPE.md`다.** 어떤 Requirement가 IMPLEMENT/EXCLUDED인지는 이 문서 기준이다.
4. **디자인 정본은 `design-reference/D-001/DESIGN.md`다.** `design-reference/vendor/airbnb/DESIGN-airbnb.md`는 레이아웃 문법 참고용일 뿐 색상·폰트·상표를 그대로 쓰지 않는다.
5. **Screen 정본은 `design-reference/SCREEN_ROUTE_CONTRACT.json`이다.** Route·Page Entry가 다른 서술과 다르면 이 JSON을 우선한다.
6. **`/run-wave WXX`를 표준 개발 명령으로 사용한다.** 이 명령 없이 임의로 여러 Task를 한꺼번에 시작하지 않는다.
7. **Wave 내부 Task를 Depends On 순서로 한 번에 하나만 구현한다.** 병렬로 여러 Task를 동시에 열지 않는다.
8. **현재 Task의 Expected Files 밖 파일은 수정하지 않는다.** 다른 파일을 고쳐야 할 필요가 보이면 별도로 보고하고 현재 Task 범위를 넘기지 않는다.
9. **Page Owner Task는 Page Entry에서 Component를 실제 조립한다.** Page Owner Task 안에서 새 Component를 만들지 않는다(Component는 별도 Component Task의 책임).
10. **SCR-001 완료 시 Next.js Starter를 제거한다.** `create-next-app` 기본 로고·문구·링크가 남아 있으면 완료로 보지 않는다.
11. **SCR-003은 항공·숙소·동행 탭을 모두 조립한다.** 하나라도 자리표시자로 남기지 않는다.
12. **항공·숙소 입력값은 서버·DB·URL·로그·분석으로 보내지 않는다.** Client Component의 일시 상태로만 유지한다.
13. **Supabase 쓰기는 Auth·동행·신고·설정 범위로 제한한다.** 여행지·안전·대표 콘텐츠에 Supabase 쓰기를 추가하지 않는다(정적 Data 사용, 규칙 16).
14. **RLS를 우회하는 Client 코드를 작성하지 않는다.** 클라이언트에서 RLS 정책을 무력화하는 조건이나 우회 쿼리를 만들지 않는다.
15. **Service Role Key를 Client에서 사용하지 않는다.** `NEXT_PUBLIC_` 접두어가 붙은 환경변수에 Service Role Key를 넣지 않는다.
16. **여행지·안전·대표는 정적 Data를 사용한다.** `src/data/*.ts`로만 관리하고 이 콘텐츠를 위한 DB 테이블이나 CRUD 화면을 만들지 않는다.
17. **Prisma·ORM·AWS·EC2를 추가하지 않는다.** Supabase JS 클라이언트를 직접 사용하고, 인프라는 Vercel+Supabase로 한정한다.
18. **Playwright는 핵심 Smoke만 작성한다.** Chromium 프로젝트 외 브라우저, 시각적 회귀, 성능 테스트를 추가하지 않는다.
19. **EXCLUDED 기능을 임의로 구현하지 않는다.** `docs/PROJECT_SCOPE.md`/`docs/UIUX_TRACEABILITY.md`/`TASKS/00_TASK_LIST.md`의 NON_IMPLEMENTATION Register에 있는 항목은 사용자가 명시적으로 범위를 바꾸기 전까지 구현하지 않는다.
20. **destructive Git 명령을 임의로 사용하지 않는다.** `git reset --hard`, `git push --force`, `git clean -fd`, 브랜치 강제 삭제 등은 사용자가 명시적으로 요청한 경우에만 사용한다.
21. **자동 PR·자동 Merge를 실행하지 않는다.** PR 생성은 요청받았을 때만 하고, Merge는 항상 사람이 수행한다(`AUTO_MERGE=false`).
22. **사람의 Preview 확인 후 다음 화면 Wave로 진행한다.** 한 Wave의 Page Owner Task가 끝나면 사용자가 Vercel Preview 등에서 실제로 확인하기 전에는 다음 Screen의 Wave를 시작하지 않는다.
23. **작업 완료 시 변경 파일·검증 결과·남은 제한사항을 보고한다.** "완료했습니다"만 말하지 않고 무엇을 바꿨는지, 무엇을 확인했는지, 아직 안 된 것은 무엇인지 함께 보고한다.

---

## Task 완료 순서

모든 Task는 다음 순서를 따른다. 순서를 건너뛰거나 뒤바꾸지 않는다.

1. **Task 읽기** — 해당 `TASKS/TASK-<ID>.md`의 Context/Requirement Ref/Depends On/Expected Files/AC/Forbidden을 전부 읽는다.
2. **입력 확인** — Depends On의 선행 Task가 실제로 완료되어 있는지, 참조하는 디자인·계약 문서(§Harness Marker)가 최신인지 확인한다.
3. **구현** — Expected Files 안에서만 코드를 작성/수정한다.
4. **관련 포맷·Unit Test** — 해당 코드에 관련된 포맷(lint/format)과 Unit Test(있다면)를 실행하고 통과시킨다.
5. **필요 시 Playwright** — 해당 Task가 Playwright Smoke 대상이면 Chromium 범위로 실행한다.
6. **Diff 확인** — 실제 변경된 파일이 Expected Files와 일치하는지 diff로 확인한다.
7. **완료 보고** — 변경 파일 목록, 검증 결과(테스트 통과 여부 등), 남은 제한사항을 보고한다.
