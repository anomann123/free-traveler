# Free Traveler — Task List

**Document ID:** TASKLIST-TRAVEL-001
**HARNESS_SCHEMA:** traveler-screen-route-v1
**기반 문서:** `docs/06_SRS_UIUX_REVISED.md`, `docs/PROJECT_SCOPE.md`, `docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, 실제 `src/app` 파일 트리
**선행 검사:** `python scripts/validate_inputs.py` PASS(위반 0건, 2026-09-19 기준 실행 결과) — 통과 후 본 문서를 작성했다.
**중요:** 이 문서는 계획 문서다. 이 Task List 작성 과정에서 구현 코드, Git Branch, Commit, Issue는 만들지 않았다.

---

## 0. 요약

| 구분 | 건수 |
|---|---:|
| Task 총 개수 | 64 |
| PAGE(Page Owner) | 5 |
| CMP(Component) | 40 |
| DATA(정적 데이터) | 3 |
| DB(스키마/RLS/접근/시드) | 4 |
| AUTH(인증/인프라) | 2 |
| UNIT(단위 테스트) | 3 |
| TEST(RLS 통합 테스트) | 1 |
| E2E(Playwright Chromium) | 3 |
| CI/DEPLOY | 3 |
| **Requirement 커버리지** | REQ-FUNC 80 + REQ-NF 34 = **114건 전부 계정됨**(IMPLEMENT 76건 → Task 연결, EXCLUDED 38건 → §5 NON_IMPLEMENTATION 표) |

Task 개수(64)는 예상 범위(45~65) 안에 있으나, 이 숫자 자체는 완료 조건이 아니다(`traveler-project-pipeline` Skill §8).

---

## 1. Page Owner Task (5개, 정확히 SCR-001~005와 1:1)

### PAGE-SCR001

| 필드 | 내용 |
|---|---|
| Seq | 23 |
| Task ID | PAGE-SCR001 |
| 제목 | SCR-001 메인 페이지 조립 |
| Category | PAGE |
| Implementation Status | IMPLEMENT |
| Requirement Ref | REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-046, REQ-FUNC-057, REQ-FUNC-068, REQ-NF-026 |
| Screen | SCR-001 |
| Route | `/` |
| Page Entry | `src/app/page.tsx` |
| Depends On | CMP-SCR001-HERO, CMP-SCR001-DEST-DOMESTIC, CMP-SCR001-DEST-OVERSEAS, CMP-SCR001-DEST-DRAWER, CMP-SCR001-THEME-CHIPS, CMP-SCR001-SAFETY-GRID, CMP-SCR001-SAFETY-DRAWER, CMP-SCR001-RECENT-MATES, CMP-SCR001-FOUNDER-SUMMARY, CMP-SCR001-FAVORITES, CMP-SHARED-HEADER-FOOTER, DATA-DESTINATIONS, DATA-SAFETY, DATA-REPRESENTATIVE |
| Expected Files | 기존 파일 수정: `src/app/page.tsx`(현재 `create-next-app` 기본 템플릿 내용) |
| Functional AC | - Section 순서: Hero(검색+`/travel-tools` CTA) → 국내 여행지 Card Grid 6 → 해외 여행지 Card Grid 6 → 여행 동기 Chip 6 → 국가별 주의사항 Card Grid 6 → 최근 동행글 Card 3 또는 완성형 Empty State → free_traveler 요약(50+/30+)+`/about` CTA<br>- 각 Section의 데이터 출처: 국내/해외 카드 = `DATA-DESTINATIONS`, 주의사항 카드 = `DATA-SAFETY`, 대표 요약 = `DATA-REPRESENTATIVE`, 최근 동행글 = `mate_post`(DB-ACCESS) 최신 3건<br>- 여행지 카드 클릭 시 같은 화면에서 상세 Drawer/Modal이 열린다(별도 페이지 이동 없음)<br>- 안전정보 카드 클릭 시 같은 화면에서 안전정보 Drawer/Modal이 열린다<br>- `create-next-app` 기본 Starter 마크업(Next.js 로고, "Get started by editing", 기본 문서/배포 링크)이 **완전히 제거**되었다 |
| Visual AC | - `create-next-app` 기본 히어로/로고/링크가 화면 어디에도 남아 있지 않다<br>- Hero 높이는 Desktop 1440px 기준 화면의 55~60%로 제한되어, 스크롤 없이 다음 Section(국내 여행지) 상단이 보인다(`D-001/DESIGN.md` §16)<br>- Desktop 콘텐츠 최대 폭 1200~1280px, Section 상하 여백 Desktop 64~96px / Mobile 40~64px(`D-001/DESIGN.md` §15)<br>- Card Grid는 Desktop 3열 → Mobile 1열로 열 수만 축소(행 재배열 금지), Mobile은 승인된 Stitch Screen ID `9f862d3f881f4bb7950e3e529b7d93f1`과 동일한 Section 순서·수량 유지<br>- 큰 빈 영역을 만들지 않는다. Lorem ipsum·"준비 중"·"정보 확인 필요" 문구를 어디에도 쓰지 않는다<br>- 최근 동행글이 0건이면: "아직 등록된 동행글이 없어요" 같은 안내 문장 + 이용 방법 한 줄 + "동행 글 작성하기"(비로그인 시 로그인 유도) CTA를 갖춘 완성형 Empty State를 표시하고, 내용 없는 빈 카드를 두지 않는다 |
| Security/Privacy AC | - 검색·필터 입력은 클라이언트 상태로만 처리하고 원문을 서버 로그에 남기지 않는다<br>- 안전정보 Drawer의 외교부 링크는 `target=_blank rel="noopener noreferrer"`를 사용한다 |
| Verify | TC-FUNC-001, TC-FUNC-004, TC-FUNC-006, TC-FUNC-046, TC-FUNC-057, TC-FUNC-068 + `E2E-PUBLIC-SMOKE` |
| Priority | P0 |

### PAGE-SCR002

| 필드 | 내용 |
|---|---|
| Seq | 32 |
| Task ID | PAGE-SCR002 |
| 제목 | SCR-002 대표 소개 페이지 조립 |
| Category | PAGE |
| Implementation Status | IMPLEMENT |
| Requirement Ref | REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-061, REQ-FUNC-062, REQ-FUNC-063 |
| Screen | SCR-002 |
| Route | `/about` |
| Page Entry | `src/app/about/page.tsx` |
| Depends On | CMP-SCR002-HERO, CMP-SCR002-STATS, CMP-SCR002-INTRO, CMP-SCR002-COUNTRIES, CMP-SCR002-TIMELINE, CMP-SCR002-GALLERY, CMP-SCR002-CONTACT-LINKS, CMP-SCR002-TOP-PICKS, CMP-SHARED-HEADER-FOOTER, DATA-REPRESENTATIVE, DATA-DESTINATIONS |
| Expected Files | 신규 생성: `src/app/about/page.tsx` |
| Functional AC | - Section 순서: Profile Hero → 여행 지표(50+ Trips/30+ Countries) → 소개·철학(2~4문단) → 여행 Timeline(6개 시점 이상) → 방문 국가 Chip(권역별, 30개국) → Gallery(사진 8장 이상) → 기억에 남는 여행지 4개+CTA<br>- Section별 데이터 출처: Hero/지표/소개/Timeline/국가/Gallery/문의링크 = `DATA-REPRESENTATIVE`, 추천 여행지 4개 = `DATA-DESTINATIONS`(대표 프로필의 추천 slug 참조)<br>- 추천 여행지 카드 클릭 시 SCR-001의 해당 여행지 상세 Drawer로 이동한다 |
| Visual AC | - Timeline 6개 이상, 방문 국가 정확히 30개(권역별 그룹), Gallery 8장 이상, 추천 여행지 정확히 4개 — 최소 수량 미달 시 게시하지 않는다(`D-001/DESIGN.md` §18)<br>- Hero 높이 Desktop 기준 화면의 약 55%로 제한해 다음 Section 시작이 보인다<br>- Desktop 콘텐츠 최대 폭 1200~1280px, Section 여백 Desktop 64~96px/Mobile 40~64px<br>- 큰 빈 영역·Lorem ipsum·"준비 중"·"정보 확인 필요" 금지<br>- 전량 정적 콘텐츠라 데이터 없음 상태는 발생하지 않지만, Gallery 개별 이미지 로드 실패 시에는 플레이스홀더 아이콘+"이미지를 불러오지 못했습니다" 완성형 대체 문구를 표시한다 |
| Security/Privacy AC | - 대표 인물 사진이 특정 서비스의 보증·인증으로 오인되지 않도록 문구를 제한한다(PROJECT_SCOPE EX-MEDIA 원칙 계승, 라이선스 승인 워크플로 자체는 EXCLUDED) |
| Verify | TC-FUNC-057~063 + 수동 QA(정적 콘텐츠 완전성 체크리스트) |
| Priority | P1 |

### PAGE-SCR003

| 필드 | 내용 |
|---|---|
| Seq | 40 |
| Task ID | PAGE-SCR003 |
| 제목 | SCR-003 통합 여행 준비 페이지 조립 |
| Category | PAGE |
| Implementation Status | IMPLEMENT |
| Requirement Ref | REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-054, REQ-FUNC-080, REQ-NF-017 |
| Screen | SCR-003 |
| Route | `/travel-tools` |
| Page Entry | `src/app/travel-tools/page.tsx` |
| Depends On | CMP-SCR003-INTRO, CMP-SCR003-TABS, CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM, CMP-SCR003-TIPS, CMP-SCR003-MATE-WRITE, CMP-SCR003-MATE-LOGIN-PROMPT, CMP-SHARED-HEADER-FOOTER, CMP-SHARED-TOAST, AUTH-ADULT-VERIFICATION |
| Expected Files | 신규 생성: `src/app/travel-tools/page.tsx` |
| Functional AC | - Section 순서: Intro(3단계 안내) → Tab(항공편/숙소/동행 구하기) → 조건 입력 Form → 요약+외부 이동 Action Card → 비전달 고지+Tip 3개 → 동행 로그인 안내 또는 작성 Form+안전 안내<br>- **항공편/숙소/동행 구하기 3개 탭이 모두 실제 콘텐츠로 조립된다.** 자리표시자로 남겨진 탭이 없다<br>- 3개 탭의 입력·검증·완료 상태는 서로 완전히 독립적으로 유지된다(한 탭의 값이 다른 탭에 영향을 주지 않는다)<br>- 항공·숙소 조건 입력값은 브라우저 상태로만 유지하며 서버 DB·서버 로그·분석 이벤트에 저장하지 않는다<br>- 외부 이동은 설정된 URL을 새 탭(`noopener,noreferrer`)으로 열고 목적지·날짜 쿼리를 붙이지 않는다<br>- 동행 작성 Form 제출 시 연락처 패턴이 감지되면 제출을 차단하고 수정 안내를 표시한다 |
| Visual AC | - Hero/Intro가 화면 전체를 채우지 않고 다음 Section(탭)이 바로 이어진다<br>- Desktop 폼 2열 그리드 → Mobile 1열, Mobile 승인 Screen ID `3e4e85ab173c49debea20fb05e92a92f` 기준 3탭 가로 균등 배치(가로 스크롤 금지) 유지<br>- 큰 빈 영역·Lorem ipsum·"준비 중"·"정보 확인 필요" 금지<br>- 비로그인 상태의 동행 탭은 빈 화면이 아니라 "로그인하고 동행을 구해보세요" 완성형 안내 카드(이용 방법+로그인 CTA 포함)를 표시한다 |
| Security/Privacy AC | - REQ-NF-017: 항공·호텔 원시 입력값이 네트워크 요청·서버 로그·DB 어디에도 나타나지 않는다(빌드 후 네트워크 탭 확인)<br>- 동행 작성 폼은 REQ-FUNC-032 연락처 탐지를 통과해야 저장된다 |
| Verify | TC-FUNC-011~026, TC-FUNC-031, TC-FUNC-032, TC-FUNC-054, TC-FUNC-080, TC-NF-017 + `E2E-TRAVEL-TOOLS` |
| Priority | P0 |

### PAGE-SCR004

| 필드 | 내용 |
|---|---|
| Seq | 48 |
| Task ID | PAGE-SCR004 |
| 제목 | SCR-004 동행 조회 페이지 조립 |
| Category | PAGE |
| Implementation Status | IMPLEMENT |
| Requirement Ref | REQ-FUNC-030, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-037, REQ-FUNC-039, REQ-FUNC-040 |
| Screen | SCR-004 |
| Route | `/mates` |
| Page Entry | `src/app/mates/page.tsx` |
| Depends On | CMP-SCR004-INTRO, CMP-SCR004-FILTER, CMP-SCR004-LIST, CMP-SCR004-DETAIL, CMP-SCR004-APPLICATION, CMP-SCR004-REPORT, CMP-SCR004-SAFETY-NOTICE, CMP-SHARED-HEADER-FOOTER, CMP-SHARED-TOAST, DB-ACCESS |
| Expected Files | 신규 생성: `src/app/mates/page.tsx` |
| Functional AC | - Section 순서: Intro+작성 CTA → Filter(국가·지역·기간·모집 상태)+결과 요약 → 동행글 Card 목록(데이터가 있으면 최대 8건 우선 노출) → 목록·상세 분할(Desktop) 또는 상세 Drawer(Mobile) → 신청 방법 3단계 안내 → 안전·신고·차단 안내+`/travel-tools` CTA<br>- 목록 데이터 출처: `mate_post`(DB-ACCESS), 종료일이 지난 글은 조회 시점에 CLOSED로 계산해 표시(배치 없음)<br>- 참가 메시지 제출은 500자 이내, 중복 PENDING/ACCEPTED 요청을 차단한다<br>- 신고 제출 시 사유 코드+설명을 받고 접수 ID를 3초 이내 표시한다<br>- 상세 패널의 "차단하기" 실행 시 즉시 목록·필터·상세 어디에서도 해당 작성자의 글이 노출되지 않는다(REQ-FUNC-040) |
| Visual AC | - Desktop은 목록(좌 40%)+상세(우 60%) 화면 내 분할, Mobile은 카드 탭 시 하단 Drawer로 상세를 연다(페이지 이동 없음)<br>- Desktop 콘텐츠 최대 폭 1200~1280px, Section 여백 Desktop 64~96px/Mobile 40~64px<br>- 조건에 맞는 글이 없으면: "조건에 맞는 동행글이 아직 없어요" 안내 문장 + 필터 초기화 버튼 + "새 동행글 작성" CTA + 이용 방법 한 줄을 갖춘 완성형 Empty State를 표시하고, 내용 없는 빈 카드를 두지 않는다<br>- Lorem ipsum·"준비 중"·"정보 확인 필요" 금지 |
| Security/Privacy AC | - 모집글·상세 어디에도 이메일·전화번호 등 공개 연락처를 노출하지 않는다(REQ-FUNC-033)<br>- 비공개 데이터(참가 메시지, 신고 상세)는 RLS로 작성자·요청자·Admin만 조회 가능하다(`DB-RLS-BASE`에 의존) |
| Verify | TC-FUNC-030, TC-FUNC-033~035, TC-FUNC-037, TC-FUNC-039, TC-FUNC-040 + `E2E-MATE-AUTH` |
| Priority | P0 |

### PAGE-SCR005

| 필드 | 내용 |
|---|---|
| Seq | 54 |
| Task ID | PAGE-SCR005 |
| 제목 | SCR-005 계정·관리 페이지 조립 |
| Category | PAGE |
| Implementation Status | IMPLEMENT |
| Requirement Ref | REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-066, REQ-FUNC-077 |
| Screen | SCR-005 |
| Route | `/account` |
| Page Entry | `src/app/account/page.tsx` |
| Depends On | CMP-SCR005-AUTH, CMP-SCR005-PROFILE, CMP-SCR005-MY-ACTIVITY, CMP-SCR005-ADMIN, CMP-SCR005-ROLE-SHELL, CMP-SHARED-HEADER-FOOTER, CMP-SHARED-TOAST, AUTH-SUPABASE-SETUP, DB-ACCESS |
| Expected Files | 신규 생성: `src/app/account/page.tsx` |
| Functional AC | - 역할별 Section: **Guest** → 계정 기능 Intro+로그인·가입·비밀번호 재설정 Card+로그인 후 가능한 기능 안내+보안 안내 / **Member** → 프로필 요약+수정 Form, 내 활동(내가 쓴 동행글+새 글 CTA, 참가 요청 목록+승인·거절, 차단 목록+해제) / **Admin(Member 탭에 추가)** → 관리 Intro, 신고 목록+상태 필터(OPEN/REVIEWING/RESOLVED/DISMISSED)+행별 상태 변경, 항공·숙소 외부 URL 설정 Form(HTTPS만 허용)<br>- **Guest·Member·Admin 3개 역할 상태가 각각 실제 콘텐츠로 조립된다.** 역할에 없는 탭·영역은 DOM에 렌더링되지 않는다(예: Guest에게 관리자 탭이 아예 존재하지 않음)<br>- 데이터 출처: 프로필/내 글/참가요청/차단 = `user_profile`/`mate_post`/`mate_application`/`user_block`(DB-ACCESS), 신고 목록 = `report`, 외부 URL = `outbound_url_setting` |
| Visual AC | - Desktop 좌측 세로 탭(폭 240px)+우측 콘텐츠(최대 1000px), Mobile 상단 가로 스크롤 탭+콘텐츠 풀폭<br>- 통계 Dashboard(차트·그래프)를 만들지 않고 목록·필터·폼으로만 구성한다<br>- 큰 빈 영역·Lorem ipsum·"준비 중"·"정보 확인 필요" 금지<br>- 내 글·참가요청·차단·신고 목록이 0건이면 각각 "아직 ~이 없어요" 안내 문장 + 다음 행동(글 작성, 다음 확인 주기 등) CTA를 갖춘 완성형 Empty State를 표시한다 |
| Security/Privacy AC | - 정확한 생년월일은 저장하지 않고 `is_adult`, `adult_verified_at`만 저장한다(REQ-FUNC-028)<br>- RLS로 본인 데이터·Admin만 비공개 데이터를 조회한다(`DB-RLS-BASE`)<br>- 외부 URL은 HTTPS 허용목록 검증을 통과해야 저장된다(REQ-FUNC-077) |
| Verify | TC-FUNC-028, 029, 036, 038, 040, 041, 066, 077 + `E2E-MATE-AUTH` |
| Priority | P0 |

---

## 2. Component Task (40개)

### 2.1 공용(Shared)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10 | CMP-SHARED-HEADER-FOOTER | 전역 Header/Footer | IMPLEMENT | REQ-FUNC-064, REQ-FUNC-065 | 전역 | 공통(전 Route) | `src/app/layout.tsx` | 없음 | 신규 생성: `src/app/_components/shared/header.tsx`, `src/app/_components/shared/footer.tsx` | 5개 Screen 공통 내비게이션(여행지·여행 도구·동행 찾기·대표 소개)과 3컬럼 Footer(서비스/정책/안내)를 제공 | Desktop 72px/Mobile 56px Header, 320px~Desktop 반응형, 가로 스크롤 없음(`D-001` §7) | 없음 | TC-FUNC-064, TC-FUNC-065 | P0 |
| 11 | CMP-SHARED-TOAST | 전역 Toast 컴포넌트 | IMPLEMENT(대체) | REQ-FUNC-043 | 전역 | 공통(전 Route) | `src/app/layout.tsx` | 없음 | 신규 생성: `src/app/_components/shared/toast.tsx` | 참가 요청 접수·승인·거절·신고 처리 결과를 이메일 대신 Toast로 1분 이내 표시 | `toast-success`/배너 톤 준수, 코랄과 구분된 semantic 색 사용 | 이메일 발송 실패로 상태 변경이 롤백되지 않음 | TC-FUNC-043 | P1 |
| 12 | CMP-SHARED-ERROR-PAGES | 404/오류 화면 | IMPLEMENT | REQ-FUNC-078 | 전역 | 공통(전 Route) | `src/app/not-found.tsx` | CMP-SHARED-HEADER-FOOTER | 신규 생성: `src/app/not-found.tsx` | 404·권한없음·외부 연결 실패에 홈/이전/재시도 중 최소 1개 복구 행동 제공 | 공통 Header/Footer 유지, 큰 빈 영역 없음 | 없음 | TC-FUNC-078 | P1 |

### 2.2 SCR-001 (10개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 13 | CMP-SCR001-HERO | 검색 Hero | IMPLEMENT | 구조적(직접 매핑 REQ 없음) | SCR-001 | `/` | `src/app/page.tsx` | CMP-SHARED-HEADER-FOOTER | 신규 생성: `src/app/_components/scr001/hero.tsx` | 목적지 키워드 검색창+`/travel-tools` CTA | 검색창은 완전 원형(pill), 높이 56px | 검색어를 서버 로그에 남기지 않음 | 수동 QA | P1 |
| 14 | CMP-SCR001-DEST-DOMESTIC | 국내 여행지 Card Grid | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-005 | SCR-001 | `/` | `src/app/page.tsx` | DATA-DESTINATIONS | 신규 생성: `src/app/_components/scr001/destination-grid.tsx` | 국내 탭 여행지만 표시, 국가·도시·계절·테마·기간 AND 필터, 키워드 부분 일치 검색, 카드 6개 | Desktop 3열 → Mobile 1열, 결과 없음 시 300ms 이내 안내+초기화 버튼(완성형 Empty State) | 없음 | TC-FUNC-001~003, TC-FUNC-005 | P0 |
| 15 | CMP-SCR001-DEST-OVERSEAS | 해외 여행지 Card Grid | IMPLEMENT | REQ-FUNC-006, REQ-FUNC-009 | SCR-001 | `/` | `src/app/page.tsx` | DATA-DESTINATIONS, DATA-SAFETY | 신규 생성: `src/app/_components/scr001/destination-grid-overseas.tsx` | 해외 여행지 카드 6개, 상세 진입 시 국가 안전정보 연결(country_code 일치), 관련 여행지 최대 6개 추천 | `surface-soft` 배경으로 국내 그리드와 구분 | 없음 | TC-FUNC-006, TC-FUNC-009 | P0 |
| 16 | CMP-SCR001-DEST-DRAWER | 여행지 상세 Drawer | IMPLEMENT | REQ-FUNC-004, REQ-FUNC-007 | SCR-001 | `/` | `src/app/page.tsx` | DATA-DESTINATIONS | 신규 생성: `src/app/_components/scr001/destination-drawer.tsx` | 소개·명소 5개↑·추천시기·1/3일 일정·예산·교통·음식 3개↑·에티켓·출처·수정일 표시 | Desktop 우측 슬라이드/Mobile 하단 Drawer, `rounded.lg` 상단 모서리 | 없음 | TC-FUNC-004, TC-FUNC-007 | P0 |
| 17 | CMP-SCR001-THEME-CHIPS | 여행 동기 Chip 필터 | IMPLEMENT | REQ-FUNC-002(연계) | SCR-001 | `/` | `src/app/page.tsx` | CMP-SCR001-DEST-DOMESTIC | 신규 생성: `src/app/_components/scr001/theme-chips.tsx` | 테마 Chip 6개 선택 시 국내/해외 그리드 필터링 | `chip`/`chip-active`, 44px 이상 터치 영역 | 없음 | 수동 QA | P1 |
| 18 | CMP-SCR001-SAFETY-GRID | 국가별 주의사항 Card Grid | IMPLEMENT | REQ-FUNC-046, REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-051, REQ-FUNC-052, REQ-FUNC-053 | SCR-001 | `/` | `src/app/page.tsx` | DATA-SAFETY | 신규 생성: `src/app/_components/scr001/safety-grid.tsx` | 소개 해외국가 전체 커버리지, 8개 카테고리, 출처·확인일·편집자, 중대경보 상단 텍스트 라벨, 국가/지역 범위 구분, 긴급연락처 | 카드 6개, 색상 단독 구분 금지(텍스트 라벨 병기) | 없음 | TC-FUNC-046~048, TC-FUNC-051~053 | P0 |
| 19 | CMP-SCR001-SAFETY-DRAWER | 안전정보 상세 Drawer | IMPLEMENT | REQ-FUNC-049, REQ-FUNC-050, REQ-FUNC-054 | SCR-001 | `/` | `src/app/page.tsx` | DATA-SAFETY | 신규 생성: `src/app/_components/scr001/safety-drawer.tsx` | 외교부 링크(새 탭), 확인 후 7일 경과 stale 배지, "공식 판단 대체 아님" 고지 | `badge-safety-info`/`badge-warning` 사용 | 외부 링크 `noopener,noreferrer` | TC-FUNC-049, TC-FUNC-050, TC-FUNC-054 | P0 |
| 20 | CMP-SCR001-RECENT-MATES | 최근 동행글 카드 | IMPLEMENT | 구조적(mate_post 재사용) | SCR-001 | `/` | `src/app/page.tsx` | DB-ACCESS | 신규 생성: `src/app/_components/scr001/recent-mates.tsx` | `mate_post` 최신 3건(모집중만), 0건이면 완성형 Empty State | 카드 3개 또는 Empty State, 빈 카드 금지 | 비공개 연락처 노출 금지 | 수동 QA | P1 |
| 21 | CMP-SCR001-FOUNDER-SUMMARY | 대표 요약 카드 | IMPLEMENT | REQ-FUNC-057(연계) | SCR-001 | `/` | `src/app/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr001/founder-summary.tsx` | `50+ Trips`/`30+ Countries` 수치가 SCR-002와 동일한 데이터 소스 참조 | `stat-card`, `/about` CTA | 없음 | TC-FUNC-057 | P1 |
| 22 | CMP-SCR001-FAVORITES | 즐겨찾기 토글 | IMPLEMENT | REQ-FUNC-068 | SCR-001 | `/` | `src/app/page.tsx` | CMP-SCR001-DEST-DOMESTIC, CMP-SCR001-DEST-OVERSEAS | 신규 생성: `src/app/_components/scr001/favorite-button.tsx` | `localStorage`에 여행지 slug 저장, 중복 추가 방지, 새로고침 후 유지 | 카드 우상단 아이콘, 44px 이상 터치 영역 | 서버 전송 없음(클라이언트 전용 저장) | TC-FUNC-068 | P2 |

### 2.3 SCR-002 (8개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 | CMP-SCR002-HERO | 대표 소개 Hero | IMPLEMENT | 구조적 | SCR-002 | `/about` | `src/app/about/page.tsx` | CMP-SHARED-HEADER-FOOTER, DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/hero.tsx` | 대표 사진+한 문장 소개 | 화면 높이 약 55% 제한 | 없음 | 수동 QA | P1 |
| 25 | CMP-SCR002-STATS | 여행 지표 카드 | IMPLEMENT | REQ-FUNC-057 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/stats.tsx` | `50+ Trips`/`30+ Countries` 두 카드+부연 설명 | `stat-card` | 없음 | TC-FUNC-057 | P1 |
| 26 | CMP-SCR002-INTRO | 소개·철학 문단 | IMPLEMENT | REQ-FUNC-058 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/intro.tsx` | 자기소개·시작 이유·철학 2~4문단 | 좌우 분할(사진/인용구+문단) | 없음 | TC-FUNC-058 | P1 |
| 27 | CMP-SCR002-COUNTRIES | 방문 국가 Chip | IMPLEMENT | REQ-FUNC-059 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/countries.tsx` | 권역별(아시아/유럽/북미/오세아니아 등) 30개국 Chip | `chip`, 그룹 헤딩 유지 | 없음 | TC-FUNC-059 | P1 |
| 28 | CMP-SCR002-TIMELINE | 여행 Timeline | IMPLEMENT | REQ-FUNC-060 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/timeline.tsx` | 연도·장소·요약 포함 시점 6개 이상 | 세로 Timeline 리스트 | 없음 | TC-FUNC-060 | P1 |
| 29 | CMP-SCR002-GALLERY | 여행 Gallery | IMPLEMENT | REQ-FUNC-061, REQ-NF-006 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/gallery.tsx` | 서로 다른 장소 사진 8장 이상, alt는 실제 장소 설명 문장 | lazy load, LCP 이미지 아닌 것은 priority 미지정 | 없음 | TC-FUNC-061, TC-NF-006 | P1 |
| 30 | CMP-SCR002-CONTACT-LINKS | 문의·SNS 링크 | IMPLEMENT | REQ-FUNC-062 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-REPRESENTATIVE | 신규 생성: `src/app/_components/scr002/contact-links.tsx` | 빈 링크는 렌더링하지 않음, 허용 프로토콜만 오픈 | 텍스트 링크 목록 | `javascript:` 등 비허용 프로토콜 차단 | TC-FUNC-062 | P2 |
| 31 | CMP-SCR002-TOP-PICKS | 추천 여행지 4 | IMPLEMENT | REQ-FUNC-063 | SCR-002 | `/about` | `src/app/about/page.tsx` | DATA-DESTINATIONS | 신규 생성: `src/app/_components/scr002/top-picks.tsx` | 정확히 4개, 비공개 여행지는 자동 제외+대체 후보 | Card Grid+CTA Banner | 없음 | TC-FUNC-063 | P1 |

### 2.4 SCR-003 (7개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 33 | CMP-SCR003-INTRO | 이용 안내 3단계 | IMPLEMENT | 구조적 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SHARED-HEADER-FOOTER | 신규 생성: `src/app/_components/scr003/intro.tsx` | "조건 입력 → 요약 확인 → 외부 사이트 이동" 3단계 안내 | 아이콘 3단 가로 배치 | 없음 | 수동 QA | P1 |
| 34 | CMP-SCR003-TABS | 탭 스위처 셸 | IMPLEMENT | 구조적(3탭 조립 기반) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SCR003-INTRO | 신규 생성: `src/app/_components/scr003/tabs.tsx` | 항공편/숙소/동행 구하기 3탭 전환, 탭별 상태 완전 독립 | 활성 탭 코랄 밑줄, Mobile 가로 균등 3분할(스크롤 없음) | 없음 | 수동 QA | P0 |
| 35 | CMP-SCR003-FLIGHT-FORM | 항공편 Form+요약+외부이동 | IMPLEMENT | REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-NF-017 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SCR003-TABS | 신규 생성: `src/app/_components/scr003/flight-form.tsx` | 국가·지역·출발일·귀국일 필수 입력, 국가 변경 시 지역 재계산, 날짜 역전/과거 차단, 요약 표시, 비전달 고지, 새 탭 외부 이동(`noopener,noreferrer`), URL 오류 시 차단+재시도 | 2열(Desktop)/1열(Mobile) Form | **입력값을 서버 DB·로그·URL 쿼리로 전송하지 않는다**(브라우저 상태로만 유지) | TC-FUNC-011~018, TC-NF-017 + `UNIT-TRAVEL-DATES` | P0 |
| 36 | CMP-SCR003-HOTEL-FORM | 숙소 Form+요약+외부이동 | IMPLEMENT | REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-NF-017 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SCR003-TABS | 신규 생성: `src/app/_components/scr003/hotel-form.tsx` | 국가·지역·체크인·체크아웃 필수 입력, 검증, 요약, 비전달 고지, 새 탭 외부 이동, URL 오류 처리 | 2열(Desktop)/1열(Mobile) Form | **입력값을 서버 DB·로그·URL 쿼리로 전송하지 않는다** | TC-FUNC-019~026, TC-NF-017 + `UNIT-TRAVEL-DATES` | P0 |
| 37 | CMP-SCR003-TIPS | 찾기 Tip 3개 | IMPLEMENT | 구조적(비전달 고지 연계 REQ-FUNC-015/023/054) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM | 신규 생성: `src/app/_components/scr003/tips.tsx` | 항공·숙소 찾기 실용 팁 3개 카드+비전달 고지 배너 | `safety-info-bg` 배너 | 없음 | TC-FUNC-054 | P1 |
| 38 | CMP-SCR003-MATE-WRITE | 동행 작성 Form | IMPLEMENT | REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-080 | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SCR003-TABS, DB-ACCESS, AUTH-ADULT-VERIFICATION | 신규 생성: `src/app/_components/scr003/mate-write-form.tsx` | 제목/국가/지역/기간/인원/조건/스타일/설명/안전수칙 동의 입력, 연락처 패턴 탐지 차단, 안전수칙 동의 시각 저장 | 안전 안내 배너(주황 계열) | 로그인+성인 확인 완료 사용자만 제출 가능 | TC-FUNC-031, TC-FUNC-032, TC-FUNC-080 + `UNIT-CONTACT-DETECTION` | P0 |
| 39 | CMP-SCR003-MATE-LOGIN-PROMPT | 동행 탭 로그인 유도 | IMPLEMENT | REQ-FUNC-027(연계) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | CMP-SCR003-TABS, AUTH-ADULT-VERIFICATION | 신규 생성: `src/app/_components/scr003/mate-login-prompt.tsx` | 비로그인/미성년 확인 상태에서 작성 Form 대신 로그인 유도 카드 표시 | 완성형 안내 카드(이용 방법+CTA) | 우회 성공 0건(서버에서도 재검증) | TC-FUNC-027 | P0 |

### 2.5 SCR-004 (7개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 41 | CMP-SCR004-INTRO | 동행 찾기 Intro | IMPLEMENT | 구조적 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | CMP-SHARED-HEADER-FOOTER | 신규 생성: `src/app/_components/scr004/intro.tsx` | 한 문장 소개+"새 동행글 작성" CTA(`/travel-tools` 이동) | CTA Banner(소형) | 없음 | 수동 QA | P1 |
| 42 | CMP-SCR004-FILTER | 검색 Filter+결과 요약 | IMPLEMENT | REQ-FUNC-030 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | DB-ACCESS | 신규 생성: `src/app/_components/scr004/filter.tsx` | 국가·지역·기간 겹침·연령대·성별·스타일·모집 상태 필터, 차단 사용자 글 제외, "조건에 맞는 모집글 N건" 요약 | Desktop sticky 좌측/Mobile 상단 시트 | 차단된 상대의 글은 결과에서 제외(RLS 연동) | TC-FUNC-030 | P0 |
| 43 | CMP-SCR004-LIST | 동행글 Card 목록 | IMPLEMENT | REQ-FUNC-033, REQ-FUNC-037 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | CMP-SCR004-FILTER | 신규 생성: `src/app/_components/scr004/mate-list.tsx` | 데이터 있으면 최대 8건 우선 노출, 종료일 경과 글은 조회 시 CLOSED로 표시, 연락처 비노출 | 2열(Desktop)/1열(Mobile) Card Grid, 0건 시 완성형 Empty State | 카드에 이메일·전화번호 등 노출 금지 | TC-FUNC-033, TC-FUNC-037 + `UNIT-MATE-STATE` | P0 |
| 44 | CMP-SCR004-DETAIL | 목록·상세 분할 패널 | IMPLEMENT | REQ-FUNC-033(연계), REQ-FUNC-040 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | CMP-SCR004-LIST, DB-ACCESS | 신규 생성: `src/app/_components/scr004/detail-panel.tsx` | 제목·작성자 정보(연락처 없음)·조건·설명 표시, 작성자 정보 하단에 "차단하기" 액션 제공(선택 시 확인 후 차단, 이후 상호 글·프로필·요청 비노출) | Desktop 좌40/우60 분할, Mobile 하단 Drawer, "차단하기"는 "신고"와 시각적으로 구분된 위치의 텍스트 버튼 | 비공개 필드는 RLS로만 노출, 차단 관계는 본인만 생성·조회·해제(`user_block`) | TC-FUNC-033, TC-FUNC-040 | P0 |
| 45 | CMP-SCR004-APPLICATION | 참가 신청 Form | IMPLEMENT | REQ-FUNC-034, REQ-FUNC-035 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | CMP-SCR004-DETAIL, AUTH-ADULT-VERIFICATION | 신규 생성: `src/app/_components/scr004/application-form.tsx` | 500자 이내 메시지, PENDING 저장, 동일 사용자 중복 PENDING/ACCEPTED 차단 | `button-primary`("참가 요청 보내기") | 비로그인/미성년 시 로그인 유도로 대체(REQ-FUNC-027) | TC-FUNC-034, TC-FUNC-035 + `UNIT-MATE-STATE` | P0 |
| 46 | CMP-SCR004-REPORT | 신고 모달 | IMPLEMENT | REQ-FUNC-039 | SCR-004 | `/mates` | `src/app/mates/page.tsx` | CMP-SCR004-DETAIL, DB-ACCESS | 신규 생성: `src/app/_components/scr004/report-modal.tsx` | 사유 코드+설명 입력, 접수 ID 3초 이내 표시 | Modal, 코랄이 아닌 semantic 색 | 신고자·피신고자 상세는 Admin만 조회(RLS) | TC-FUNC-039 | P1 |
| 47 | CMP-SCR004-SAFETY-NOTICE | 신청 방법+안전 안내 | IMPLEMENT | 구조적(안전 고지) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | CMP-SCR004-REPORT | 신규 생성: `src/app/_components/scr004/safety-notice.tsx` | "모집글 확인→참가 메시지 전송→작성자 승인 대기" 3단계+연락처 공유 금지·신고/차단 방법 요약+`/travel-tools` CTA | 3단계 안내+경고 톤 Banner | 없음 | 수동 QA | P1 |

### 2.6 SCR-005 (5개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 49 | CMP-SCR005-AUTH | 로그인/가입/재설정 | IMPLEMENT | REQ-FUNC-066, REQ-FUNC-027(연계) | SCR-005 | `/account` | `src/app/account/page.tsx` | AUTH-SUPABASE-SETUP | 신규 생성: `src/app/_components/scr005/auth-tab.tsx` | 이메일 가입·인증·로그인·로그아웃·비밀번호 재설정, 로그인 후 가능한 기능 안내, 보안 안내 | Guest에게만 노출되는 탭 | 인증되지 않은 이메일은 쓰기 권한 없음 | TC-FUNC-066 | P0 |
| 50 | CMP-SCR005-PROFILE | 프로필 요약·수정 | IMPLEMENT | REQ-FUNC-028, REQ-FUNC-029 | SCR-005 | `/account` | `src/app/account/page.tsx` | AUTH-ADULT-VERIFICATION, DB-ACCESS | 신규 생성: `src/app/_components/scr005/profile-tab.tsx` | 닉네임(필수)·연령대(필수)·성별(선택)·여행 스타일(필수)·자기소개, 성인 확인 상태 배지 | Member/Admin에게만 노출 | 생년월일 미저장, `is_adult`/`adult_verified_at`만 저장 | TC-FUNC-028, TC-FUNC-029 | P0 |
| 51 | CMP-SCR005-MY-ACTIVITY | 내 활동(글/요청/차단) | IMPLEMENT | REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-040 | SCR-005 | `/account` | `src/app/account/page.tsx` | DB-ACCESS | 신규 생성: `src/app/_components/scr005/my-activity-tab.tsx` | 내 글 목록+새 글 CTA+수동 마감/수정/삭제, 참가 요청 승인·거절, 차단 목록+해제 | Member/Admin에게만 노출, 0건 시 완성형 Empty State | 본인 데이터만 RLS로 조회 | TC-FUNC-036, TC-FUNC-038, TC-FUNC-040 | P0 |
| 52 | CMP-SCR005-ADMIN | 관리자 탭 | IMPLEMENT | REQ-FUNC-041, REQ-FUNC-077 | SCR-005 | `/account` | `src/app/account/page.tsx` | DB-ACCESS | 신규 생성: `src/app/_components/scr005/admin-tab.tsx` | 신고 목록+상태(OPEN/REVIEWING/RESOLVED/DISMISSED) 필터, 항공·숙소 외부 URL HTTPS 설정 Form | Admin에게만 노출, 차트/통계 없음(목록+폼만) | HTTP/`javascript:`/`data:` URL 저장 차단 | TC-FUNC-041, TC-FUNC-077 | P0 |
| 53 | CMP-SCR005-ROLE-SHELL | 역할별 탭 셸 | IMPLEMENT | 구조적(역할 게이팅) | SCR-005 | `/account` | `src/app/account/page.tsx` | AUTH-SUPABASE-SETUP | 신규 생성: `src/app/_components/scr005/role-shell.tsx` | Guest/Member/Admin 판별 후 해당 탭만 렌더링 | Desktop 세로 탭/Mobile 가로 탭 | 역할에 없는 탭은 DOM에 존재하지 않음(서버에서도 재검증) | 수동 QA + `E2E-MATE-AUTH` | P0 |

---

## 3. 정적 데이터 Task (3개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DATA-DESTINATIONS | 여행지 정적 데이터 | IMPLEMENT | REQ-FUNC-004, REQ-FUNC-007, REQ-FUNC-063, REQ-NF-026 | N/A | N/A | N/A | 없음 | 신규 생성: `src/data/destinations.ts` | 국내 10곳 이상·해외 15개국 30개 도시 이상, 소개 300자↑·명소 5개↑·1/3일 일정·예산·교통·음식 3개↑·에티켓 3개↑·출처·수정일 필드 포함 | 해당 없음(데이터 파일) | 이미지는 일반 URL+alt만 기록(라이선스 승인 워크플로 없음, EX-MEDIA) | TC-FUNC-004, TC-NF-026 | P0 |
| 2 | DATA-SAFETY | 국가 안전정보 정적 데이터 | IMPLEMENT | REQ-FUNC-046, REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-052, REQ-FUNC-053, REQ-NF-027, REQ-NF-028 | N/A | N/A | N/A | DATA-DESTINATIONS | 신규 생성: `src/data/country-safety.ts` | 소개 해외국가 전원 커버리지, 8개 카테고리, `scope_type`/`scope_text`, 긴급연락처, `verified_at` 포함 | 해당 없음 | 없음 | TC-FUNC-046~048, TC-NF-027, TC-NF-028 | P0 |
| 3 | DATA-REPRESENTATIVE | 대표 소개 정적 데이터 | IMPLEMENT | REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-061, REQ-FUNC-062 | N/A | N/A | N/A | DATA-DESTINATIONS | 신규 생성: `src/data/representative.ts` | `50+ Trips`/`30+ Countries` 단일 소스, 소개문·철학, 30개국 방문 목록, Timeline 6개↑, Gallery 8장↑, 문의/SNS 링크 | 해당 없음 | 없음 | TC-FUNC-057~062 | P0 |

---

## 4. DB / 인증·인프라 Task (6개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | DB-SCHEMA-BASE | 핵심 테이블 스키마 | IMPLEMENT | REQ-FUNC-028, REQ-FUNC-031, REQ-FUNC-034, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-077 | N/A | N/A | N/A | 없음 | 신규 생성: `supabase/migrations/0001_schema_base.sql` | 정확히 6개 테이블만 생성: `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_url_setting`(§3 상한 준수) | 해당 없음 | PK/FK/CHECK 제약으로 무결성 확보(예: `mate_application` 유니크 제약) | 수동 스키마 리뷰 | P0 |
| 5 | DB-RLS-BASE | RLS 정책 | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | N/A | N/A | N/A | DB-SCHEMA-BASE | 신규 생성: `supabase/migrations/0002_rls_base.sql` | 본인 글·요청, 요청 대상 작성자, Moderator/Admin만 비공개 데이터 조회 | 해당 없음 | 권한별 부정 접근 테스트 전량 403/빈 결과 | TC-FUNC-044, TC-NF-013 + `TEST-RLS-BASIC` | P0 |
| 6 | DB-ACCESS | 데이터 접근 계층 | IMPLEMENT | REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-037, REQ-FUNC-038, REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-077, REQ-NF-014, REQ-NF-015 | N/A | N/A | N/A | DB-SCHEMA-BASE, DB-RLS-BASE | 신규 생성: `src/lib/db/mate.ts`, `src/lib/db/report.ts`, `src/lib/db/outbound-url.ts`, `src/lib/db/block.ts` | Server Action/Route Handler로 CRUD 제공, 입력 검증·이스케이프 적용. `block.ts`는 `user_block` 생성(차단)·삭제(해제)·목록 조회를 제공하고 `mate.ts` 조회 함수가 이를 참조해 차단 상대의 글을 결과에서 제외 | 해당 없음 | CSRF 방어(Server Actions 기본), 저장 XSS 차단 | TC-NF-014, TC-NF-015 | P0 |
| 7 | DB-SEED-BASE | 기본 시드 데이터 | IMPLEMENT | 구조적(개발/데모 지원) | N/A | N/A | N/A | DB-SCHEMA-BASE | 신규 생성: `supabase/seed/base.sql` | 로컬/스테이징 개발용 최소 시드(테스트 계정 1~2개, 샘플 모집글) | 해당 없음 | 실제 개인정보 미포함(더미 데이터만) | 수동 QA | P2 |
| 8 | AUTH-SUPABASE-SETUP | Supabase Auth 연동 | IMPLEMENT | REQ-FUNC-066, REQ-NF-012, REQ-NF-014, REQ-NF-016 | N/A | N/A | N/A | DB-SCHEMA-BASE | 신규 생성: `src/lib/supabase/client.ts`, `src/lib/supabase/server.ts`, `src/app/auth/callback/route.ts` | 이메일 가입·인증·로그인·로그아웃·재설정, 세션 관리 | 해당 없음 | TLS 기본 적용, 비밀키는 환경변수로만 관리(클라이언트 번들 미포함) | TC-FUNC-066, TC-NF-012, TC-NF-016 | P0 |
| 9 | AUTH-ADULT-VERIFICATION | 성인 확인·쓰기 게이트 | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-028 | N/A | N/A | N/A | AUTH-SUPABASE-SETUP | 신규 생성: `src/lib/auth/adult-gate.ts` | 미인증/미성년 사용자의 쓰기 요청을 401 또는 로그인 리다이렉트로 차단, 정확한 생년월일 미저장 | 해당 없음 | 서버 측에서 재검증(클라이언트 우회 방지) | TC-FUNC-027, TC-FUNC-028 | P0 |

---

## 5. Unit / RLS Test Task (4개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Depends On | Expected Files | Functional AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|
| 55 | UNIT-TRAVEL-DATES | 날짜 검증 단위 테스트 | IMPLEMENT | REQ-FUNC-013, REQ-FUNC-021 | CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM | 신규 생성: `tests/unit/travel-dates.spec.ts` | 과거 출발일/체크인, 귀국일<출발일, 체크아웃≤체크인 등 경계값 전부 차단되는지 검증 | TC-FUNC-013, TC-FUNC-021 | P0 |
| 56 | UNIT-CONTACT-DETECTION | 연락처 탐지 단위 테스트 | IMPLEMENT | REQ-FUNC-032 | CMP-SCR003-MATE-WRITE | 신규 생성: `tests/unit/contact-detection.spec.ts` | 전화번호·이메일·메신저 ID 패턴 기준 테스트셋 탐지율 95%↑, 오탐 5%↓ 검증 | TC-FUNC-032 | P0 |
| 57 | UNIT-MATE-STATE | 모집글/신청 상태 전이 단위 테스트 | IMPLEMENT | REQ-FUNC-035, REQ-FUNC-037 | CMP-SCR004-LIST, CMP-SCR004-APPLICATION | 신규 생성: `tests/unit/mate-state.spec.ts` | 중복 PENDING/ACCEPTED 차단, 종료일 경과 시 CLOSED 계산 로직 검증 | TC-FUNC-035, TC-FUNC-037 | P0 |
| 58 | TEST-RLS-BASIC | RLS 통합 테스트 | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | DB-RLS-BASE | 신규 생성: `tests/integration/rls-basic.spec.ts` | 권한별(Guest/Member/Owner/Admin) 부정 접근 시도가 전량 403 또는 빈 결과인지 검증 | TC-FUNC-044, TC-NF-013 | P0 |

---

## 6. E2E(Playwright Chromium) Task (3개, 핵심 5~7개 흐름을 2~3개로 묶음)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Depends On | Expected Files | Functional AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|
| 59 | E2E-PUBLIC-SMOKE | 공개 화면 Smoke(SCR-001/002) | IMPLEMENT(부분) | REQ-NF-031(대체) | PAGE-SCR001, PAGE-SCR002 | 신규 생성: `tests/e2e/public-smoke.spec.ts` | 흐름 1) 메인 진입→국내/해외 카드 클릭→상세 Drawer 오픈 2) 안전정보 카드→Drawer 오픈 3) `/about` 진입→Timeline/Gallery 렌더 확인. **Chromium 프로젝트만 사용, Firefox/WebKit·시각적 회귀·성능 테스트는 포함하지 않는다** | TC-NF-031 | P0 |
| 60 | E2E-TRAVEL-TOOLS | 여행 도구 Smoke(SCR-003) | IMPLEMENT(부분) | REQ-NF-031(대체) | PAGE-SCR003 | 신규 생성: `tests/e2e/travel-tools.spec.ts` | 흐름 1) 항공 탭 입력→요약→외부 이동 새 탭 열림 확인 2) 숙소 탭 동일 플로우 3) 날짜 오류 시 제출 차단 확인. **Chromium 전용 Smoke, 다른 브라우저·성능·시각적 회귀 없음** | TC-NF-031 | P0 |
| 61 | E2E-MATE-AUTH | 동행·계정 Smoke(SCR-004/005) | IMPLEMENT(부분) | REQ-NF-031(대체) | PAGE-SCR004, PAGE-SCR005 | 신규 생성: `tests/e2e/mate-auth.spec.ts` | 흐름 1) 로그인→동행 목록 필터→상세→참가 요청 제출 2) `/account`에서 참가 요청 승인/거절 3) 관리자 계정으로 신고 상태 변경+외부 URL 저장. **Chromium 전용 Smoke** | TC-NF-031 | P0 |

---

## 7. CI / Vercel·Supabase 확인 Task (3개)

| Seq | Task ID | 제목 | Implementation Status | Requirement Ref | Depends On | Expected Files | Functional AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|
| 62 | CI-LINT-BUILD | CI 파이프라인(Lint/Build/Test) | IMPLEMENT(부분) | REQ-NF-031 | E2E-PUBLIC-SMOKE, E2E-TRAVEL-TOOLS, E2E-MATE-AUTH, UNIT-TRAVEL-DATES, UNIT-CONTACT-DETECTION, UNIT-MATE-STATE | 신규 생성: `.github/workflows/ci.yml` | main 병합 전 TypeScript strict, ESLint, Unit Test, Playwright Chromium Smoke 자동 실행 및 통과 요구. **자동 Merge Runner는 만들지 않는다(승인은 사람이 수행)** | TC-NF-031 | P0 |
| 63 | DEPLOY-VERCEL | Vercel 배포 설정 확인 | IMPLEMENT | REQ-NF-016, REQ-NF-034 | CI-LINT-BUILD | 신규 생성: `docs/ops/vercel-checklist.md` | Vercel 프로젝트 환경변수(Supabase 키, 외부 URL 등) 등록 확인, 무료/최소 티어로 월 비용 100,000원 이하 목표 확인. **EC2·AWS 인프라를 만들지 않는다** | TC-NF-016, TC-NF-034 | P1 |
| 64 | DEPLOY-SUPABASE-CHECK | Supabase 배포 확인 | IMPLEMENT | REQ-NF-012, REQ-NF-013 | DB-RLS-BASE, AUTH-SUPABASE-SETUP | 신규 생성: `docs/ops/supabase-checklist.md` | 운영 프로젝트에 TLS 1.2+ 기본 적용, RLS 정책이 프로덕션에도 배포되었는지 체크리스트로 확인 | TC-NF-012, TC-NF-013 | P1 |

---

## 8. NON_IMPLEMENTATION Register (EXCLUDED 38건 — 삭제하지 않고 근거·후속 방향 기록)

### 8.1 REQ-FUNC (16건)

| Requirement | 근거(Source) | 후속 방향 |
|---|---|---|
| REQ-FUNC-008 | `PROJECT_SCOPE.md` EX-CMS — 콘텐츠 수량 자동 게이트 미구축 | 출시 전 수동 체크리스트로 국내 10곳/해외 15개국 30개 도시 충족 여부 확인. 자동화는 CMS 도입 시 재검토 |
| REQ-FUNC-010 | `PROJECT_SCOPE.md` — Should 우선순위, URL query 필터 동기화 범위 밖 | 사용성 피드백 누적 후 차기 버전에서 검토 |
| REQ-FUNC-042 | `PROJECT_SCOPE.md` §2 — 세부 제재 조치(경고/숨김/계정 제한) 대신 신고 상태 변경만 제공 | 신고량 추이를 보고 Moderator 툴 고도화 시점 결정 |
| REQ-FUNC-045 | `PROJECT_SCOPE.md` — 탈퇴 시 비식별화·30일 삭제 자동 파이프라인 범위 밖 | 개인정보 요청 발생 시 수동 처리 절차를 운영 문서로 별도 수립 |
| REQ-FUNC-055 | `PROJECT_SCOPE.md` EX-CMS — Editor/Admin 안전정보 작성·검수·게시 워크플로 없음, 정적 데이터 직접 수정으로 대체 | 콘텐츠 운영자 채용/증가 시 CMS 도입 검토 |
| REQ-FUNC-056 | `PROJECT_SCOPE.md` EX-AUDIT — 안전정보 변경 이력 보존 UI 없음 | Git 커밋 이력으로 최소한의 추적성만 유지, 정식 이력 관리는 차기 버전 |
| REQ-FUNC-067 | `PROJECT_SCOPE.md` — 여행지+안전정보 통합검색 범위 밖(개별 검색만 제공) | 검색 사용 패턴 확인 후 통합검색 우선순위 재평가 |
| REQ-FUNC-069 | `PROJECT_SCOPE.md` — Should, Web Share API/URL 공유 범위 밖 | 차기 버전에서 URL 복사 폴백부터 추가 검토 |
| REQ-FUNC-070 | `PROJECT_SCOPE.md` — SEO 메타데이터 전면 적용 범위 밖, Next.js 기본 title만 | 트래픽 증가 시 canonical/OG/구조화 데이터 추가 |
| REQ-FUNC-071 | `PROJECT_SCOPE.md` — 분석 이벤트 수집 파이프라인 범위 밖 | KPI 측정 필요 시점에 최소 이벤트 스키마부터 도입 |
| REQ-FUNC-072 | `PROJECT_SCOPE.md` EX-CMS — Editor/Admin 콘텐츠 CRUD 없음 | 정적 데이터 파일 직접 수정으로 유지, 콘텐츠 팀 규모 확대 시 재검토 |
| REQ-FUNC-073 | `PROJECT_SCOPE.md` EX-MEDIA — 미디어 업로드·라이선스 승인 워크플로 없음 | 이미지 URL+alt만 기록하는 현재 방식 유지 |
| REQ-FUNC-074 | `PROJECT_SCOPE.md` EX-CMS — 게시 전 완전성 자동 게이트 없음 | §3 정적 데이터 Task의 수동 체크리스트로 대체, 규모 확대 시 자동화 |
| REQ-FUNC-075 | `PROJECT_SCOPE.md` — stale 현황 대시보드 범위 밖(공개 페이지 배지로 대체) | 안전정보 운영 담당자 지정 시 대시보드 필요성 재평가 |
| REQ-FUNC-076 | `PROJECT_SCOPE.md` EX-AUDIT — 범용 감사 로그 없음 | 규정 준수 요구 발생 시 감사 로그 스키마부터 별도 설계 |
| REQ-FUNC-079 | `PROJECT_SCOPE.md` — 자동 접근성 검사·수동 스크린리더 검증 범위 밖 | 기본 시맨틱 마크업만 적용, 접근성 감사는 차기 버전 |

### 8.2 REQ-NF (22건)

| Requirement | 근거(Source) | 후속 방향 |
|---|---|---|
| REQ-NF-001 | `PROJECT_SCOPE.md` EX-OPS — LCP 필드 측정 파이프라인 미구축 | Vercel Analytics 등 저비용 옵션 도입 시점에 재검토 |
| REQ-NF-002 | `PROJECT_SCOPE.md` EX-OPS — INP 측정 미구축 | 상동 |
| REQ-NF-003 | `PROJECT_SCOPE.md` EX-OPS — CLS 측정 미구축 | 상동 |
| REQ-NF-004 | `PROJECT_SCOPE.md` EX-OPS — 필터 응답 부하 테스트 미실시 | 트래픽 증가 시 부하 테스트 도입 |
| REQ-NF-005 | `PROJECT_SCOPE.md` EX-OPS — 쓰기 API 부하 테스트 미실시 | 상동 |
| REQ-NF-007 | `PROJECT_SCOPE.md` EX-OPS — Lighthouse CI 게이트 미구축 | CI 고도화 시 `CI-LINT-BUILD`에 추가 검토 |
| REQ-NF-008 | `PROJECT_SCOPE.md` EX-OPS — 가용성 SLA 모니터링 미구축, Vercel 기본 인프라 의존 | 유료 모니터링 도입 시 재검토 |
| REQ-NF-009 | `PROJECT_SCOPE.md` EX-OPS — 5xx 비율 모니터링 미구축 | 상동 |
| REQ-NF-010 | `PROJECT_SCOPE.md` EX-OPS — 자동 백업 RPO/RTO 설계 없음, Supabase 기본 백업 의존 | 데이터 규모 증가 시 백업 정책 별도 수립 |
| REQ-NF-011 | `PROJECT_SCOPE.md` EX-OPS — 주 1회 자동 링크 점검 스케줄러 없음 | 관리자 수동 점검으로 대체, 자동화는 차기 버전 |
| REQ-NF-018 | `PROJECT_SCOPE.md` — 개인정보 내보내기/삭제 자동화 범위 밖(REQ-FUNC-045와 동일 사유) | 수동 처리 절차로 대체 |
| REQ-NF-019 | `PROJECT_SCOPE.md` EX-OPS — 신고 응답시간 측정/부하 테스트 미실시(기능 자체는 IMPLEMENT) | 운영 지표 필요 시 계측 추가 |
| REQ-NF-020 | `PROJECT_SCOPE.md` — 24시간 SLA 추적 체계 미구축, 관리자 탭은 상태 필터만 제공 | 신고량 증가 시 SLA 대시보드 검토 |
| REQ-NF-021 | `PROJECT_SCOPE.md` EX-OPS — Rate limiting 인프라 미구축 | 어뷰징 발생 시 즉시 도입 검토 |
| REQ-NF-022 | `PROJECT_SCOPE.md` EX-AUDIT — Moderator 조치 추적용 감사 로그 없음(REQ-FUNC-042와 동일 사유) | 감사 로그 스키마 설계 시 함께 처리 |
| REQ-NF-023 | `PROJECT_SCOPE.md` — WCAG 2.2 AA 공식 준수 검증 범위 밖 | 접근성 감사 예산 확보 시 재검토 |
| REQ-NF-024 | `PROJECT_SCOPE.md` — axe 자동 검사 파이프라인 미구축 | CI 고도화 시 추가 |
| REQ-NF-025 | `PROJECT_SCOPE.md` — 키보드·스크린리더 수동 검증 미실시 | 상동 |
| REQ-NF-029 | `PROJECT_SCOPE.md` EX-MEDIA — 미디어 라이선스 메타데이터 100% 수집 안 함(URL+alt만) | 미디어 워크플로 도입 시 함께 처리 |
| REQ-NF-030 | `PROJECT_SCOPE.md` — SEO 메타데이터 전면 적용 범위 밖(REQ-FUNC-070과 동일) | 상동 |
| REQ-NF-032 | `PROJECT_SCOPE.md` EX-OPS — 구조화 로그 체계 미구축 | 운영 규모 확대 시 로깅 인프라 도입 |
| REQ-NF-033 | `PROJECT_SCOPE.md` EX-OPS — 5xx·외부 링크 실패 자동 알림 미구축 | 상동 |

---

## 9. Requirement 커버리지 자체 점검

- REQ-FUNC-001~080 전부(80건)와 REQ-NF-001~034 전부(34건), 총 **114건**이 위 §1~§7의 Task `Requirement Ref` 열 또는 §8 NON_IMPLEMENTATION Register 중 정확히 한 쪽 이상에 등장한다.
- IMPLEMENT 계열 76건(REQ-FUNC 64 + REQ-NF 12)은 모두 하나 이상의 구현 Task(§1~§4)와 하나 이상의 Test/Verify 참조(§5~§6 또는 TC-* 인용)에 연결되어 있다.
- EXCLUDED 38건(REQ-FUNC 16 + REQ-NF 22)은 §8에서 삭제 없이 근거와 후속 방향을 기록했다.
- **빠진 Requirement ID 없음.** (검증: `docs/UIUX_TRACEABILITY.md`의 114개 ID를 전수 대조)
