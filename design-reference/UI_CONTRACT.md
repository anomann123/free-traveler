# Free Traveler — UI Implementation Contract

**Document ID:** UICONTRACT-TRAVEL-001
**기반 문서:** `docs/03_UI_COVERAGE_ANALYSIS.md`, `docs/04_UIUX_PLAN.md`, `docs/STITCH_VALIDATION_REPORT.md`, `design-reference/D-001/DESIGN.md`
**현재 코드 상태:** `src/app/layout.tsx`, `src/app/page.tsx`만 존재(그 외 라우트 미구현)
**목적:** 승인된 SCR-001~005(Desktop) 및 SCR-001·SCR-003(Mobile) Screen을 Next.js App Router 구현 계약으로 고정한다. 각 Screen의 Route, Page Entry, 영역 순서, 주요 Component, 상태, 사용자 행동, 화면 간 이동, Desktop·Mobile 규칙, 금지 기능을 기록하며 임의로 확장하지 않는다.

---

## 0. Screen 분류 — 핵심 4 / 보조 1

| 분류 | Screen | 근거 |
|---|---|---|
| 핵심(Core) | SCR-001, SCR-003, SCR-004, SCR-005 | 검색·발견(001), 여행 조건 입력+외부 이동+동행 작성(003), 동행 조회·참가(004), 인증·프로필·내 활동·관리자 게이트(005) — MVP 필수 인터랙션을 직접 수행하는 화면 |
| 보조(Supplementary) | SCR-002 | 대표 소개는 정적 정보 제공 화면으로 인터랙션 게이트를 갖지 않으며, 다른 4개 화면으로 연결되는 진입점 역할만 수행 |

---

## 1. SCR-001 — 메인

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-001 |
| **Route** | `/` |
| **Page Entry** | `src/app/page.tsx` |
| **영역 순서** | Header → ① 검색 Hero(목적지 검색창+`/travel-tools` CTA) → ② 국내 인기 여행지 Card Grid 6 → ③ 해외 인기 여행지 Card Grid 6 → ④ 여행 동기·테마 Chip 6 → ⑤ 국가별 주의사항 Card Grid 6(안전정보 Drawer 연결) → ⑥ 최근 동행글 Card 3 또는 완성형 Empty State → ⑦ free_traveler 요약(50+/30+ 지표)+`/about` CTA → Footer |
| **주요 Component** | `search-bar-pill`, `destination-card`(국내/해외), `chip`/`chip-active`(테마), `destination-card` 변형(안전정보 배지 `badge-safety-info`/`badge-warning`), `mate-card`(최근 동행), `stat-card`(50+/30+), Drawer/Modal(여행지 상세, 안전정보 상세), `top-nav`, `footer-light` |
| **상태** | Loading(②③⑤⑥ 스켈레톤) · Success(기본) · Empty(④ 필터 결과 없음, ⑥ 모집글 없음 — 완성형 Empty State) · Error(⑤ Drawer 로드 실패, 검색 실패 — 재시도 배너) |
| **사용자 행동** | 목적지 키워드 검색, 테마 Chip으로 카드 필터링, 여행지 카드 클릭→상세 Drawer 오픈, 즐겨찾기 토글(localStorage), 안전정보 카드 클릭→안전정보 Drawer 오픈, CTA 클릭 |
| **다른 화면으로의 이동** | `/travel-tools`(Hero·⑥ Empty CTA), `/mates`(⑥ 카드 클릭), `/about`(⑦ CTA), 외부(외교부 0404, Drawer 내 링크) |
| **Desktop·Mobile 규칙** | Desktop 1440px 콘텐츠 폭 1200~1280px, Hero 높이 화면의 55~60%로 제한해 스크롤 없이 ② Section 상단이 보이게 함. Card Grid는 Desktop 3열 → Mobile 1열로 열 수만 축소(행 재배열 금지). Mobile 승인 Screen ID `9f862d3f881f4bb7950e3e529b7d93f1` 기준 Section 순서·수량 동일 유지, Section 여백 Mobile 40~64px |
| **금지 기능** | 여행지·안전정보 CRUD 화면(Editor/Admin), 통합검색(여행지+안전정보 결합), URL query 필터 상태 동기화, 실시간 가격/별점/광고, Airbnb 상표 요소, 결제·예약 UI |

