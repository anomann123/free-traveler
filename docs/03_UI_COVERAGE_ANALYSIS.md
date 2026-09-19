# Free Traveler — UI Coverage Analysis

**Document ID:** UICOV-TRAVEL-001
**기반 문서:** `00_PRD.md`(PRD-TRAVEL-001), `02_SRS_BASELINE.md`(SRS-TRAVEL-001), `PROJECT_SCOPE.md`(SCOPE-TRAVEL-001)
**목적:** SRS의 REQ-FUNC-001~080, REQ-NF-001~034(총 114건)를 전량 보존한 채, 5개 디자인 Screen에 배치 가능한 항목과 화면 요소가 아닌 항목을 구분한다.

---

## 1. 디자인 Screen 정의 (5개 고정)

| Screen | Route | 사용자 목표 | 주요 영역 | 상태(State) | 이동 목적지 |
|---|---|---|---|---|---|
| **SCR-001** | `/` 메인 | 국내·해외 여행지를 발견하고, 상세·안전정보를 확인한 뒤 다음 행동(도구/동행/대표)으로 이동한다 | 전역 GNB/Footer, 국내·해외 탭, 검색·필터바, 여행지 카드 목록, 빈 결과 안내, **여행지 상세 Drawer/Modal**(소개·명소·일정·예산·교통·음식·에티켓·출처·즐겨찾기), **국가 안전정보 Drawer/Modal**(8개 카테고리·stale 배지·중대경보 배너·외교부 링크), 대표 추천 카드 | Idle(목록) / Filtered / Empty / DestinationDetailOpen / SafetyDetailOpen / Stale | SCR-002, SCR-003, SCR-004, 외부(외교부 0404) |
| **SCR-002** | `/about` 대표 소개 | `free_traveler`의 경험·철학을 확인하고 추천 여행지로 이동한다 | 히어로(이미지+`50+`/`30+` 수치 카드), 소개문·철학·편집 원칙, 방문 권역/국가 목록, 여행 타임라인, 추천 여행지 6, 문의·SNS 링크 | Static(콘텐츠 렌더) | SCR-001(추천 여행지 상세) |
| **SCR-003** | `/travel-tools` 통합 여행 준비 | 항공·호텔 조건을 정리해 외부 사이트로 이동하거나, 동행 모집글을 작성한다 | **3탭 고정**: 항공 탭 / 호텔 탭 / 동행 작성 탭 — 각 입력 폼, 날짜·연락처 검증, 요약 카드, 비전달 고지, 외부 이동 버튼, 안전수칙 동의 | FormEditing / Validating / Blocked / Summary / Redirecting(외부) / SubmittingMatePost | 외부(Google Flights/Booking.com 새 탭), SCR-004(작성 완료 후 동행 상세) |
| **SCR-004** | `/mates` 동행 조회 | 조건에 맞는 동행글을 탐색하고 참가를 요청하거나 신고·조회한다 | 필터(국가·지역·기간·연령대·성별·스타일·모집상태), 모집글 카드 목록, **동행 상세 패널**(설명·모집상태·참가요청 폼·신고 모달) | ListLoaded / Filtered / DetailPanelOpen / ApplicationSubmitted / ReportModalOpen / ClosedAuto | SCR-003(새 글 작성), SCR-005(로그인 유도·내 활동) |
| **SCR-005** | `/account` 계정·관리 | 로그인·가입하고 프로필과 내 활동(글/요청/차단)을 관리하며, 신고·외부URL을 처리한다 | **4탭 고정**: 로그인/가입 탭 / 프로필 탭 / 내 활동 탭(내 글·참가요청·차단 관리) / 관리자 탭(신고 상태 필터·외부 URL 설정) | LoggedOut / AuthPending / ProfileEditing / ActivityList / AdminReportQueue | SCR-004(내 모집글), SCR-001(즐겨찾기 여행지) |

**배치 규칙 적용 확인**

