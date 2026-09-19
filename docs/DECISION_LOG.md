# Free Traveler — Decision Log

**Document ID:** DECLOG-TRAVEL-001
**목적:** 프로젝트 진행 중 확정된 구조적 결정을 한곳에 고정해, 이후 어떤 문서·Task·구현도 이 결정과 모순되지 않도록 한다. 결정을 변경해야 할 경우 기존 항목을 지우지 않고 새 항목(예: DEC-015)으로 추가하며, 바뀐 이유와 대체 관계를 명시한다.

---

## 요약 표

| ID | 결정 | 상태 | 확정일 | 근거 문서 |
|---|---|---|---|---|
| DEC-001 | 실제 개발 루트는 `traveler/app` | CONFIRMED | 2026-09-13 | 저장소 실측(`pwd`, `package.json`) |
| DEC-002 | 디자인 Screen은 핵심 4개·보조 1개 | CONFIRMED | 2026-09-19 | `docs/03_UI_COVERAGE_ANALYSIS.md`, `design-reference/UI_CONTRACT.md` §0 |
| DEC-003 | `/travel-tools`에 항공·숙소·동행 작성을 통합 | CONFIRMED | 2026-09-19 | `docs/05_UIUX_APPROVED.md` §3, `design-reference/SCREEN_ROUTE_CONTRACT.json` |
| DEC-004 | 여행지·안전·대표는 정적 TypeScript Data | CONFIRMED | 2026-09-19 | `docs/PROJECT_SCOPE.md`(EX-CMS), `docs/ARCHITECTURE.md` §6 |
| DEC-005 | Supabase는 Auth와 동행 기능 중심 | CONFIRMED | 2026-09-19 | `docs/ARCHITECTURE.md` §7 |
| DEC-006 | DB는 6개 Table로 제한 | CONFIRMED | 2026-09-19 | `.claude/skills/traveler-project-pipeline/SKILL.md` §3 |
| DEC-007 | 항공·숙소 입력은 Browser Memory에만 유지 | CONFIRMED | 2026-08-20(SRS) / 2026-09-19(재확인) | `docs/02_SRS_BASELINE.md` CON-01, `docs/ARCHITECTURE.md` §4~5 |
| DEC-008 | Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본 | CONFIRMED | 2026-09-19 | `design-reference/DESIGN_MANIFEST.md`, `design-reference/D-001/DESIGN.md` |
| DEC-009 | Playwright는 Chromium Smoke만 필수 | CONFIRMED | 2026-09-19 | `docs/PROJECT_SCOPE.md` §1-11, `TASKS/00_TASK_LIST.md` §6 |
| DEC-010 | 사용자의 개발 실행 단위는 Wave | CONFIRMED | 2026-09-19 | 본 문서(신규 도입) |
| DEC-011 | Single Agent가 Wave 내부 Task를 순차 수행 | CONFIRMED | 2026-09-19 | 본 문서(신규 도입), `TASKS/00_TASK_LIST.md`(Depends On/Seq 구조) |
| DEC-012 | PR·Merge는 사용자가 수동 수행 | CONFIRMED | 2026-09-19 | `TASKS/TASK-CI-LINT-BUILD.md` Forbidden 절 |
| DEC-013 | EC2·AWS는 사용하지 않음 | CONFIRMED | 2026-09-19 | `docs/PROJECT_SCOPE.md`(EX-OPS), `docs/ARCHITECTURE.md` §10 |
| DEC-014 | 제외 기능은 EXCLUDED로 관리 | CONFIRMED | 2026-09-19 | `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md` §8 |

---

## DEC-001 — 실제 개발 루트는 `traveler/app`

**결정:** Next.js 프로젝트의 실제 루트는 `C:\AI_Service\traveler\app`이며, 이후 모든 문서(`docs/`, `design-reference/`, `TASKS/`, `scripts/`, `.claude/`)는 이 디렉터리를 기준으로 한 상대 경로로 작성한다.

**배경:** 세션 시작 시 `pwd`와 `package.json`을 확인한 결과, Next.js 스캘드(`next`, `react`, `src/app`)가 존재하는 위치가 `traveler` 저장소 최상위가 아니라 그 하위 `app` 디렉터리였다. 이후 작성된 모든 문서·스크립트의 경로 표기(`src/app/page.tsx` 등)는 이 루트를 기준으로 한다.