---

## 2. SCR-002 — 대표 소개

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-002 |
| **Route** | `/about` |
| **Page Entry** | `src/app/about/page.tsx` |
| **영역 순서** | Header → ① Profile Hero(대표 사진+한 문장 소개) → ② 여행 지표(50+ Trips/30+ Countries) → ③ 소개·철학(2~4문단) → ④ 여행 Timeline(6개 시점 이상) → ⑤ 방문 국가 Chip(권역별, 30개국) → ⑥ Gallery(사진 8장 이상) → ⑦ 기억에 남는 여행지 4개+CTA → Footer |
| **주요 Component** | `stat-card`(50+/30+), 좌우 분할(소개·철학), Timeline 리스트, `chip`(권역별 국가), Gallery Card Grid, `destination-card` 변형(추천 4), `button-primary`(CTA) |
| **상태** | Loading(⑥ Gallery 이미지) · Success(기본, 전량 정적 콘텐츠) · Error(⑥ 개별 이미지 로드 실패 시 플레이스홀더 아이콘+안내로 대체, 페이지 전체는 유지) |
| **사용자 행동** | Gallery 사진 확대 보기, 추천 여행지 카드 클릭, CTA 클릭 |
| **다른 화면으로의 이동** | `/`(⑦ 추천 여행지→SCR-001 상세 Drawer), `/travel-tools`, `/mates`(⑦ CTA) |
| **Desktop·Mobile 규칙** | Desktop 콘텐츠 폭 1200~1280px, Hero 높이 화면의 약 55%. Card/Gallery/Chip은 Desktop 다열 → Mobile 1열. 이번 승인 범위에 Mobile Screen 미포함 — 구현 시 D-001 §14 반응형 규칙(열 수만 축소)을 그대로 적용하고 별도 Stitch 승인 없이 Section 순서·수량은 변경하지 않는다 |
| **금지 기능** | Editor/Admin 콘텐츠 CRUD, 미디어 업로드·라이선스 승인 워크플로(이미지는 URL+alt만), 인물 사진의 특정 서비스 보증 오인 연출, Airbnb 상표 요소 |

---

## 3. SCR-003 — 통합 여행 준비

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-003 |
| **Route** | `/travel-tools` |
| **Page Entry** | `src/app/travel-tools/page.tsx` |
| **영역 순서** | Header → ① Intro(이용 순서 3단계 안내) → ② Tab Switcher(항공편/숙소/동행 구하기) → ③ 조건 입력 Form(국가·지역·출발일·귀국일, 탭별 4필드) → ④ 요약+외부 이동 Action Card → ⑤ 비전달 고지 배너+Tip Card 3개 → ⑥ 동행 탭: 로그인 안내 카드 또는 모집글 작성 Form+안전 안내 배너 → Footer |
| **주요 Component** | 3단계 안내 아이콘 행, Tab(항공편/숙소/동행 구하기, 활성 탭 코랄 밑줄), `text-input` Form 필드, Action Card+`button-primary`(외부 이동), `badge-safety-info` 고지 배너, Tip Card 3개, `banner-warning`(안전 안내), 로그인 유도 카드 |
| **상태** | Loading(④ 외부 이동 버튼 클릭 직후) · Success(③→④ 전환, ⑥ 작성 완료 Toast) · Error(③ 날짜/필수값 검증 실패, ④ 외부 URL 오류, ⑥ 연락처 패턴 감지 — 각각 인라인 오류) · Unauthorized(⑥ 비로그인 시 작성 Form 대신 로그인 유도 카드) |
| **사용자 행동** | 탭 전환(3탭 독립 상태 유지), 조건 입력·검증, 요약 확인, 외부 사이트로 새 탭 이동, 동행 모집글 작성·안전수칙 동의 체크, 로그인 유도 CTA 클릭 |
| **다른 화면으로의 이동** | 외부(Google Flights/Booking.com 새 탭, `noopener,noreferrer`), `/mates`(⑥ 작성 완료 후 해당 모집글 상세), `/account`(⑥ 로그인 유도) |
| **Desktop·Mobile 규칙** | 3탭의 입력·검증·완료 상태는 서로 완전히 독립적으로 관리(한 탭 값이 다른 탭에 영향 없음). Desktop 폼 2열 그리드 → Mobile 1열 풀폭. Mobile 승인 Screen ID `3e4e85ab173c49debea20fb05e92a92f` 기준 3탭 가로 균등 배치 유지(가로 스크롤 금지) |
| **금지 기능** | 항공·숙소 입력값의 서버 DB·로그·분석 이벤트 저장(브라우저 상태로만 유지), 외부 URL에 목적지·날짜 쿼리 파라미터 부착, 실시간 항공권·호텔 가격 표시, 내부 예약·결제·발권 UI, Airbnb 상표 요소 |