| 규칙 | 반영 위치 |
|---|---|
| 여행지·안전 상세는 SCR-001 Drawer/Modal | REQ-FUNC-004, 006, 046~056 → SCR-001 |
| 항공·숙소·동행 작성은 SCR-003의 3탭 | REQ-FUNC-011~026(항공/호텔), 031~032/080(동행 작성) → SCR-003 |
| 동행 상세는 SCR-004 상세 패널 | REQ-FUNC-033~035, 037, 039 → SCR-004 |
| 로그인·프로필·내 활동·간단 관리자는 SCR-005 탭 | REQ-FUNC-028~029, 036, 038, 040~041, 066, 077 → SCR-005 |
| API Route·인증 callback·오류 처리는 기술 Route(디자인 Screen 미산정) | REQ-FUNC-078(오류 화면)은 발생 시점의 화면 위에 표시되는 공통 요소로 취급하며 별도 Screen으로 세지 않음 |

---

## 2. 분류 기준

### 2.1 UI 배치 분류

| 분류 | 정의 |
|---|---|
| **UI_DIRECT** | 5개 Screen 중 하나에 사용자가 직접 보고 조작하는 구체적 요소(폼, 버튼, 목록, 패널, 배지, 링크, 탭)로 나타난다 |
| **UI_STATE** | 화면 결과에 반영되지만 그 자체는 별도 요소가 아니라 클라이언트 상태·판정 로직(검증 차단, 옵션 재계산, 중복 방지, 세션 유지)으로 구현된다 |
| **NON_UI** | 특정 화면 요소로 나타나지 않는 서버·보안·데이터·성능 규칙이다 |
| **OPERATIONS** | 콘텐츠 운영, 관리자 업무 절차, 모니터링·SLA 등 운영 프로세스에 관한 요구사항이다 |

### 2.2 PROJECT_SCOPE 분류(참조)

`PROJECT_SCOPE.md` 값을 그대로 인용한다: `IMPLEMENT`, `IMPLEMENT(간소화)`, `IMPLEMENT(대체)`, `IMPLEMENT(부분)`, `EXCLUDED`. 본 문서는 이 값을 변경하지 않는다.

---

## 3. Functional Requirements 배치 (REQ-FUNC-001~080)

### 3.1 F1. Destination Guide (001~010) → 주 배치: SCR-001

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-001 | UI_DIRECT | IMPLEMENT | SCR-001 | 국내/해외 탭 |
| REQ-FUNC-002 | UI_DIRECT | IMPLEMENT | SCR-001 | 필터바 |
| REQ-FUNC-003 | UI_DIRECT | IMPLEMENT | SCR-001 | 검색창 |
| REQ-FUNC-004 | UI_DIRECT | IMPLEMENT | SCR-001 | 여행지 상세 Drawer/Modal 본문 |
| REQ-FUNC-005 | UI_DIRECT | IMPLEMENT | SCR-001 | 빈 결과 안내+초기화 버튼 |
| REQ-FUNC-006 | UI_DIRECT | IMPLEMENT | SCR-001 | 상세 Drawer 내 안전정보 링크 |
| REQ-FUNC-007 | UI_DIRECT | IMPLEMENT(간소화) | SCR-001 | 이미지+alt 텍스트 표시 |
| REQ-FUNC-008 | OPERATIONS | EXCLUDED | N/A(SCR-001 콘텐츠 대상) | 수량 게이트는 화면 요소가 아닌 콘텐츠 작성 시점 수동 확인 |
| REQ-FUNC-009 | UI_DIRECT | IMPLEMENT | SCR-001 | 관련 여행지 카드(최대 6) |
| REQ-FUNC-010 | UI_STATE | EXCLUDED | N/A(SCR-001 관련) | URL query 동기화 로직, 구현 범위 밖 |

### 3.2 F2. Flight Link-out (011~018) → 주 배치: SCR-003 항공 탭

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-011 | UI_DIRECT | IMPLEMENT | SCR-003 | 항공 입력 폼 |
| REQ-FUNC-012 | UI_STATE | IMPLEMENT | SCR-003 | 지역 옵션 재계산 로직 |
| REQ-FUNC-013 | UI_STATE | IMPLEMENT | SCR-003 | 날짜 검증 차단 로직 |
| REQ-FUNC-014 | UI_DIRECT | IMPLEMENT | SCR-003 | 요약 카드 |
| REQ-FUNC-015 | UI_DIRECT | IMPLEMENT | SCR-003 | 비전달 고지 문구 |
| REQ-FUNC-016 | UI_DIRECT | IMPLEMENT | SCR-003 | 외부 이동 버튼 |
| REQ-FUNC-017 | NON_UI | IMPLEMENT | N/A(SCR-003 관련) | 서버 미저장 규칙 |
| REQ-FUNC-018 | UI_DIRECT | IMPLEMENT | SCR-003 | URL 오류 안내+재시도 버튼 |

