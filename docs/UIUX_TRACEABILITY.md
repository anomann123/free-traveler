# Free Traveler — UI/UX Traceability Matrix

**Document ID:** UIUX-TRACE-001
**기반 문서:** `docs/02_SRS_BASELINE.md`, `docs/PROJECT_SCOPE.md`, `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/05_UIUX_APPROVED.md`, `docs/06_SRS_UIUX_REVISED.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`

## 열 정의

| 열 | 의미 |
|---|---|
| Requirement | `02_SRS_BASELINE.md` 원문 ID(REQ-FUNC-001~080, REQ-NF-001~034), 삭제·재번호 없음 |
| Implementation Status | `PROJECT_SCOPE.md` 기준 범위 판단: `IMPLEMENT` / `IMPLEMENT(간소화)` / `IMPLEMENT(대체)` / `IMPLEMENT(부분)` / `EXCLUDED` |
| Screen | 승인된 SCR-00X, 다수 화면에 걸치면 쉼표로 병기, 화면 요소가 아니면 `N/A`, 전 화면 공통이면 `전역` |
| Route | Screen에 대응하는 Next.js Route, `N/A` 또는 `공통(전 Route)` |
| Page Entry | 대응 파일 경로, `N/A` 또는 `src/app/layout.tsx`(공통) |
| Task | 이번 문서 작성 시점 기준 Task 미생성 — `EXCLUDED`가 아닌 모든 행은 `PENDING_TASK_GENERATION`, `EXCLUDED` 행은 범위 밖이므로 `NOT_APPLICABLE(EXCLUDED)` |
| Test | `02_SRS_BASELINE.md` §5 표기와 1:1 대응하는 `TC-FUNC-XXX`/`TC-NF-XXX`, `EXCLUDED`는 `N/A(EXCLUDED)` |
| Status | 현재 코드 기준 실제 진행 상태: `NOT_STARTED`(구현 예정, 아직 코드 없음) 또는 `EXCLUDED`. **`src/app`에는 `layout.tsx`, `page.tsx` 스캘드만 존재하므로 어떤 항목도 `IMPLEMENTED`로 표기하지 않는다.** |

---

## 1. Functional Requirements (REQ-FUNC-001~080)

### 1.1 F1. Destination Guide

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-001 | NOT_STARTED |
| REQ-FUNC-002 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-002 | NOT_STARTED |
| REQ-FUNC-003 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-003 | NOT_STARTED |
| REQ-FUNC-004 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-004 | NOT_STARTED |
| REQ-FUNC-005 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-005 | NOT_STARTED |
| REQ-FUNC-006 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-006 | NOT_STARTED |
| REQ-FUNC-007 | IMPLEMENT(간소화) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-007 | NOT_STARTED |
| REQ-FUNC-008 | EXCLUDED | N/A(SCR-001 콘텐츠 대상) | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-009 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-009 | NOT_STARTED |
| REQ-FUNC-010 | EXCLUDED | N/A(SCR-001 관련) | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 1.2 F2. Flight Link-out

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-011 | NOT_STARTED |
| REQ-FUNC-012 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-012 | NOT_STARTED |
| REQ-FUNC-013 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-013 | NOT_STARTED |
| REQ-FUNC-014 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-014 | NOT_STARTED |
| REQ-FUNC-015 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-015 | NOT_STARTED |
| REQ-FUNC-016 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-016 | NOT_STARTED |
| REQ-FUNC-017 | IMPLEMENT | N/A(SCR-003 관련 서버 미저장 규칙) | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-017 | NOT_STARTED |
| REQ-FUNC-018 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-018 | NOT_STARTED |