---

## 4. SCR-004 — 동행 조회

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-004 |
| **Route** | `/mates` |
| **Page Entry** | `src/app/mates/page.tsx` |
| **영역 순서** | Header → ① Intro+새 동행글 작성 CTA → ② 검색 Filter(국가·지역·기간·모집 상태)+결과 요약 → ③ 동행글 Card 목록(데이터 있으면 최대 8건 우선 노출) → ④ 목록·상세 분할(Desktop 좌 40%/우 60%) 또는 상세 Drawer(Mobile) → ⑤ 동행 신청 방법 3단계 안내 → ⑥ 안전·신고·차단 안내+`/travel-tools` CTA → Footer |
| **주요 Component** | `button-primary`(작성 CTA), Filter 패널(sticky, 국가/지역/기간/모집상태), `mate-card`, 상세 패널(제목·작성자 정보-연락처 없음·조건·설명·참가 메시지 입력·`button-primary`(참가 요청)·신고 텍스트 버튼), 3단계 안내, `banner-warning`(안전 안내) |
| **상태** | Loading(③④ 스켈레톤) · Success(기본) · Empty(③④ 조건에 맞는 글 없음 — 완성형 Empty State: 필터 초기화+작성 CTA+이용 방법) · Error(④ 참가 요청/신고 제출 실패 — 재시도 배너) · Unauthorized(④ 비로그인 참가 요청 시도 시 폼 대신 로그인 안내) |
| **사용자 행동** | 필터 조건 변경, 모집글 카드 클릭→상세 열람, 참가 메시지 작성·제출, 신고 모달 오픈·제출, 목록 결과 정렬 |
| **다른 화면으로의 이동** | `/travel-tools`(① 작성 CTA, ⑥ CTA), `/account`(비로그인 시 로그인 유도, 내 활동으로 연결) |
| **Desktop·Mobile 규칙** | Desktop: 목록(좌 40%)+상세(우 60%) 화면 내 분할, 페이지 이동 없음. Mobile: 카드 탭 시 하단 Drawer로 상세 오픈. Filter 패널은 Desktop sticky 좌측 → Mobile 상단 접이식 시트. 이번 승인 범위에 Mobile Screen 미포함 — 구현 시 D-001 §11·§14 규칙을 그대로 적용 |
| **금지 기능** | 실시간 채팅·영상통화·실시간 위치 공유, 공개 연락처(전화번호·메신저 ID·이메일) 노출, 신고 세부 제재 조치 UI(경고·계정 제한 등, 상태 변경만 허용), 별점·리뷰, Airbnb 상표 요소 |

---

## 5. SCR-005 — 계정·관리