### 3.3 F3. Hotel Link-out (019~026) → 주 배치: SCR-003 호텔 탭

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-019 | UI_DIRECT | IMPLEMENT | SCR-003 | 호텔 입력 폼 |
| REQ-FUNC-020 | UI_STATE | IMPLEMENT | SCR-003 | 지역 옵션 재계산 로직 |
| REQ-FUNC-021 | UI_STATE | IMPLEMENT | SCR-003 | 날짜 검증 차단 로직 |
| REQ-FUNC-022 | UI_DIRECT | IMPLEMENT | SCR-003 | 요약 카드 |
| REQ-FUNC-023 | UI_DIRECT | IMPLEMENT | SCR-003 | 비전달 고지 문구 |
| REQ-FUNC-024 | UI_DIRECT | IMPLEMENT | SCR-003 | 외부 이동 버튼 |
| REQ-FUNC-025 | NON_UI | IMPLEMENT | N/A(SCR-003 관련) | 서버 미저장 규칙 |
| REQ-FUNC-026 | UI_DIRECT | IMPLEMENT | SCR-003 | 오류 안내 |

### 3.4 F4. Travel Mate (027~045) → 주 배치: SCR-003(작성)/SCR-004(조회·상세)/SCR-005(관리)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-027 | UI_STATE | IMPLEMENT | 전역(SCR-003/004/005 쓰기 게이트) | 인증 세션 접근 제어 |
| REQ-FUNC-028 | UI_STATE | IMPLEMENT | SCR-005 | 성인 확인 상태 게이트 |
| REQ-FUNC-029 | UI_DIRECT | IMPLEMENT | SCR-005 | 프로필 탭 폼 |
| REQ-FUNC-030 | UI_DIRECT | IMPLEMENT | SCR-004 | 필터바 |
| REQ-FUNC-031 | UI_DIRECT | IMPLEMENT | SCR-003 | 동행 작성 탭 폼 |
| REQ-FUNC-032 | UI_STATE | IMPLEMENT | SCR-003 | 연락처 패턴 탐지·제출 차단 |
| REQ-FUNC-033 | UI_DIRECT | IMPLEMENT | SCR-004 | 상세 패널 표시(연락처 비노출) |
| REQ-FUNC-034 | UI_DIRECT | IMPLEMENT | SCR-004 | 상세 패널 참가 요청 폼 |
| REQ-FUNC-035 | UI_STATE | IMPLEMENT | SCR-004 | 중복 요청 차단 로직 |
| REQ-FUNC-036 | UI_DIRECT | IMPLEMENT | SCR-005 | 내 활동 탭 승인/거절 버튼 |
| REQ-FUNC-037 | UI_DIRECT | IMPLEMENT | SCR-004 | 목록·상세 CLOSED 상태 배지(조회 시 계산) |
| REQ-FUNC-038 | UI_DIRECT | IMPLEMENT | SCR-005 | 내 활동 탭 마감/수정/삭제 |
| REQ-FUNC-039 | UI_DIRECT | IMPLEMENT | SCR-004 | 상세 패널 신고 모달 |
| REQ-FUNC-040 | UI_DIRECT | IMPLEMENT | SCR-005 | 내 활동 탭 차단/해제 |
| REQ-FUNC-041 | UI_DIRECT | IMPLEMENT(간소화) | SCR-005 | 관리자 탭 신고 목록·상태 필터 |
| REQ-FUNC-042 | OPERATIONS | EXCLUDED | N/A | 세부 제재 조치, 관리자 탭 범위 밖 |
| REQ-FUNC-043 | UI_DIRECT | IMPLEMENT(대체) | 전역(SCR-003/004/005 Toast) | 이메일 대신 Toast/화면 상태 |
| REQ-FUNC-044 | NON_UI | IMPLEMENT | N/A | RLS 서버 정책 |
| REQ-FUNC-045 | OPERATIONS | EXCLUDED | N/A | 탈퇴 비식별화·삭제 파이프라인 |

