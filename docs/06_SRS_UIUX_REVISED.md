# SRS Revision Addendum — UI/UX Screen Consolidation

**Document ID:** SRS-TRAVEL-001-REV-UIUX
**개정 대상:** `docs/02_SRS_BASELINE.md`(SRS-TRAVEL-001, Rev 1.0)
**개정 유형:** 라우트·화면 구조 개정(Requirement 본문 개정 아님)
**기반 문서:** `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/05_UIUX_APPROVED.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`

---

## 0. 개정 원칙

1. **`02_SRS_BASELINE.md`의 REQ-FUNC-001~080, REQ-NF-001~034는 단 한 건도 삭제·재번호 부여하지 않는다.** 본 문서는 그 요구사항들을 5개 승인 Screen에 연결하기 위한 **라우트/화면 구조 개정판**이며, `02_SRS_BASELINE.md`를 대체하지 않는다. 요구사항의 원문·우선순위(M/S/C)·수용 기준(AC)은 `02_SRS_BASELINE.md`가 계속 기준 문서다.
2. 본 문서가 실제로 개정하는 것은 `02_SRS_BASELINE.md` **§3.5 Page and Route Inventory**와 **§3.6 Use Cases**의 Route 표기뿐이다. §4 Specific Requirements, §5 Traceability Matrix, §6 Appendix(데이터 모델·API 등)는 본 문서에서 재작성하지 않는다.
3. 제외된 기능은 EXCLUDED로 명시하며, 구현되지 않은 항목을 구현된 것으로 기록하지 않는다.

---

## 1. 요구사항 보존 확인

| 구분 | 범위 | 건수 | 상태 |
|---|---|---|---|
| Functional Requirements | REQ-FUNC-001~080 | 80 | `02_SRS_BASELINE.md` §4.1에 원문 유지, 삭제 없음 |
| Non-Functional Requirements | REQ-NF-001~034 | 34 | `02_SRS_BASELINE.md` §4.2에 원문 유지, 삭제 없음 |
| **합계** | | **114** | 전량 `docs/UIUX_TRACEABILITY.md`에서 1회씩 추적 |

---

## 2. §3.5 Page and Route Inventory — 개정판

`02_SRS_BASELINE.md` §3.5의 15개 공개 Route는 아래와 같이 **5개 승인 Screen(Page Entry)** 으로 통합된다. 원본 표는 `02_SRS_BASELINE.md`에 그대로 남기고, 본 표를 구현 기준의 최신본으로 사용한다.

| Screen ID | Route | Page Entry | Access | 통합된 기존 Route |
|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | Public | `/destinations`, `/destinations/domestic`, `/destinations/overseas`, `/destinations/[slug]`(Drawer), `/safety`, `/safety/[countryCode]`(Drawer) |
| SCR-002 | `/about` | `src/app/about/page.tsx` | Public | `/about`(변경 없음) |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | Public(동행 작성 탭은 Adult Member) | `/flights`(탭), `/hotels`(탭), `/mates/new`(탭) |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | Public(참가 요청은 Adult Member) | `/mates`(변경 없음), `/mates/[id]`(분할 패널/Drawer) |
| SCR-005 | `/account` | `src/app/account/page.tsx` | Public/Member/Role Restricted(탭별 상이) | `/auth/*`, `/my/*`, `/admin/*` |

**기술 Route(Screen 미포함, `SCREEN_ROUTE_CONTRACT.json` `technical_routes`):**

| Route | Page Entry | 비고 |
|---|---|---|
| `/auth/callback` | `src/app/auth/callback/route.ts` | Supabase 이메일 인증 콜백 |
| `/api/*` | `src/app/api/**/route.ts` | 신고·참가요청·차단 서버 처리 |
| `*`(404) | `src/app/not-found.tsx` | 공통 오류 화면 |

---

## 3. §3.6 Use Cases — Route 표기 개정