**영향:** `SCREEN_ROUTE_CONTRACT.json`의 `page_entry`, `scripts/validate_inputs.py`/`scripts/audit_tasks.py`의 `ROOT = Path(__file__).resolve().parent.parent` 계산이 모두 이 루트를 전제한다. 저장소 구조가 바뀌면(예: monorepo 전환) 이 결정을 갱신해야 한다.

---

## DEC-002 — 디자인 Screen은 핵심 4개·보조 1개

**결정:** SRS의 다중 공개 Route를 SCR-001~005 5개 디자인 Screen으로 통합하고, 그중 SCR-001·SCR-003·SCR-004·SCR-005를 **핵심**, SCR-002(대표 소개)를 **보조**로 분류한다.

**배경:** 핵심 4개는 검색·발견(SCR-001), 여행 조건 입력+외부 이동+동행 작성(SCR-003), 동행 조회·참가(SCR-004), 인증·프로필·관리자 게이트(SCR-005)라는 MVP 필수 인터랙션을 직접 수행한다. SCR-002는 정적 정보 제공 화면으로 인터랙션 게이트가 없어 보조로 분류했다.

**영향:** `design-reference/SCREEN_ROUTE_CONTRACT.json`의 `classification` 필드(`core`/`supplementary`), `docs/UI_CONTRACT.md` §0, `docs/ARCHITECTURE.md` §2에 동일하게 반영되어 있다.

---

## DEC-003 — `/travel-tools`에 항공·숙소·동행 작성을 통합

**결정:** 원래 SRS의 `/flights`, `/hotels`, `/mates/new` 3개 별도 Route를 하나의 Screen(SCR-003, Route `/travel-tools`)의 항공편/숙소/동행 구하기 3개 탭으로 통합한다.

**배경:** 세 기능 모두 "조건 입력 → 요약 확인 → 다음 행동(외부 이동 또는 글 작성)"이라는 동일한 상호작용 패턴을 공유하고, 통합 시 Header/Footer·비전달 고지 등 공통 UI를 한 번만 구현하면 된다.

**영향:** 3개 탭의 입력·검증·완료 상태는 서로 완전히 독립적으로 유지해야 한다(`PAGE-SCR003` Functional AC). `docs/05_UIUX_APPROVED.md` §3에 기존 Route → SCR-003 매핑이 기록되어 있다.

---

## DEC-004 — 여행지·안전·대표는 정적 TypeScript Data

**결정:** 여행지(`destination`), 국가 안전정보(`country_safety`), 대표 소개(`representative_profile`) 콘텐츠는 Supabase 테이블이 아니라 `src/data/*.ts` 정적 데이터로 관리한다.

**배경:** Editor/Admin 콘텐츠 CRUD·게시 워크플로(`PROJECT_SCOPE.md` EX-CMS)를 만들지 않기로 한 범위 결정에 따라, 콘텐츠는 저장소에서 직접 파일을 수정하는 방식으로 운영한다.

**영향:** `DATA-DESTINATIONS`/`DATA-SAFETY`/`DATA-REPRESENTATIVE` 세 Task로 구현하며, DB 6개 테이블(DEC-006)에는 이 콘텐츠용 테이블이 포함되지 않는다.

---

## DEC-005 — Supabase는 Auth와 동행 기능 중심

**결정:** Supabase는 이메일 인증(Auth)과 동행(mates) 관련 쓰기 기능에만 사용한다. 여행지·안전·대표 콘텐츠 읽기에는 사용하지 않는다(DEC-004).

**배경:** MVP 범위에서 실제로 서버 상태 변경이 필요한 것은 회원 가입·로그인, 동행 글/참가 요청/차단/신고, 관리자의 신고 처리·외부 URL 설정뿐이다.

**영향:** `docs/ARCHITECTURE.md` §7, DB 6개 테이블(DEC-006)이 전부 이 범위에 속한다.

---

## DEC-006 — DB는 6개 Table로 제한

**결정:** Supabase에는 정확히 `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_url_setting` 6개 테이블만 만든다.