### 3.5 F5. Country Safety (046~056) → 주 배치: SCR-001 안전정보 Drawer/Modal

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-046 | OPERATIONS | IMPLEMENT | N/A(SCR-001 콘텐츠 대상) | 해외 15개국 안전정보 수동 작성 |
| REQ-FUNC-047 | UI_DIRECT | IMPLEMENT | SCR-001 | 8개 카테고리 섹션 |
| REQ-FUNC-048 | UI_DIRECT | IMPLEMENT | SCR-001 | 출처·확인일·편집자 메타 |
| REQ-FUNC-049 | UI_DIRECT | IMPLEMENT | SCR-001 | 외교부 링크 |
| REQ-FUNC-050 | UI_DIRECT | IMPLEMENT | SCR-001 | stale 경고 배지(렌더 시 계산) |
| REQ-FUNC-051 | UI_DIRECT | IMPLEMENT | SCR-001 | 중대경보 상단 배너 |
| REQ-FUNC-052 | UI_DIRECT | IMPLEMENT | SCR-001 | 국가/지역 범위 구분 표시 |
| REQ-FUNC-053 | UI_DIRECT | IMPLEMENT | SCR-001 | 긴급연락처 섹션 |
| REQ-FUNC-054 | UI_DIRECT | IMPLEMENT | SCR-001, SCR-003 | 면책 고지 문구(안전 상세+항공 요약) |
| REQ-FUNC-055 | OPERATIONS | EXCLUDED | N/A | Editor/Admin 작성·검수·게시 워크플로 |
| REQ-FUNC-056 | OPERATIONS | EXCLUDED | N/A | 변경 이력 보존 |

### 3.6 F6. About free_traveler (057~063) → 주 배치: SCR-002

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-057 | UI_DIRECT | IMPLEMENT | SCR-002(+SCR-001) | 대표명·수치 카드 |
| REQ-FUNC-058 | UI_DIRECT | IMPLEMENT | SCR-002 | 소개문·철학 |
| REQ-FUNC-059 | UI_DIRECT | IMPLEMENT | SCR-002 | 방문 권역/국가 목록 |
| REQ-FUNC-060 | UI_DIRECT | IMPLEMENT | SCR-002 | 타임라인 |
| REQ-FUNC-061 | UI_DIRECT | IMPLEMENT(간소화) | SCR-002 | 대표 이미지+alt |
| REQ-FUNC-062 | UI_DIRECT | IMPLEMENT | SCR-002 | 문의·SNS 링크 |
| REQ-FUNC-063 | UI_DIRECT | IMPLEMENT | SCR-002 | 추천 여행지 6(→SCR-001 이동) |