| 항목 | 내용 |
|---|---|
| **Screen ID** | SCR-005 |
| **Route** | `/account` |
| **Page Entry** | `src/app/account/page.tsx` |
| **영역 순서** | Header → 좌측 세로 탭(Desktop)/상단 가로 탭(Mobile), 역할별 조건부 렌더링: **Guest** → Intro+로그인·가입·비밀번호 재설정 Card+로그인 후 가능한 기능 안내+보안 안내 · **Member** → 프로필 요약+수정 Form, 내 활동(내가 쓴 동행글+새 글 CTA, 참가 요청 목록+승인/거절, 차단 목록+해제) · **Admin(Member 탭에 추가)** → 관리 Intro, 신고 목록+상태 필터(OPEN/REVIEWING/RESOLVED/DISMISSED)+행별 상태 변경, 항공·숙소 외부 URL 설정 Form(HTTPS만 허용) → Footer |
| **주요 Component** | 세로/가로 Tab, `text-input`(로그인·가입·프로필 Form), `mate-card` 변형(내 글), 참가 요청 리스트+승인/거절 버튼, 차단 목록+해제 버튼, 신고 목록(상태 배지 `badge-safety-info`/`badge-warning`/success/muted)+상태 변경 버튼, 외부 URL Form 2개+`button-primary`(저장) |
| **상태** | Loading(프로필/목록/신고 큐) · Success(기본, 저장·처리 후 `toast-success`) · Empty(내 글·요청·차단 없음, 신고 없음 — 완성형 Empty State) · Error(로그인/가입 실패, 저장 실패, URL 저장 실패-비허용 프로토콜) · Unauthorized(역할에 없는 탭은 DOM 미노출, 직접 URL 접근 시 권한 안내+홈/로그인 CTA) |
| **사용자 행동** | 로그인·회원가입·비밀번호 재설정, 프로필 수정·저장, 동행글 작성 CTA 클릭, 참가 요청 승인/거절, 사용자 차단·해제, 신고 상태 필터링·변경, 외부 URL 입력·저장 |
| **다른 화면으로의 이동** | `/mates`(내 모집글→상세, 참가 요청 처리 결과 연결), `/`(즐겨찾기 여행지로) |
| **Desktop·Mobile 규칙** | Desktop 좌측 세로 탭(폭 240px)+우측 콘텐츠(최대 1000px). Mobile 상단 가로 스크롤 탭 바+콘텐츠 풀폭 스택. 이번 승인 범위에 Mobile Screen 미포함 — 구현 시 D-001 §14 규칙 적용 |
| **금지 기능** | 통계 Dashboard(차트·그래프), 범용 감사 로그 UI, 세부 제재 조치(경고·콘텐츠 숨김·계정 일시 제한 등, 신고 상태 변경만 허용), 개인정보 내보내기/탈퇴 자동 파이프라인 UI, 미디어 업로드·라이선스 승인 워크플로, Airbnb 상표 요소, 결제 UI |

---

## 6. 기술 Route (Screen 미포함)

다음은 디자인 Screen으로 세지 않는 기술 Route다. 각 Screen의 화면 요소는 위 §1~5를 따르되, 아래 Route는 별도 Page Entry로 구현하며 UI Screen 목록·수량 검증 대상이 아니다.

| Route | 설명 |
|---|---|
| `src/app/auth/callback/route.ts` | Supabase 이메일 인증 콜백 처리 |
| `src/app/api/*` | 신고·참가요청·차단 등 서버 상태 변경용 Route Handler (필요 시) |
| `src/app/not-found.tsx` | 404 처리, SCR-001~005 어디서든 공통 재사용 |

---

## 7. 화면 간 이동 요약 (Navigation Graph)

| From | To | 트리거 |
|---|---|---|
| SCR-001 | SCR-003 | Hero CTA, ⑥ Empty State CTA |
| SCR-001 | SCR-004 | ⑥ 최근 동행글 카드 클릭 |
| SCR-001 | SCR-002 | ⑦ CTA |
| SCR-001 | 외부(외교부 0404) | 안전정보 Drawer 링크 |
| SCR-002 | SCR-001 | ⑦ 추천 여행지 카드 클릭 |
| SCR-002 | SCR-003, SCR-004 | ⑦ CTA |
| SCR-003 | 외부(Google Flights/Booking.com) | ④ 외부 이동 버튼 |
| SCR-003 | SCR-004 | ⑥ 동행글 작성 완료 후 |
| SCR-003 | SCR-005 | ⑥ 로그인 유도 |
| SCR-004 | SCR-003 | ①⑥ CTA |
| SCR-004 | SCR-005 | 비로그인 참가 요청 시 로그인 유도 |
| SCR-005 | SCR-004 | 내 모집글 클릭 |
| SCR-005 | SCR-001 | 즐겨찾기 여행지 클릭 |

---

## 8. 공통 금지 기능 (전 Screen)

`design-reference/D-001/DESIGN.md` §20 Do Not을 그대로 승계한다: Airbnb 상표 요소, 구매·예약·결제 UI, Proprietary 폰트 파일, Color Token 표 외 임의 색상, 실시간 가격·별점·광고, Lorem ipsum/준비 중/빈 카드, 역할에 없는 탭 렌더링.
