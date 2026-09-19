# Free Traveler — Architecture

**Document ID:** ARCH-TRAVEL-001
**기반 문서:** `package.json`, `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `TASKS/TASK_MANIFEST.csv`
**목적:** Traveler 구현이 지켜야 할 기술 경계(무엇을 쓰고, 무엇을 쓰지 않는지)를 한 문서로 고정한다. 여기 적힌 경계와 다른 방식으로 구현하지 않는다.

---

## 1. 스택 개요

| 계층 | 기술 | 비고 |
|---|---|---|
| 프레임워크 | **Next.js App Router**(`next@16.3.4`) | `package.json` 확인 완료. Pages Router 사용 금지 |
| 언어 | **TypeScript**(`typescript@^5`) | `.ts`/`.tsx`만 사용, `.js` 신규 작성 금지 |
| UI | React 19 + Tailwind CSS 4 | `@tailwindcss/postcss` 이미 설치됨 |
| 데이터베이스 | Supabase PostgreSQL | §7 참조, ORM 없이 Supabase 클라이언트로 직접 접근 |
| 정적 데이터 | `src/data/*.ts` | §6 참조 |
| 테스트 | Vitest(단위) + Playwright(Chromium E2E Smoke) | §9 참조, 둘 다 아직 미설치 |
| CI/CD | GitHub Actions + Vercel Preview | §10 참조 |
| **미사용** | Prisma/ORM, EC2, AWS, 자동 Merge Runner, CMS, 외부 이메일 공급자, 모니터링 SaaS | §11 참조 |

---

## 2. 화면·Route 구성 — 핵심 4 · 보조 1

`design-reference/SCREEN_ROUTE_CONTRACT.json`(`schema_version: traveler-screen-route-v1`)이 정본이다. 5개 Screen 외 신규 Route를 임의로 추가하지 않는다.

| Screen | 분류 | Route | Page Entry |
|---|---|---|---|
| SCR-001 메인 | **핵심** | `/` | `src/app/page.tsx` |
| SCR-002 대표 소개 | **보조** | `/about` | `src/app/about/page.tsx` |
| SCR-003 통합 여행 준비 | **핵심** | `/travel-tools` | `src/app/travel-tools/page.tsx` |
| SCR-004 동행 조회 | **핵심** | `/mates` | `src/app/mates/page.tsx` |
| SCR-005 계정·관리 | **핵심** | `/account` | `src/app/account/page.tsx` |

**핵심 4(SCR-001, 003, 004, 005)**는 검색·발견, 여행 조건 입력+외부 이동+동행 작성, 동행 조회·참가, 인증·프로필·관리자 게이트라는 MVP 필수 인터랙션을 직접 수행한다. **보조 1(SCR-002)**은 정적 정보 제공 화면으로 인터랙션 게이트를 갖지 않는다.

기술 Route(`/auth/callback`, `/api/*`, `not-found.tsx`)는 위 5개 Screen에 포함되지 않는 별도 구현 대상이다(Screen 수에 포함하지 않음).

---

## 3. Server Component / Client Component 경계

Next.js App Router 기본값은 **Server Component**다. 아래 표에 해당하는 것만 파일 최상단에 `"use client"`를 선언한다.

| 구분 | 대상 | 이유 |
|---|---|---|
| **Server Component(기본)** | 5개 `page.tsx` 최상위, 정적 콘텐츠 렌더링(SCR-001 카드 그리드, SCR-002 전체, SCR-004 목록 초기 렌더), `src/data`를 읽어 서버에서 마크업을 만드는 모든 구간 | 데이터 fetch·정적 렌더는 클라이언트 JS 번들에 포함할 필요가 없음 |
| **Client Component(`"use client"`)** | 검색창·필터 상태(SCR-001), 여행지·안전정보 Drawer 열림 상태, **항공·숙소 입력 Form 전체**(SCR-003), 탭 전환 상태(SCR-003/005), 참가 신청·신고 Form(SCR-004), 로그인 Form과 역할별 탭 상태(SCR-005), 즐겨찾기 토글(`localStorage`), 전역 Toast | `useState`/`useEffect`/이벤트 핸들러/브라우저 API(`localStorage`, `window.open`)가 필요한 지점만 |
| **Server Action / Route Handler** | 동행 글·참가 요청·차단·신고·프로필 CRUD(Supabase 접근), 인증 콜백 | DB 접근은 서버 경계에서만 수행하고 클라이언트에 Supabase Service Role 키를 노출하지 않는다 |

**원칙:** Client Component는 상호작용이 필요한 최소 leaf 노드에만 적용하고, `page.tsx` 전체를 Client Component로 만들지 않는다.

---

## 4. 항공·숙소 입력 폼 — Client 일시 상태 전용

- `CMP-SCR003-FLIGHT-FORM`, `CMP-SCR003-HOTEL-FORM`은 **Client Component**이며, 국가·지역·출발일(체크인)·귀국일(체크아웃) 값을 오직 컴포넌트 로컬 상태(`useState`)로만 보관한다.
- 이 값은 브라우저 세션 동안(페이지 새로고침 전까지)만 유지되는 **일시 상태**다. `localStorage`/`sessionStorage`에도 저장하지 않는다(즐겨찾기 기능과 달리 영속화 대상이 아니다).
- 요약 확인 후 외부 이동은 사전에 관리자가 설정한 `FLIGHT_OUTBOUND_URL`/`HOTEL_OUTBOUND_URL`을 그대로 새 탭(`target="_blank" rel="noopener noreferrer"`)으로 열며, 입력값을 그 URL에 쿼리 파라미터로 붙이지 않는다.

## 5. 항공·숙소 입력값 미전송 원칙

항공·숙소 조건 입력값은 다음 어디로도 전송하지 않는다:

- **API**: Route Handler/Server Action 호출 없음(이 두 Form에는 서버 엔드포인트가 존재하지 않는다)
- **DB**: Supabase 테이블에 저장하지 않는다(§7의 6개 테이블 중 항공·숙소 입력을 위한 테이블은 없다)
- **URL**: 외부 이동 URL, 내부 라우팅 URL 어디에도 쿼리 파라미터로 포함하지 않는다
- **로그**: `console.log`, 서버 로그, 분석 이벤트(`window.gtag` 등)에 원시 입력값을 남기지 않는다

이 원칙은 `CMP-SCR003-FLIGHT-FORM`/`CMP-SCR003-HOTEL-FORM`/`PAGE-SCR003`의 Forbidden 절에 이미 명시되어 있으며(`TASKS/TASK-CMP-SCR003-FLIGHT-FORM.md` 등), 코드 리뷰 시 네트워크 탭·서버 로그 확인으로 검증한다.

---

## 6. 정적 데이터 — `src/data`

여행지·국가 안전정보·대표 소개 콘텐츠는 **데이터베이스가 아니라 정적 TypeScript 데이터**로 관리한다.

| 파일 | 내용 | 근거 Task |
|---|---|---|
| `src/data/destinations.ts` | 국내 10곳 이상·해외 15개국 30개 도시 이상 | `DATA-DESTINATIONS` |
| `src/data/country-safety.ts` | 소개 해외국가 전원 안전정보(8개 카테고리) | `DATA-SAFETY` |
| `src/data/representative.ts` | `free_traveler` 소개·철학·Timeline·방문국가·Gallery | `DATA-REPRESENTATIVE` |

이 세 파일은 Editor/Admin CRUD 화면 없이 저장소에서 직접 수정한다(`PROJECT_SCOPE.md` EX-CMS). 현재 `src/data` 디렉터리 자체가 아직 없다(§12 착수 차단 참조).

---

## 7. Supabase — Auth와 동행 기능 중심

Supabase는 **인증(Auth)과 동행(mates) 관련 기능에만** 사용한다. 여행지·안전정보·대표 소개는 §6에 따라 Supabase를 거치지 않는다.

### 7.1 DB Table (정확히 6개, 그 이상 만들지 않음)

| # | 테이블 | 용도 | 근거 Task |
|---|---|---|---|
| 1 | `user_profile` | 닉네임·연령대·성별·여행 스타일·성인 확인 상태 | `DB-SCHEMA-BASE` |
| 2 | `mate_post` | 동행 모집글 | 〃 |
| 3 | `mate_application` | 참가 요청 | 〃 |
| 4 | `user_block` | 사용자 차단 관계 | 〃 |
| 5 | `report` | 신고 접수·상태 | 〃 |
| 6 | `outbound_url_setting` | 관리자가 설정하는 항공·숙소 외부 URL(HTTPS만) | 〃 |

### 7.2 Browser / Server Supabase Client 분리

| Client | 위치 | 사용처 |
|---|---|---|
| Browser Client | `src/lib/supabase/client.ts` | Client Component에서 로그인 상태 구독, 세션 갱신 등 브라우저 전용 동작 |
| Server Client | `src/lib/supabase/server.ts` | Server Component/Server Action/Route Handler에서 쿠키 기반 세션으로 DB 접근 |

Service Role 키(있다면)는 서버 전용 코드에서만 읽고 클라이언트 번들에 절대 포함하지 않는다(`NEXT_PUBLIC_` 접두어 금지).

### 7.3 간단한 RLS 원칙

- **공개 읽기:** `mate_post`는 모집 상태·차단 관계를 고려해 필터링된 목록을 누구나 읽을 수 있다.
- **본인 쓰기/읽기:** `user_profile`, `mate_application`, `user_block`은 본인 행만 쓰고 읽는다(단, `mate_application`은 대상 글 작성자도 읽을 수 있다).
- **작성자 처리:** `mate_post` 수정·마감, `mate_application` 승인/거절은 해당 글 작성자만 가능하다.
- **Admin 전용:** `report`, `outbound_url_setting`은 신고자 본인의 신고 이력 조회를 제외하면 Admin 역할만 읽고 쓴다.
- 세부 정책은 `DB-RLS-BASE` Task(`supabase/migrations/0002_rls_base.sql`)에서 구현하며, 위 원칙보다 더 넓은 접근을 허용하는 정책을 추가하지 않는다.

### 7.4 ORM 미사용

Prisma를 포함한 어떤 ORM도 추가하지 않는다. `src/lib/db/*.ts`(`DB-ACCESS` Task)에서 Supabase JS 클라이언트(`@supabase/supabase-js` 또는 `@supabase/ssr`)의 쿼리 빌더를 직접 사용한다.

---

## 8. 테스트 — Vitest + Playwright Chromium Smoke

| 종류 | 도구 | 대상 | 파일 |
|---|---|---|---|
| 단위 테스트 | **Vitest** | 날짜 검증(`UNIT-TRAVEL-DATES`), 연락처 탐지(`UNIT-CONTACT-DETECTION`), 모집글/신청 상태 전이(`UNIT-MATE-STATE`) | `tests/unit/*.spec.ts` |
| 통합 테스트 | Vitest 또는 동등 러너 | RLS 정책(`TEST-RLS-BASIC`) | `tests/integration/rls-basic.spec.ts` |
| E2E Smoke | **Playwright, Chromium 프로젝트만** | 공개 화면(`E2E-PUBLIC-SMOKE`), 여행 도구(`E2E-TRAVEL-TOOLS`), 동행·계정(`E2E-MATE-AUTH`) | `tests/e2e/*.spec.ts` |

Playwright는 Chromium 하나만 구성하고 Firefox·WebKit 프로젝트, 시각적 회귀, 성능/부하 테스트는 추가하지 않는다(`TASKS/TASK-E2E-*.md` Forbidden 절과 동일 원칙).

---

## 9. CI/CD — GitHub Actions + Vercel Preview

- **GitHub Actions**(`CI-LINT-BUILD`, `.github/workflows/ci.yml`): main 병합 전 TypeScript strict, ESLint, Vitest, Playwright Chromium Smoke를 자동 실행한다. **병합 승인은 사람이 수행**하며 자동 Merge는 구성하지 않는다.
- **Vercel**: PR마다 Preview 배포를 생성해 리뷰어가 실제 화면에서 확인한다. Production 배포는 main 병합 후 Vercel이 자동 처리한다(`DEPLOY-VERCEL`, `docs/ops/vercel-checklist.md`).
- Supabase 배포 확인은 `DEPLOY-SUPABASE-CHECK`(`docs/ops/supabase-checklist.md`)에서 체크리스트로 다룬다.

---

## 10. 명시적 비사용/제외 대상

| 항목 | 상태 | 근거 |
|---|---|---|
| **AWS·EC2** | 사용 안 함 | 인프라는 Vercel(웹)+Supabase(DB/Auth)로 한정. `PROJECT_SCOPE.md` EX-OPS |
| **자동 Merge Runner** | 사용 안 함 | PR 승인·병합은 사람이 수행 |
| **CMS(콘텐츠 관리 시스템)** | 프로젝트 범위 제외 | 여행지·안전·대표는 §6의 정적 데이터 파일로 직접 관리(`PROJECT_SCOPE.md` EX-CMS) |
| **외부 이메일 공급자**(SendGrid 등) | 프로젝트 범위 제외 | 참가 요청·승인·거절·신고 결과는 전역 Toast/화면 상태로만 안내(`PROJECT_SCOPE.md` EX-EMAIL) |
| **Monitoring(APM/로그 수집 SaaS)** | 프로젝트 범위 제외 | 5xx 모니터링·구조화 로그·알림 파이프라인 미구축(`PROJECT_SCOPE.md` EX-OPS) |
| **Prisma/ORM** | 사용 안 함 | §7.4 |

---

## 11. 착수 차단(Blockers) — 실제로 없는 파일·환경변수만 기록

아래는 2026-09-19 기준 저장소를 직접 확인한 결과 **실제로 존재하지 않는** 항목이다. 존재를 가정하지 않고, 해당 Task 착수 전 반드시 준비해야 한다.

### 11.1 누락된 디렉터리/파일

| 항목 | 확인 방법 | 필요한 이유 |
|---|---|---|
| `src/data/` 디렉터리 자체 | `ls src` 결과 `src/app`만 존재 | §6 정적 데이터 3개 파일의 선행 조건 |
| `src/lib/` 디렉터리 자체 | 동일 | Supabase 클라이언트(§7.2), DB 접근(§7.4), 성인 확인 게이트의 선행 조건 |
| `.env.local`(또는 `.env.example`) | 저장소 루트에 `.env*` 파일 없음(확인 완료) | 아래 11.2 환경변수를 로드할 파일이 없음 |
| `supabase/` 디렉터리(마이그레이션·시드 경로) | 저장소 루트에 없음 | `DB-SCHEMA-BASE`/`DB-RLS-BASE`/`DB-SEED-BASE`의 선행 조건 |
| `tests/` 디렉터리 | 저장소 루트에 없음 | Vitest/Playwright 명세 파일의 선행 조건 |
| `.github/workflows/` | 저장소 루트에 `.github` 없음 | `CI-LINT-BUILD`의 선행 조건 |

### 11.2 누락된 의존성(`package.json`에 미설치, 2026-09-19 확인)

| 패키지 | 용도 |
|---|---|
| `@supabase/supabase-js` 또는 `@supabase/ssr` | §7.2 Browser/Server Client |
| `vitest` | §8 단위·통합 테스트 |
| `@playwright/test` | §8 E2E Chromium Smoke |

### 11.3 누락된 환경변수(현재 `.env*` 파일이 없으므로 값 확인 불가 = 전부 누락 상태)

| 변수 | 용도 |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Browser/Server Supabase Client 초기화 |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | 〃 |
| `SUPABASE_SERVICE_ROLE_KEY`(서버 전용, `NEXT_PUBLIC_` 접두어 절대 금지) | 서버 전용 관리 작업이 필요할 경우에만 |
| `FLIGHT_OUTBOUND_URL` | `outbound_url_setting` 초기값 또는 폴백값 |
| `HOTEL_OUTBOUND_URL` | 〃 |

이 목록에 없는 항목(예: 이메일 공급자 API 키, 모니터링 SaaS 토큰)은 §10에 따라 프로젝트 범위 밖이므로 착수 차단 사유로 기록하지 않는다.