### 3.7 F7. Common, Admin, Governance (064~080) → 전역 또는 SCR-005

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-FUNC-064 | UI_DIRECT | IMPLEMENT | 전역(모든 Screen) | GNB/Footer |
| REQ-FUNC-065 | NON_UI | IMPLEMENT | 전역(모든 Screen) | 반응형 레이아웃 품질 속성 |
| REQ-FUNC-066 | UI_DIRECT | IMPLEMENT | SCR-005 | 로그인/가입 탭 |
| REQ-FUNC-067 | UI_DIRECT | EXCLUDED | N/A | 통합검색, 범위 밖 |
| REQ-FUNC-068 | UI_DIRECT | IMPLEMENT | SCR-001 | 즐겨찾기 버튼(localStorage) |
| REQ-FUNC-069 | UI_DIRECT | EXCLUDED | N/A | URL 공유, 범위 밖 |
| REQ-FUNC-070 | NON_UI | EXCLUDED | N/A | SEO 메타데이터 |
| REQ-FUNC-071 | NON_UI | EXCLUDED | N/A | 분석 이벤트 수집 |
| REQ-FUNC-072 | OPERATIONS | EXCLUDED | N/A | Editor/Admin CRUD |
| REQ-FUNC-073 | OPERATIONS | EXCLUDED | N/A | 미디어 업로드 워크플로 |
| REQ-FUNC-074 | OPERATIONS | EXCLUDED | N/A | 완전성 자동 게이트 |
| REQ-FUNC-075 | OPERATIONS | EXCLUDED | N/A | stale 현황 대시보드 |
| REQ-FUNC-076 | NON_UI | EXCLUDED | N/A | 범용 감사 로그 |
| REQ-FUNC-077 | UI_DIRECT | IMPLEMENT | SCR-005 | 관리자 탭 외부 URL 설정 폼 |
| REQ-FUNC-078 | UI_DIRECT | IMPLEMENT | 전역(기술 Route 결과 표시) | 404/500/권한없음 화면 — 별도 Screen 미산정 |
| REQ-FUNC-079 | NON_UI | EXCLUDED | N/A | 자동 접근성 검사·수동 검증 |
| REQ-FUNC-080 | UI_DIRECT | IMPLEMENT | SCR-003(+전역 정책 링크) | 안전수칙 동의 체크박스, 정책 페이지 |

---

## 4. Non-Functional Requirements 배치 (REQ-NF-001~034)

비기능 요구사항은 대부분 화면 요소가 아닌 시스템 품질·운영 규칙이므로 배치 Screen을 `N/A`로 표기하고, 관련이 있는 Screen은 비고에 참고로 남긴다.

### 4.1 Performance (001~007)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-001 | NON_UI | EXCLUDED | N/A | LCP 측정, 미구축 |
| REQ-NF-002 | NON_UI | EXCLUDED | N/A | INP 측정, 미구축 |
| REQ-NF-003 | NON_UI | EXCLUDED | N/A | CLS 측정, 미구축 |
| REQ-NF-004 | NON_UI | EXCLUDED | N/A | 필터 응답 부하 테스트, 미실시 |
| REQ-NF-005 | NON_UI | EXCLUDED | N/A | 쓰기 API 부하 테스트, 미실시 |
| REQ-NF-006 | NON_UI | IMPLEMENT | N/A(SCR-001 이미지 다수) | `next/image` 기본 최적화 |
| REQ-NF-007 | OPERATIONS | EXCLUDED | N/A | Lighthouse CI 게이트, 미구축 |

### 4.2 Reliability and Recovery (008~011)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-008 | OPERATIONS | EXCLUDED | N/A | 가용성 SLA 모니터링 |
| REQ-NF-009 | OPERATIONS | EXCLUDED | N/A | 5xx 비율 모니터링 |
| REQ-NF-010 | OPERATIONS | EXCLUDED | N/A | 백업 RPO/RTO |
| REQ-NF-011 | OPERATIONS | EXCLUDED | N/A | 링크 자동 점검 스케줄러 |

### 4.3 Security and Privacy (012~018)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-012 | NON_UI | IMPLEMENT | N/A | TLS(플랫폼 기본) |
| REQ-NF-013 | NON_UI | IMPLEMENT | N/A | Auth/RLS 서버 검증(SCR-004/005 접근 제어 근거) |
| REQ-NF-014 | NON_UI | IMPLEMENT | N/A | CSRF/SameSite |
| REQ-NF-015 | NON_UI | IMPLEMENT | N/A | XSS 방지 |
| REQ-NF-016 | NON_UI | IMPLEMENT | N/A | 비밀키 환경변수 |
| REQ-NF-017 | NON_UI | IMPLEMENT | N/A(SCR-003 관련) | 항공·호텔 입력값 미저장 |
| REQ-NF-018 | OPERATIONS | EXCLUDED | N/A | 개인정보 내보내기·삭제 |

### 4.4 Safety and Moderation (019~022)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-019 | NON_UI | EXCLUDED | N/A | 신고 접수 응답시간 측정 |
| REQ-NF-020 | OPERATIONS | EXCLUDED | N/A | 1차 검토 SLA |
| REQ-NF-021 | NON_UI | EXCLUDED | N/A | 속도 제한(rate limiting) |
| REQ-NF-022 | OPERATIONS | EXCLUDED | N/A | Moderator 조치 추적성(감사 로그) |