**배경:** DEC-004·DEC-005의 결과로 실제 쓰기 상태가 필요한 도메인이 6개로 확정되었고, 범용 감사 로그·미디어 자산 등 EXCLUDED 기능(DEC-014)을 위한 테이블은 만들지 않는다.

**영향:** `scripts/audit_tasks.py` 검사 #12(DB Table 범위)가 이 6개를 기준선으로 검증하며, 소폭(허용 오차 2개)을 넘는 추가 테이블 언급이 있으면 감사가 실패한다.

---

## DEC-007 — 항공·숙소 입력은 Browser Memory에만 유지

**결정:** 항공·숙소 조건 입력값(국가·지역·출발일/체크인·귀국일/체크아웃)은 Client Component의 로컬 상태로만 유지하며, API·DB·URL 쿼리·서버 로그·분석 이벤트 어디에도 전송하지 않는다.

**배경:** `docs/02_SRS_BASELINE.md` CON-01("항공·호텔 입력값은 브라우저 메모리 상태로만 처리하고 서버 DB·로그·외부 URL에 저장하지 않는다")에서 최초로 확정된 제약이며, 이후 모든 문서에서 그대로 계승했다.

**영향:** `docs/ARCHITECTURE.md` §4~5, `TASKS/TASK-CMP-SCR003-FLIGHT-FORM.md`/`TASK-CMP-SCR003-HOTEL-FORM.md`의 Security/Privacy AC와 Forbidden 절, `scripts/audit_tasks.py` 검사 #13이 이 원칙의 실제 존재 여부를 검증한다.

---

## DEC-008 — Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본

**결정:** `design-reference/vendor/airbnb/DESIGN-airbnb.md`는 레이아웃 문법(카드 밀도, 단일 그림자 티어, 여백 리듬)만 참고하는 vendor 자료로 취급하고, 실제 구현 기준은 `design-reference/D-001/DESIGN.md`(Status: LOCKED)로 한다.

**배경:** Airbnb 참고본의 상표·색상(Rausch)·폰트(Cereal)·워드마크·예약/결제 UI를 그대로 쓰면 상표권·브랜드 혼동 문제가 생긴다. Free Traveler는 코랄(`#F0603F`) 단일 포인트, Inter+OS 기본 한글 폰트 등 독자 토큰 체계를 D-001에 확정했다.

**영향:** `design-reference/DESIGN_MANIFEST.md`가 `Active Design Version: D-001`, `Vendor Reference: .../airbnb/DESIGN-airbnb.md`를 명시적으로 구분해 기록한다. D-001을 변경해야 할 경우 D-001을 직접 덮어쓰지 않고 D-002 등 새 버전 디렉터리를 만든다(`DESIGN_MANIFEST.md` Governance 절).

---

## DEC-009 — Playwright는 Chromium Smoke만 필수

**결정:** Playwright E2E 테스트는 Chromium 프로젝트의 Smoke Test만 구성한다. Firefox·WebKit 프로젝트, 시각적 회귀 테스트, 성능/부하 테스트는 만들지 않는다.

**배경:** MVP 단계에서 크로스 브라우저 회귀·시각적 회귀·부하 테스트까지 구축하는 것은 `PROJECT_SCOPE.md`의 EX-OPS 범위(자동화된 성능·모니터링 파이프라인 제외)와 충돌하며, 핵심 골든 패스 확인에는 단일 브라우저 Smoke로 충분하다고 판단했다.

**영향:** `TASKS/00_TASK_LIST.md` §6에 `E2E-PUBLIC-SMOKE`/`E2E-TRAVEL-TOOLS`/`E2E-MATE-AUTH` 3개 Task만 존재하며, `scripts/audit_tasks.py` 검사 #15·#16이 Chromium 외 브라우저·시각적 회귀·성능 테스트 키워드를 감지하면 실패 처리한다.

---

## DEC-010 — 사용자의 개발 실행 단위는 Wave

**결정:** `TASKS/00_TASK_LIST.md`의 64개 Task를 한 번에 전부 실행하지 않고, 사용자가 지정하는 **Wave** 단위(예: "1차 Wave = 정적 데이터+DB 기반 Task", "2차 Wave = SCR-001 관련 Task" 등 사용자가 그때그때 범위를 정하는 묶음)로 나누어 순차 진행한다.

