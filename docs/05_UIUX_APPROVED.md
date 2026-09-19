# Free Traveler — UI/UX Approval Record

**Document ID:** UIUX-APPROVED-001
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`
**목적:** SRS의 다중 공개 Route를 5개 승인 Screen으로 통합한 결과를 공식 기록하고, 이후 SRS 개정본(`06_SRS_UIUX_REVISED.md`)과 추적성 문서(`UIUX_TRACEABILITY.md`)의 근거로 삼는다.

---

## 1. 승인 상태 요약

| 항목 | 값 |
|---|---|
| Stitch 검증 최종 판정 | `STITCH_VALIDATION_NEEDS_HUMAN`(`docs/STITCH_VALIDATION_REPORT.md`) |
| 승인 대상 Screen | SCR-001~005(Desktop) 5개, SCR-001·SCR-003(Mobile) 2개 |
| 승인 조건 | 각 Screen의 **콘텐츠**는 PASS. 단 SCR-001 Mobile(2개), SCR-004 Desktop(3개), SCR-005 Desktop(2개, 수정 과정에서 생성)에 중복 화면이 남아 있어, `design-reference/DESIGN_MANIFEST.md`에 기재된 canonical Screen ID만 승인 대상이며 나머지 중복본은 Stitch 소유자가 수동 삭제해야 한다 |
| 디자인 정본 | `design-reference/D-001/DESIGN.md` (Status: LOCKED) |
| 구현 코드 상태 | **미착수.** `src/app`에는 `layout.tsx`, `page.tsx` 스캘드만 존재하며 본 문서가 승인하는 것은 화면 설계와 Route 계약이지 실제 구현이 아니다 |

---

## 2. 승인된 Screen 인벤토리

| Screen ID | Route | Page Entry | Device | Stitch Screen ID(canonical) | 분류 |
|---|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | Desktop 1440 | `a482ca45c55c4ebab0c51f2b9925ffa1` | 핵심 |
| SCR-001 Mobile | `/` | `src/app/page.tsx` | Mobile 390 | `9f862d3f881f4bb7950e3e529b7d93f1` | 핵심(Mobile 변형) |
| SCR-002 | `/about` | `src/app/about/page.tsx` | Desktop 1440 | `4fb00e0ddafe48f6a5e939adde28ec83` | 보조 |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | Desktop 1440 | `7be58bc38217407faa6fefd9a8e303f8` | 핵심 |
| SCR-003 Mobile | `/travel-tools` | `src/app/travel-tools/page.tsx` | Mobile 390 | `3e4e85ab173c49debea20fb05e92a92f` | 핵심(Mobile 변형) |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | Desktop 1440 | `f16524ce9c2f4428b840f56e473567cf` | 핵심 |
| SCR-005 | `/account` | `src/app/account/page.tsx` | Desktop 1440 | `c60112d500414a07961b82edd72409f1` | 핵심 |

> SCR-002, SCR-004, SCR-005는 이번 승인 범위에 Mobile 변형이 포함되지 않는다. 구현 시 `design-reference/D-001/DESIGN.md` §14의 반응형 규칙(열 수만 축소, Section 순서·수량 불변)을 그대로 적용한다.

---

## 3. 기존 공개 Route → 5개 승인 Screen 통합 매핑

`docs/02_SRS_BASELINE.md` §3.5 Page and Route Inventory에 정의된 Route는 삭제되지 않고, 아래와 같이 5개 Screen의 탭·패널·Drawer·Modal로 통합되었다.

| 기존 Route(SRS §3.5) | 통합 위치 | 통합 방식 |
|---|---|---|
| `/destinations` | SCR-001 | 국내·해외 인기 여행지 Card Grid Section |
| `/destinations/domestic` | SCR-001 | 국내 여행지 Card Grid Section |
| `/destinations/overseas` | SCR-001 | 해외 여행지 Card Grid Section |
| `/destinations/[slug]` | SCR-001 | 여행지 상세 **Drawer/Modal**(같은 화면에서 오픈, 페이지 이동 없음) |
| `/flights` | SCR-003 | **항공편 탭** |
| `/hotels` | SCR-003 | **숙소 탭** |
| `/safety` | SCR-001 | 국가별 주의사항 Card Grid Section |
| `/safety/[countryCode]` | SCR-001 | 안전정보 상세 **Drawer/Modal** |
| `/about` | SCR-002 | 그대로 유지(Route 동일, Screen 계약만 추가) |
| `/mates` | SCR-004 | 그대로 유지(Route 동일, Screen 계약 추가) |
| `/mates/[id]` | SCR-004 | 동행 상세 **목록·상세 분할 패널**(Desktop) / **Drawer**(Mobile) |
| `/mates/new` | SCR-003 | **동행 구하기 탭**(모집글 작성 Form) |
| `/auth/*` | SCR-005 | Guest 로그인/가입/비밀번호 재설정 탭 |
| `/my/*` | SCR-005 | Member 프로필·내 활동(내 글·참가요청·차단) 탭 |
| `/admin/*` | SCR-005 | Admin 탭(신고 상태 필터·변경, 외부 URL 설정 — 콘텐츠 CRUD는 `PROJECT_SCOPE.md` 기준 EXCLUDED) |

**결과:** 원래 15개 공개 Route가 5개 Screen(=5개 Page Entry)으로 통합되었으며, `[slug]`/`[id]`/`[countryCode]` 동적 상세 페이지는 모두 별도 Route가 아닌 Drawer/Modal/분할 패널로 대체되었다. 기술 Route(`/auth/callback`, `/api/*`, `not-found`)는 Screen 수에 포함하지 않는다(`design-reference/SCREEN_ROUTE_CONTRACT.json` `technical_routes` 참조).

---

## 4. UI Route Contract 요약

전체 계약은 `design-reference/UI_CONTRACT.md`(서술형)와 `design-reference/SCREEN_ROUTE_CONTRACT.json`(기계 판독용)에 고정되어 있다. 핵심 조건:

- `schema_version: traveler-screen-route-v1`, `framework: nextjs-app-router`
- `screens` 배열 정확히 5개, Route/Page Entry 중복 없음(검증 완료)
- 핵심 4(SCR-001, SCR-003, SCR-004, SCR-005) · 보조 1(SCR-002)
- 모든 Screen `page_owner_task_required=true`, `preview_required=true`
- SCR-001만 `starter_template_forbidden=true`
- `technical_routes`는 Screen 수 집계에서 제외
- `required_navigation`에 12건의 실제 이동 관계 기록

---

## 5. Release Acceptance Criteria (MVP 출시 승인 조건)

`docs/02_SRS_BASELINE.md` §6.8.3 Rollout Acceptance를 5-Screen 구조 기준으로 재확인한다. 아래 조건을 모두 충족해야 SCR-001~005 기반 MVP를 출시 승인할 수 있다.

| # | 조건 | 근거 |
|---|---|---|
| 1 | SCR-001~005 각 Screen이 `design-reference/UI_CONTRACT.md`의 영역 순서·최소 콘텐츠 수를 충족 | `04_UIUX_PLAN.md`, `D-001/DESIGN.md` §18 |
| 2 | Stitch 프로젝트의 중복 화면(SCR-001 Mobile, SCR-004, SCR-005)이 정리되어 canonical Screen만 남음 | `STITCH_VALIDATION_REPORT.md` §4 |
| 3 | `UIUX_TRACEABILITY.md`의 IMPLEMENT 대상 REQ-FUNC/REQ-NF 항목이 모두 Task 생성 및 Playwright 핵심 Smoke Test(REQ-NF-031 대체 기준)를 통과 | `PROJECT_SCOPE.md` §1-11 |
| 4 | EXCLUDED로 표시된 요구사항이 구현 범위로 임의 복원되지 않음 | `PROJECT_SCOPE.md` §3 |
| 5 | 5개 Screen 모두 Vercel 배포 후 실제 브라우저에서 Desktop 1440px 기준 확인, SCR-001·SCR-003은 Mobile 390px 기준도 확인 | `PROJECT_SCOPE.md` §1-12 |
| 6 | 본 문서 §1의 "구현 코드 상태" 항목이 실제 코드 기준으로 갱신되어 더 이상 "미착수"가 아님 | 본 문서 §1 |

이 조건이 충족되기 전까지 MVP는 "설계 승인" 단계이며 "구현 완료" 또는 "출시 가능" 상태로 기록하지 않는다.