| ID | Use Case | 기존 표기(§3.6) | 개정 표기(승인 Screen 기준) |
|---|---|---|---|
| UC-01 | 여행지 검색·필터·상세 열람 | `/destinations*` | SCR-001 ①~③ Section + 상세 Drawer |
| UC-02 | 항공 여행 조건 입력·요약·외부 이동 | `/flights` | SCR-003 항공편 탭 |
| UC-03 | 호텔 숙박 조건 입력·요약·외부 이동 | `/hotels` | SCR-003 숙소 탭 |
| UC-04 | 동행 모집글 작성·마감 | `/mates/new` | SCR-003 동행 구하기 탭 + SCR-005 내 활동(마감/수정/삭제) |
| UC-05 | 동행 참가 요청·승인·거절 | `/mates/[id]` | SCR-004 상세 패널 + SCR-005 내 활동(참가 요청) |
| UC-06 | 신고·차단·운영 처리 | `/my/*`, `/admin/*` | SCR-004 신고 모달, SCR-005 내 활동(차단) + Admin 탭(신고 상태) |
| UC-07 | 국가별 안전정보 확인 | `/safety*` | SCR-001 ⑤ Section + 안전정보 Drawer |
| UC-08 | 대표 소개 확인 | `/about` | SCR-002 |
| UC-09 | 콘텐츠·외부 URL 관리 | `/admin/*` | **부분 개정**: 여행지·안전 콘텐츠 CRUD(REQ-FUNC-072~075)는 `PROJECT_SCOPE.md`에 따라 EXCLUDED, 외부 URL 설정(REQ-FUNC-077)만 SCR-005 Admin 탭에서 구현 |

---

## 4. UI Route Contract (참조)

전체 계약은 `design-reference/UI_CONTRACT.md`와 `design-reference/SCREEN_ROUTE_CONTRACT.json`에 고정되어 있으며 본 문서는 이를 SRS 라우트 인벤토리의 공식 후속 버전으로 채택한다. 주요 조건:

- `schema_version: traveler-screen-route-v1`, `framework: nextjs-app-router`, `screens` 5개, Route/Page Entry 중복 없음
- 핵심 4(SCR-001, SCR-003, SCR-004, SCR-005) · 보조 1(SCR-002)
- `/travel-tools`는 항공·숙소·동행 구하기 3탭을 모두 포함하며 3탭의 입력·검증·완료 상태는 서로 독립적이다
- `/account`는 인증(Guest)·프로필(Member)·내 활동(Member)·간단 관리자(Admin: 신고 상태 변경 + 외부 URL 설정만)를 역할별 조건부 탭으로 포함한다
- `required_navigation` 12건이 §3의 Route 통합과 정합함

---

## 5. Release Acceptance Criteria (참조)

`docs/05_UIUX_APPROVED.md` §5와 동일한 조건을 SRS 개정판의 출시 승인 기준으로 채택한다. 요약하면 (1) Screen별 영역 순서·최소 콘텐츠 수 충족, (2) Stitch 중복 화면 정리 완료, (3) `UIUX_TRACEABILITY.md`의 IMPLEMENT 항목 Task 생성 및 테스트 통과, (4) EXCLUDED 항목 임의 복원 금지, (5) Desktop 1440px 전 Screen + SCR-001·SCR-003 Mobile 390px 배포 확인, (6) 구현 코드 상태가 실제로 갱신될 것 — 6개 조건을 모두 충족해야 MVP 출시를 승인한다. 세부 표는 `05_UIUX_APPROVED.md` §5를 참조하며 본 문서에서 중복 작성하지 않는다.

---

## 6. 현재 구현 상태 고지

이 개정판이 작성되는 시점 기준으로 `src/app`에는 `layout.tsx`, `page.tsx` 스캘드만 존재하며, 위에서 개정한 5개 Screen(Route)은 **아직 코드로 구현되지 않았다.** 본 문서는 요구사항과 화면·라우트 구조의 연결 관계만 확정하며, 실제 구현 여부는 `docs/UIUX_TRACEABILITY.md`의 Implementation Status/Status 열을 기준으로 별도 추적한다.