### 1.3 F3. Hotel Link-out

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-019 | NOT_STARTED |
| REQ-FUNC-020 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-020 | NOT_STARTED |
| REQ-FUNC-021 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-021 | NOT_STARTED |
| REQ-FUNC-022 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-022 | NOT_STARTED |
| REQ-FUNC-023 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-023 | NOT_STARTED |
| REQ-FUNC-024 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-024 | NOT_STARTED |
| REQ-FUNC-025 | IMPLEMENT | N/A(SCR-003 관련 서버 미저장 규칙) | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-025 | NOT_STARTED |
| REQ-FUNC-026 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-026 | NOT_STARTED |

### 1.4 F4. Travel Mate

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | 전역(SCR-003/004/005 쓰기 게이트) | 공통(전 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-027 | NOT_STARTED |
| REQ-FUNC-028 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-028 | NOT_STARTED |
| REQ-FUNC-029 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-029 | NOT_STARTED |
| REQ-FUNC-030 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-030 | NOT_STARTED |
| REQ-FUNC-031 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-031 | NOT_STARTED |
| REQ-FUNC-032 | IMPLEMENT | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-032 | NOT_STARTED |
| REQ-FUNC-033 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-033 | NOT_STARTED |
| REQ-FUNC-034 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-034 | NOT_STARTED |
| REQ-FUNC-035 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-035 | NOT_STARTED |
| REQ-FUNC-036 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-036 | NOT_STARTED |
| REQ-FUNC-037 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-037 | NOT_STARTED |
| REQ-FUNC-038 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-038 | NOT_STARTED |
| REQ-FUNC-039 | IMPLEMENT | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-039 | NOT_STARTED |
| REQ-FUNC-040 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-040 | NOT_STARTED |
| REQ-FUNC-041 | IMPLEMENT(간소화) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-041 | NOT_STARTED |
| REQ-FUNC-042 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-043 | IMPLEMENT(대체) | 전역(SCR-003/004/005 Toast) | 공통(전 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-043 | NOT_STARTED |
| REQ-FUNC-044 | IMPLEMENT | N/A(서버 RLS 정책) | N/A | N/A | PENDING_TASK_GENERATION | TC-FUNC-044 | NOT_STARTED |
| REQ-FUNC-045 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 1.5 F5. Country Safety

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | N/A(SCR-001 콘텐츠 대상) | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-046 | NOT_STARTED |
| REQ-FUNC-047 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-047 | NOT_STARTED |
| REQ-FUNC-048 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-048 | NOT_STARTED |
| REQ-FUNC-049 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-049 | NOT_STARTED |
| REQ-FUNC-050 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-050 | NOT_STARTED |
| REQ-FUNC-051 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-051 | NOT_STARTED |
| REQ-FUNC-052 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-052 | NOT_STARTED |
| REQ-FUNC-053 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-053 | NOT_STARTED |
| REQ-FUNC-054 | IMPLEMENT | SCR-001, SCR-003 | `/`, `/travel-tools` | `src/app/page.tsx`, `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-054 | NOT_STARTED |
| REQ-FUNC-055 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-056 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 1.6 F6. About free_traveler

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | SCR-002, SCR-001 | `/about`, `/` | `src/app/about/page.tsx`, `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-057 | NOT_STARTED |
| REQ-FUNC-058 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-058 | NOT_STARTED |
| REQ-FUNC-059 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-059 | NOT_STARTED |
| REQ-FUNC-060 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-060 | NOT_STARTED |
| REQ-FUNC-061 | IMPLEMENT(간소화) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-061 | NOT_STARTED |
| REQ-FUNC-062 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-062 | NOT_STARTED |
| REQ-FUNC-063 | IMPLEMENT | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-063 | NOT_STARTED |

### 1.7 F7. Common, Admin, Governance

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역(모든 Screen) | 공통(전 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-064 | NOT_STARTED |
| REQ-FUNC-065 | IMPLEMENT | 전역(모든 Screen) | 공통(전 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | TC-FUNC-065 | NOT_STARTED |
| REQ-FUNC-066 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-066 | NOT_STARTED |
| REQ-FUNC-067 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-068 | IMPLEMENT | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-068 | NOT_STARTED |
| REQ-FUNC-069 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-070 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-071 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-072 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-073 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-074 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-075 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-076 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-077 | IMPLEMENT | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-077 | NOT_STARTED |
| REQ-FUNC-078 | IMPLEMENT | 전역(기술 Route 결과 표시) | 공통(전 Route) | `src/app/not-found.tsx` | PENDING_TASK_GENERATION | TC-FUNC-078 | NOT_STARTED |
| REQ-FUNC-079 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-FUNC-080 | IMPLEMENT | SCR-003(+전역 정책 링크) | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | TC-FUNC-080 | NOT_STARTED |

---

## 2. Non-Functional Requirements (REQ-NF-001~034)

### 2.1 Performance

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-001 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-002 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-003 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-004 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-005 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-006 | IMPLEMENT | N/A(SCR-001 이미지 다수 대상) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-006 | NOT_STARTED |
| REQ-NF-007 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 2.2 Reliability and Recovery

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-008 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-009 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-010 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-011 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 2.3 Security and Privacy

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | N/A(플랫폼 기본 TLS) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-012 | NOT_STARTED |
| REQ-NF-013 | IMPLEMENT | N/A(서버 Auth/RLS) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-013 | NOT_STARTED |
| REQ-NF-014 | IMPLEMENT | N/A(Server Actions CSRF) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-014 | NOT_STARTED |
| REQ-NF-015 | IMPLEMENT | N/A(입력 검증·이스케이프) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-015 | NOT_STARTED |
| REQ-NF-016 | IMPLEMENT | N/A(환경변수 관리) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-016 | NOT_STARTED |
| REQ-NF-017 | IMPLEMENT | N/A(SCR-003 관련 서버 미저장 규칙) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-017 | NOT_STARTED |
| REQ-NF-018 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 2.4 Safety and Moderation

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-019 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-020 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-021 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-022 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 2.5 Accessibility

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-023 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-024 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-025 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 2.6 Content, Freshness, SEO, Copyright

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | N/A(SCR-001/002 콘텐츠 대상) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-026 | NOT_STARTED |
| REQ-NF-027 | IMPLEMENT | N/A(SCR-001 콘텐츠 대상) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-027 | NOT_STARTED |
| REQ-NF-028 | IMPLEMENT(부분) | N/A(SCR-001 stale 배지 관련) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-028 | NOT_STARTED |
| REQ-NF-029 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-030 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |

### 2.7 Maintainability, Monitoring, Cost

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-031 | IMPLEMENT(부분) | N/A(CI/Playwright) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-031 | NOT_STARTED |
| REQ-NF-032 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-033 | EXCLUDED | N/A | N/A | N/A | NOT_APPLICABLE(EXCLUDED) | N/A(EXCLUDED) | EXCLUDED |
| REQ-NF-034 | IMPLEMENT | N/A(인프라 비용 운영 기준) | N/A | N/A | PENDING_TASK_GENERATION | TC-NF-034 | NOT_STARTED |

---

## 3. 집계 검증

| 구분 | 건수 |
|---|---:|
| REQ-FUNC 전체 | 80 |
| REQ-NF 전체 | 34 |
| **합계** | **114** |
| Implementation Status = EXCLUDED | FUNC 16 + NF 22 = 38 |
| Implementation Status ≠ EXCLUDED(IMPLEMENT 계열) | FUNC 64 + NF 12 = 76 |
| Task = PENDING_TASK_GENERATION | 76건(IMPLEMENT 계열과 동일) |
| Task = NOT_APPLICABLE(EXCLUDED) | 38건(EXCLUDED와 동일) |
| Status = NOT_STARTED | 76건 |
| Status = EXCLUDED | 38건 |

> 위 집계는 `docs/PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 건수(FUNC 64/16, NF 12/22)와 정확히 일치한다. 어떤 Requirement도 삭제되지 않았으며, 어떤 항목도 `IMPLEMENTED`로 거짓 기록되지 않았다.