### 4.5 Accessibility (023~025)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-023 | NON_UI | EXCLUDED | N/A | WCAG 2.2 AA 공식 준수 검증 |
| REQ-NF-024 | OPERATIONS | EXCLUDED | N/A | axe 자동 검사 |
| REQ-NF-025 | OPERATIONS | EXCLUDED | N/A | 키보드·스크린리더 수동 검증 |

### 4.6 Content, Freshness, SEO, Copyright (026~030)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-026 | OPERATIONS | IMPLEMENT | N/A(SCR-001/002 콘텐츠 대상) | 콘텐츠 완전성 체크리스트 |
| REQ-NF-027 | OPERATIONS | IMPLEMENT | N/A(SCR-001 콘텐츠 대상) | 안전정보 커버리지 |
| REQ-NF-028 | OPERATIONS | IMPLEMENT(부분) | N/A(SCR-001 stale 배지 관련) | 7일 이내 확인 목표치(수치는 운영 약속) |
| REQ-NF-029 | OPERATIONS | EXCLUDED | N/A | 미디어 라이선스 메타 100% |
| REQ-NF-030 | NON_UI | EXCLUDED | N/A | SEO 메타데이터 전면 적용 |

### 4.7 Maintainability, Monitoring, Cost (031~034)

| ID | UI 분류 | PROJECT_SCOPE | 배치 Screen | 비고 |
|---|---|---|---|---|
| REQ-NF-031 | NON_UI | IMPLEMENT(부분) | N/A | strict/lint 통과 + Playwright smoke 대체 |
| REQ-NF-032 | NON_UI | EXCLUDED | N/A | 구조화 로그 |
| REQ-NF-033 | OPERATIONS | EXCLUDED | N/A | 5xx·외부링크 실패 알림 |
| REQ-NF-034 | OPERATIONS | IMPLEMENT | N/A | 월 인프라 비용 목표 |

---

## 5. 집계 검증

### 5.1 총 Requirement 수

| 구분 | 건수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계** | **114** |

### 5.2 UI 배치 분류별 건수

| 분류 | FUNC | NF | 합계 |
|---|---:|---:|---:|
| UI_DIRECT | 53 | 0 | 53 |
| UI_STATE | 9 | 0 | 9 |
| NON_UI | 8 | 18 | 26 |
| OPERATIONS | 10 | 16 | 26 |
| **합계** | **80** | **34** | **114** |

### 5.3 PROJECT_SCOPE 분류별 건수(교차 검증용, `PROJECT_SCOPE.md`와 동일해야 함)

| 구분 | FUNC | NF |
|---|---:|---:|
| IMPLEMENT(모든 하위 표기 포함) | 64 | 12 |
| EXCLUDED | 16 | 22 |

### 5.4 Screen별 UI_DIRECT/UI_STATE 요구사항 배치 건수(전역·N/A 제외, 참고용)

| Screen | 배치 건수(중복 표기된 보조 배치 포함) |
|---|---:|
| SCR-001 | 18 |
| SCR-002 | 7 |
| SCR-003 | 18 |
| SCR-004 | 6 |
| SCR-005 | 8 |
| 전역(GNB/Footer/오류화면/공통 게이트/Toast) | 5 |
| **합계(UI_DIRECT+UI_STATE, 중복 포함)** | **62** |

> 5개 Screen과 전역 요소로 배치되지 않는 나머지 요구사항(NON_UI, OPERATIONS 및 EXCLUDED 처리된 UI 항목)은 `N/A`로 표기했으며, 이는 화면 미배치가 아니라 "특정 화면의 개별 UI 요소로 표현되지 않는 시스템·운영 규칙"이라는 의미다. 모든 요구사항은 §3~§4 표에 원본 ID 그대로 1회씩 포함되어 있으며 어떤 항목도 삭제되지 않았다. EXCLUDED로 표기된 항목은 `PROJECT_SCOPE.md`의 판단을 그대로 인용했을 뿐 본 문서에서 구현 범위로 되돌리지 않았다.