**배경:** 64개 Task를 동시에 진행하면 검토·롤백 단위가 지나치게 커진다. Wave 단위로 나누면 Depends On 순서를 지키면서도 사용자가 매 단계 결과를 확인하고 다음 Wave 범위를 조정할 수 있다.

**영향:** 이 결정 시점에는 Wave의 구체적 분할표(어떤 Task가 몇 차 Wave에 속하는지)는 아직 확정하지 않았다. Wave 분할이 문서화되면 별도 문서(예: `TASKS/WAVE_PLAN.md`)로 관리하고 이 항목에 참조를 추가한다.

---

## DEC-011 — Single Agent가 Wave 내부 Task를 순차 수행

**결정:** 하나의 Wave 안에서는 여러 에이전트(세션)가 동시에 병렬 작업하지 않고, **하나의 에이전트가 Task List의 Seq·Depends On 순서에 따라 한 번에 하나씩** 순차 수행한다.

**배경:** `TASKS/00_TASK_LIST.md`의 의존 구조(Page Owner는 같은 Screen의 Component Task 전체에 의존, `scripts/audit_tasks.py` 검사 #4 Dependency Cycle 0)는 순차 실행을 전제로 설계되었다. 여러 에이전트가 동시에 같은 파일(`page.tsx`, 공용 컴포넌트 등)을 건드리면 충돌·중복 커밋 위험이 커진다.

**영향:** Wave 실행 시 병렬 Task 분배를 시도하지 않는다. 병렬화가 필요해지면 이 결정을 갱신하고 충돌 방지 전략(파일 단위 분리 등)을 별도로 수립해야 한다.

---

## DEC-012 — PR·Merge는 사용자가 수동 수행

**결정:** GitHub Actions CI(`CI-LINT-BUILD`)는 Lint/Build/Test를 자동 실행하지만, Pull Request 생성 후의 **승인과 Merge는 항상 사용자가 수동으로 수행**한다. 자동 Merge Runner는 구성하지 않는다.

**배경:** 자동 Merge는 검토 없이 변경이 반영될 위험이 있고, `PROJECT_SCOPE.md`의 EX-OPS 범위(무인 자동 Merge Runner 제외)와도 일치한다.

**영향:** `TASKS/TASK-CI-LINT-BUILD.md` Forbidden 절에 "자동 Merge Runner는 만들지 않는다(승인은 사람이 수행)"가 명시되어 있고, `scripts/audit_tasks.py` 검사 #16이 관련 키워드를 감지한다.

---

## DEC-013 — EC2·AWS는 사용하지 않음

**결정:** 인프라는 Vercel(웹 배포)과 Supabase(DB/Auth)로 한정하고, AWS EC2를 포함한 어떤 AWS 리소스도 사용하지 않는다.

**배경:** `PROJECT_SCOPE.md` EX-OPS에서 정한 범위이며, MVP 규모에서 별도 컴퓨트 인프라를 운영할 필요가 없다고 판단했다.

**영향:** `docs/ARCHITECTURE.md` §10, `TASKS/TASK-DEPLOY-VERCEL.md` Functional AC("EC2·AWS 인프라를 만들지 않는다"), `scripts/audit_tasks.py` 검사 #16이 이를 강제한다.

---

## DEC-014 — 제외 기능은 EXCLUDED로 관리

**결정:** 범위에서 제외한 모든 Requirement(REQ-FUNC/REQ-NF)는 삭제하지 않고 **EXCLUDED** 상태로 근거·후속 방향과 함께 계속 추적한다.

**배경:** SRS 원본의 요구사항 번호 체계를 그대로 유지해야 추적성이 끊기지 않는다. 범위 판단이 바뀔 때마다 요구사항을 지우면 왜 빠졌는지 이력이 사라진다.

**영향:** `docs/PROJECT_SCOPE.md`(최초 분류), `docs/UIUX_TRACEABILITY.md`(Implementation Status 열), `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register(Task 미생성 근거), `scripts/audit_tasks.py` 검사 #17·#18이 이 원칙을 기계적으로 검증한다(REQ-FUNC 80개·REQ-NF 34개 전량이 Task 또는 EXCLUDED 표 중 하나에 존재해야 하고, EXCLUDED만으로 구성된 구현 Task는 존재할 수 없다).
