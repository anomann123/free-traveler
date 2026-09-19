# Free Traveler — Project Scope (Implementation Baseline)

**Document ID:** SCOPE-TRAVEL-001
**기반 문서:** `00_PRD.md`(PRD-TRAVEL-001), `02_SRS_BASELINE.md`(SRS-TRAVEL-001)
**현재 코드 상태:** `app/package.json`(Next.js 16 / React 19 / TypeScript / Tailwind 4 스캐폴드), `app/src/app`(App Router 초기 구조), `app/src/data`(정적 데이터 디렉터리, 비어 있음)
**요구사항 상태 정의**

| 상태 | 의미 |
|---|---|
| **IMPLEMENT** | 이번 범위에서 직접 구현하고 테스트한다 |
| **EXCLUDED** | 이번 범위에서 만들지 않으며 제외 이유를 함께 기록한다 |

---

## 1. 반드시 직접 구현할 범위

| # | 항목 | 대응 화면/기능 |
|---|---|---|
| 1 | 핵심 화면 4개 + 보조 화면 1개 | 핵심: `/destinations`(여행지), `/flights`(비행기 찾기), `/hotels`(호텔 찾기), `/mates`(동행 찾기) · 보조: `/`(홈, 4개 핵심 화면과 `/safety`, `/about`으로 연결되는 진입 허브) |
| 2 | 여행지 검색·필터와 상세 패널 | `/destinations`, `/destinations/domestic`, `/destinations/overseas`, `/destinations/[slug]` |
| 3 | 국가 안전정보 패널 | `/safety`, `/safety/[countryCode]` |
| 4 | `free_traveler` 대표 소개 | `/about` |
| 5 | 항공·숙소 입력·검증·요약·외부 이동 | `/flights`, `/hotels` |
| 6 | Supabase 이메일 인증과 성인 확인 | `/auth/*` |
| 7 | 동행글 작성·조회·수정·마감 | `/mates`, `/mates/[id]`, `/mates/new`, `/my/*` |
| 8 | 참가 요청·승인·거절 | `/mates/[id]`, `/my/*` |
| 9 | 간단한 차단·신고 | `/my/*`, 신고 모달 |
| 10 | 내 활동과 간단한 관리자 탭 | `/my/*`, `/admin/*`(신고 상태·외부 URL 설정만) |
| 11 | Playwright 핵심 Smoke Test | 위 1~10 화면의 골든 패스 |
| 12 | Vercel 배포 | 전체 애플리케이션 |

---

## 2. 구현 방식 원칙

| 원칙 | 적용 대상 |
|---|---|
| 여행지·안전·대표 콘텐츠는 `src/data` 정적 데이터로 관리한다 | REQ-FUNC-001~010, 046~056, 057~063 |
| 즐겨찾기는 `localStorage`로 클라이언트에만 저장한다 | REQ-FUNC-068 |
| 실제 이메일 알림 대신 Toast 또는 화면 상태로 결과를 표시한다 | REQ-FUNC-043 |
| 동행글 자동 마감은 배치 없이 조회 시점에 종료일을 계산해 판정한다 | REQ-FUNC-037 |
| 안전정보 최신성(stale)은 배치 없이 렌더링 시점에 `verified_at` 기준 7일 경과 여부를 계산한다 | REQ-FUNC-050 |
| 이미지는 일반 인터넷 URL과 alt 텍스트만 사용하고 업로드·라이선스 승인 절차는 만들지 않는다 | REQ-FUNC-007, 061 |
| 관리자는 신고 상태 변경과 외부 URL(항공·호텔) 설정만 다루며 콘텐츠 CRUD는 다루지 않는다 | REQ-FUNC-041, 077 |

---

## 3. 제외 기능과 사유

| 제외 항목 | 사유 |
|---|---|
| **EX-CMS** 전체 콘텐츠 CMS | 여행지·안전·대표 콘텐츠는 `src/data` 정적 파일로 직접 작성·배포한다. 게시 상태 전환, 미리보기, Editor/Admin CRUD 화면을 만들지 않는다. |
| **EX-MEDIA** 미디어 업로드·라이선스 승인 워크플로 | 이미지는 일반 인터넷 URL과 alt 텍스트만 정적 데이터에 기록한다. 업로드, 라이선스 유형·URL 필수 입력, 게시 차단 검증을 만들지 않는다. |
| **EX-AUDIT** 범용 감사 로그 | 신고 상태 변경 등 최소한의 상태값만 남기고, 관리자 행위 전반(actor/action/before/after)을 기록하는 범용 감사 로그 체계를 만들지 않는다. |
| **EX-OPS** 자동 백업·장애 알림·부하 테스트 | DB 백업 RPO/RTO 운영, 5xx·외부 링크 장애 알림, 동시 사용자 부하 테스트, Lighthouse CI 성능 게이트를 구축하지 않는다. Vercel/Supabase 기본 제공 범위에 의존한다. |
| **EX-EMAIL** 외부 이메일 사업자 연동 | 참가 요청·승인·거절·신고 결과는 Toast 또는 화면 상태로만 안내하고 실제 이메일 발송 연동을 만들지 않는다. |

> 위 표에 없는 EC2·AWS 인프라, 무인 자동 Merge Runner는 요구사항 문서에 대응 항목이 없는 개발/운영 프로세스 사안이며 본 프로젝트의 배포·협업 방식에 포함하지 않는다.

---

## 4. 요구사항 매핑 — Functional Requirements (REQ-FUNC-001~080)

### 4.1 F1. Destination Guide

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | `src/data`의 `scope: DOMESTIC/OVERSEAS` 필드로 탭 분기 | Playwright smoke: 탭 전환 시 목록 재검증 |
| REQ-FUNC-002 | IMPLEMENT | 국가·도시·계절·테마·기간 필터를 클라이언트 사이드 AND 조건으로 적용 | 수동 QA: 복수 필터 조합 결과 확인 |
| REQ-FUNC-003 | IMPLEMENT | 여행지명·국가명·테마 키워드 부분 일치 클라이언트 검색 | 수동 QA: 한글 부분 일치·결과 없음 케이스 |
| REQ-FUNC-004 | IMPLEMENT | 정적 데이터 스키마에 소개/명소 5개↑/추천시기/1·3일 일정/예산/교통/음식 3개↑/에티켓/출처/수정일 필드를 필수로 정의 | 수동 QA: 필드 누락 여부 체크리스트 검토 |
| REQ-FUNC-005 | IMPLEMENT | 빈 결과 시 조건 완화 안내 문구와 전체 초기화 버튼 표시 | Playwright smoke: 결과 없음 상태 진입 |
| REQ-FUNC-006 | IMPLEMENT | 여행지 데이터의 `country_code`와 안전정보 데이터의 `country_code`를 동일 키로 연결 | 수동 QA: 해외 여행지 상세→안전정보 링크 이동 |
| REQ-FUNC-007 | IMPLEMENT(간소화) | 이미지 URL과 alt 텍스트만 정적 데이터에 기록(EX-MEDIA로 출처/작가/라이선스 필드는 축소) | 수동 QA: alt 텍스트 존재 여부 확인 |
| REQ-FUNC-008 | EXCLUDED | EX-CMS(자동 게시 게이트 미구축) — 국내 10곳·해외 15개국 30개 도시 수량은 데이터 작성 시점에 수동으로 충족 | 수동 QA: 출시 전 콘텐츠 수량 체크리스트 |
| REQ-FUNC-009 | IMPLEMENT | 같은 국가·테마 정적 데이터를 필터링해 상세 하단 최대 6개 표시 | 수동 QA: 관련 여행지 노출 확인 |
| REQ-FUNC-010 | EXCLUDED | EX-SCOPE — Should 우선순위, 12개 필수 범위 밖. 필터 상태는 화면 내 메모리 상태로만 유지 | 해당 없음 |

### 4.2 F2. Flight Link-out

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-011 | IMPLEMENT | 목적 국가/지역·도시/출발일/귀국일 필수 입력 폼 | Playwright smoke: 항공 폼 렌더 확인 |
| REQ-FUNC-012 | IMPLEMENT | 국가 변경 시 지역·도시 옵션 재계산, 기존 값 초기화 | 수동 QA: 국가 변경 시나리오 |
| REQ-FUNC-013 | IMPLEMENT | 과거 출발일, 귀국일<출발일 클라이언트 검증으로 제출 차단 | Playwright smoke: 잘못된 날짜 제출 차단 |
| REQ-FUNC-014 | IMPLEMENT | 유효 입력 후 요약 단계 표시, 브라우저 세션 동안 상태 유지 | 수동 QA: 수정→재요약 값 일치 확인 |
| REQ-FUNC-015 | IMPLEMENT | 폼·요약 화면에 "입력값은 외부 사이트로 전달되지 않습니다" 고정 문구 표시 | 수동 QA: 문구 노출 확인 |
| REQ-FUNC-016 | IMPLEMENT | 환경변수 `FLIGHT_OUTBOUND_URL`을 `target=_blank rel="noopener noreferrer"`로 새 탭 오픈, query 미부착 | Playwright smoke: 외부 이동 버튼 클릭→새 탭 검증 |
| REQ-FUNC-017 | IMPLEMENT | 항공 입력값은 클라이언트 상태(React state)로만 유지하고 서버 요청·로그를 생성하지 않음 | 코드 리뷰: 서버 API 미존재 확인 |
| REQ-FUNC-018 | IMPLEMENT | URL 미설정·허용목록 밖이면 이동 차단 및 재시도 버튼 표시 | 수동 QA: URL 미설정 상태 시뮬레이션 |

### 4.3 F3. Hotel Link-out

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-019 | IMPLEMENT | 숙박 국가/지역·도시/체크인/체크아웃 필수 입력 폼 | Playwright smoke: 호텔 폼 렌더 확인 |
| REQ-FUNC-020 | IMPLEMENT | 국가 변경 시 지역·도시 옵션 재계산 | 수동 QA: 국가 변경 시나리오 |
| REQ-FUNC-021 | IMPLEMENT | 과거 체크인, 체크아웃≤체크인 검증으로 제출 차단 | Playwright smoke: 잘못된 날짜 제출 차단 |
| REQ-FUNC-022 | IMPLEMENT | 유효 입력 후 요약값을 폼 입력과 동일하게 표시 | 수동 QA: 요약-입력 일치 확인 |
| REQ-FUNC-023 | IMPLEMENT | 폼·요약에 입력값 비전달 고지 표시 | 수동 QA: 문구 노출 확인 |
| REQ-FUNC-024 | IMPLEMENT | 환경변수 `HOTEL_OUTBOUND_URL`을 새 탭·`noopener,noreferrer`로 오픈 | Playwright smoke: 외부 이동 버튼 클릭→새 탭 검증 |
| REQ-FUNC-025 | IMPLEMENT | 호텔 입력값은 서버 DB·로그·분석 이벤트에 저장하지 않음 | 코드 리뷰: 서버 API 미존재 확인 |
| REQ-FUNC-026 | IMPLEMENT | URL 오류 시 이동 차단, 현재 입력 유지, 오류 메시지 표시 | 수동 QA: URL 오류 상태 시뮬레이션 |

### 4.4 F4. Travel Mate

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-027 | IMPLEMENT | Supabase Auth 세션 검사로 동행 쓰기 작업(글 작성·요청·신고·차단) 접근을 제어 | Playwright smoke: 비로그인 접근 시 로그인 유도 |
| REQ-FUNC-028 | IMPLEMENT | 성인 확인 플로우에서 `is_adult`, `adult_verified_at`만 저장, 생년월일 미저장 | 코드 리뷰: 스키마에 생년월일 필드 없음 확인 |
| REQ-FUNC-029 | IMPLEMENT | 닉네임(필수)·연령대(필수)·성별(선택)·여행 스타일(필수)·자기소개 프로필 폼 | 수동 QA: 필수/선택 필드 검증 |
| REQ-FUNC-030 | IMPLEMENT | 국가·지역·기간 겹침·연령대·성별·여행 스타일·모집 상태 필터, 차단 사용자 글 제외 | 수동 QA: 필터 조합 및 차단 제외 확인 |
| REQ-FUNC-031 | IMPLEMENT | 제목/국가/지역/기간/인원/조건/스타일/설명/안전수칙 동의 입력 폼과 검증 | Playwright smoke: 모집글 작성 골든 패스 |
| REQ-FUNC-032 | IMPLEMENT | 본문에서 전화번호·이메일·메신저 ID 정규식 패턴 탐지 후 제출 차단 | 수동 QA: 연락처 패턴 포함 텍스트 제출 시도 |
| REQ-FUNC-033 | IMPLEMENT | 모집글 표시 응답에서 이메일·전화번호 등 연락처 필드 제외 | 코드 리뷰: 응답 데이터에 연락처 필드 없음 확인 |
| REQ-FUNC-034 | IMPLEMENT | 참가 메시지(최대 500자) 비공개 제출, PENDING 상태 저장 | Playwright smoke: 참가 요청 제출 |
| REQ-FUNC-035 | IMPLEMENT | Supabase 유니크 제약(사용자+글 조합)으로 중복 PENDING/ACCEPTED 차단 | 수동 QA: 동일 글 재요청 시도 |
| REQ-FUNC-036 | IMPLEMENT | 작성자만 ACCEPTED/REJECTED로 상태 변경 가능(RLS로 권한 제한) | Playwright smoke: 승인·거절 처리 |
| REQ-FUNC-037 | IMPLEMENT | 조회 시점에 오늘 날짜와 종료일을 비교해 CLOSED로 판정(배치 없음) | 수동 QA: 종료일 경과 글 조회 시 CLOSED 표시 |
| REQ-FUNC-038 | IMPLEMENT | 작성자가 모집글 수동 마감·수정·삭제, 승인 요청자 존재 시 경고 표시 | 수동 QA: 수정/삭제 시나리오 |
| REQ-FUNC-039 | IMPLEMENT | 글·사용자·참가 요청 신고 폼(사유 코드+설명), 신고 ID 즉시 표시 | Playwright smoke: 신고 제출 |
| REQ-FUNC-040 | IMPLEMENT | 사용자 차단·해제, 차단 후 상호 글·프로필·요청 비노출 | 수동 QA: 차단 전후 노출 비교 |
| REQ-FUNC-041 | IMPLEMENT(간소화) | 관리자 탭에서 신고 목록과 상태(OPEN/RESOLVED 등) 필터만 제공 | 수동 QA: 관리자 탭 신고 목록·상태 필터 확인 |
| REQ-FUNC-042 | EXCLUDED | EX-AUDIT/EX-SCOPE — 경고·콘텐츠 숨김·계정 제한 등 세부 제재 조치는 만들지 않고 신고 상태 변경만 제공(§2 원칙) | 해당 없음 |
| REQ-FUNC-043 | IMPLEMENT(대체) | EX-EMAIL — 이메일 대신 Toast/화면 상태로 참가 요청·승인·거절·신고 결과 안내 | 수동 QA: 상태 변경 시 Toast 노출 확인 |
| REQ-FUNC-044 | IMPLEMENT | Supabase RLS로 본인 글·요청, 대상 작성자, Admin만 비공개 데이터 열람 허용 | 수동 QA: 타 사용자 계정으로 비공개 데이터 접근 시도 |
| REQ-FUNC-045 | EXCLUDED | EX-SCOPE — 탈퇴 시 비식별화·30일 내 삭제 파이프라인은 12개 필수 범위 밖 | 해당 없음 |

### 4.5 F5. Country Safety

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-046 | IMPLEMENT | 소개되는 해외 15개국 전체에 안전정보 정적 데이터 1건씩 작성 | 수동 QA: 국가 수 대비 안전정보 수 일치 확인 |
| REQ-FUNC-047 | IMPLEMENT | 치안/사기/법규/교통/재난/보건/문화/긴급연락처 8개 섹션을 정적 데이터 스키마에 필수화 | 수동 QA: 섹션 누락 체크리스트 |
| REQ-FUNC-048 | IMPLEMENT | 정적 데이터에 출처명/URL/최종확인일/편집자 필드 포함 | 수동 QA: 메타데이터 필드 확인 |
| REQ-FUNC-049 | IMPLEMENT | 외교부 해외안전여행 링크를 새 탭·`noopener,noreferrer`로 제공 | Playwright smoke: 공식 출처 링크 클릭 |
| REQ-FUNC-050 | IMPLEMENT | 렌더링 시점에 `verified_at` 기준 7일 경과 여부를 계산해 stale 배지 표시(배치 없음, §2 원칙) | Playwright smoke: stale 배지 렌더 확인 |
| REQ-FUNC-051 | IMPLEMENT | 중대 경보를 본문 상단에 텍스트 라벨로 표시(색상 단독 사용 금지) | 수동 QA: 중대 경보 데이터 표시 위치 확인 |
| REQ-FUNC-052 | IMPLEMENT | 정적 데이터에 `scope_type`(COUNTRY/REGION), `scope_text` 필드 구분 | 수동 QA: 지역 경보 표시 확인 |
| REQ-FUNC-053 | IMPLEMENT | 현지 긴급전화·영사콜센터 연결 정보를 정적 데이터에 포함 | 수동 QA: 긴급연락처 섹션 확인 |
| REQ-FUNC-054 | IMPLEMENT | 안전 페이지·항공 요약에 "공식 판단 대체 아님, 출국 전 원문 재확인" 고지 문구 표시 | 수동 QA: 고지 문구 노출 확인 |
| REQ-FUNC-055 | EXCLUDED | EX-CMS — Editor/Admin 작성·검수·게시 워크플로 없이 정적 데이터 파일을 직접 수정 | 해당 없음 |
| REQ-FUNC-056 | EXCLUDED | EX-AUDIT — 변경 이력(이전값/사유/담당자) 보존 UI를 만들지 않음 | 해당 없음 |

### 4.6 F6. About free_traveler

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-057 | IMPLEMENT | 정적 데이터에 `50+ Trips`, `30+ Countries` 단일 소스로 정의, 홈·About에서 동일 참조 | 수동 QA: 홈-About 수치 일치 확인 |
| REQ-FUNC-058 | IMPLEMENT | 확정 소개문·여행 철학·편집 원칙을 정적 데이터로 About 페이지에 전문 표시 | 수동 QA: 소개문 노출 확인 |
| REQ-FUNC-059 | IMPLEMENT | 방문 권역/국가 목록을 정적 데이터로 제공 | 수동 QA: 국가 목록-권역 연결 확인 |
| REQ-FUNC-060 | IMPLEMENT | 연도·장소·요약을 포함한 여행 타임라인 정적 데이터 | 수동 QA: 타임라인 항목 표시 확인 |
| REQ-FUNC-061 | IMPLEMENT(간소화) | 대표 이미지에 URL과 alt 텍스트만 기록(EX-MEDIA로 라이선스 필드 축소) | 수동 QA: alt 텍스트 존재 확인 |
| REQ-FUNC-062 | IMPLEMENT | 문의·SNS 링크를 정적 설정값으로 제공, 빈 값은 렌더링 생략 | 수동 QA: 빈 링크 미노출 확인 |
| REQ-FUNC-063 | IMPLEMENT | 추천 여행지 6곳을 정적 데이터에서 선택해 여행지 상세로 연결 | Playwright smoke: 추천 여행지 링크 이동 |

### 4.7 F7. Common, Admin, Governance

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-FUNC-064 | IMPLEMENT | 전역 내비게이션·푸터에 핵심 화면과 정책 페이지 링크 배치 | Playwright smoke: 전역 내비게이션 이동 |
| REQ-FUNC-065 | IMPLEMENT | Tailwind 반응형 유틸리티로 320px~데스크톱 레이아웃 구성 | 수동 QA: 모바일/데스크톱 뷰포트 확인 |
| REQ-FUNC-066 | IMPLEMENT | Supabase Auth로 이메일 가입/인증/로그인/로그아웃/비밀번호 재설정 구현 | Playwright smoke: 가입-로그인-로그아웃 골든 패스 |
| REQ-FUNC-067 | EXCLUDED | EX-SCOPE — 여행지+안전정보 통합검색은 12개 필수 범위 밖, 여행지 검색(002/003)만 제공 | 해당 없음 |
| REQ-FUNC-068 | IMPLEMENT | `localStorage`에 즐겨찾기 목록 저장, 중복 방지 로직 포함(§2 원칙) | 수동 QA: 즐겨찾기 추가/해제/새로고침 유지 확인 |
| REQ-FUNC-069 | EXCLUDED | EX-SCOPE — Should 우선순위, Web Share API/URL 공유 기능은 12개 필수 범위 밖 | 해당 없음 |
| REQ-FUNC-070 | EXCLUDED | EX-SCOPE — canonical/OG/구조화 데이터 전면 적용은 12개 필수 범위 밖, Next.js 기본 title만 적용 | 해당 없음 |
| REQ-FUNC-071 | EXCLUDED | EX-SCOPE — 이벤트 분석 스키마·수집 파이프라인은 12개 필수 범위 밖 | 해당 없음 |
| REQ-FUNC-072 | EXCLUDED | EX-CMS — Editor/Admin CRUD·미리보기·상태(DRAFT/REVIEW 등) 전환 화면을 만들지 않음 | 해당 없음 |
| REQ-FUNC-073 | EXCLUDED | EX-MEDIA — 업로드 시 출처/작가/라이선스/URL 필수 입력 워크플로를 만들지 않음 | 해당 없음 |
| REQ-FUNC-074 | EXCLUDED | EX-CMS — 게시 전 완전성 자동 게이트를 만들지 않고 §4.1 REQ-FUNC-004 필드 체크리스트로 수동 대체 | 해당 없음 |
| REQ-FUNC-075 | EXCLUDED | EX-SCOPE — stale 현황 대시보드는 "간단한 관리자 탭"(신고·URL만) 범위 밖, stale 배지는 공개 페이지(050)에서 제공 | 해당 없음 |
| REQ-FUNC-076 | EXCLUDED | EX-AUDIT — 관리자 행위 전반에 대한 범용 감사 로그를 만들지 않음 | 해당 없음 |
| REQ-FUNC-077 | IMPLEMENT | 관리자 탭에서 항공·호텔 외부 URL을 HTTPS 허용목록으로만 저장(§1-10) | 수동 QA: HTTP/비허용 URL 저장 시도 차단 확인 |
| REQ-FUNC-078 | IMPLEMENT | Next.js 404/500/권한없음 페이지와 외부 연결 실패 시 재시도 UI 제공 | 수동 QA: 각 오류 화면 진입 및 복구 버튼 확인 |
| REQ-FUNC-079 | EXCLUDED | EX-SCOPE — 자동 접근성 검사(axe)와 수동 스크린리더 검증 절차는 12개 필수 범위 밖, 기본 시맨틱 HTML만 적용 | 해당 없음 |
| REQ-FUNC-080 | IMPLEMENT | 이용약관/개인정보 처리방침/동행 안전수칙/콘텐츠 면책 정적 페이지 제공, 모집글 작성 시 안전수칙 동의 시각 저장(031과 연계) | Playwright smoke: 동의 체크 없이 제출 차단 확인 |

---

## 5. 요구사항 매핑 — Non-Functional Requirements (REQ-NF-001~034)

### 5.1 Performance

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-001 | EXCLUDED | EX-OPS — 부하·필드데이터 기반 LCP 측정 파이프라인 미구축, Next.js 기본 최적화만 적용 | 해당 없음 |
| REQ-NF-002 | EXCLUDED | EX-OPS — INP 실사용자 측정 미구축 | 해당 없음 |
| REQ-NF-003 | EXCLUDED | EX-OPS — CLS 측정 미구축 | 해당 없음 |
| REQ-NF-004 | EXCLUDED | EX-OPS — 동시 사용자 50명 부하 테스트 미실시 | 해당 없음 |
| REQ-NF-005 | EXCLUDED | EX-OPS — 쓰기 API 부하 테스트 미실시 | 해당 없음 |
| REQ-NF-006 | IMPLEMENT | `next/image`의 반응형 크기·lazy load 기본 동작 사용, 주요 LCP 이미지에 `priority` 지정 | 수동 QA: 이미지 lazy load 동작 확인 |
| REQ-NF-007 | EXCLUDED | EX-OPS — Lighthouse CI 성능 게이트 미구축 | 해당 없음 |

### 5.2 Reliability and Recovery

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-008 | EXCLUDED | EX-OPS — 가용성 SLA 모니터링 미구축, Vercel 기본 인프라에 의존 | 해당 없음 |
| REQ-NF-009 | EXCLUDED | EX-OPS — 5xx 비율 모니터링 미구축 | 해당 없음 |
| REQ-NF-010 | EXCLUDED | EX-OPS(자동 백업 제외) — Supabase 기본 백업 정책에 의존, RPO/RTO 별도 설계 없음 | 해당 없음 |
| REQ-NF-011 | EXCLUDED | EX-OPS — 주 1회 자동 링크 점검 스케줄러 미구축, 관리자 수동 점검으로 대체 | 해당 없음 |

### 5.3 Security and Privacy

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-012 | IMPLEMENT | Vercel·Supabase 기본 HTTPS/TLS 1.2+ 사용 | 수동 QA: 배포 URL HTTPS 확인 |
| REQ-NF-013 | IMPLEMENT | Supabase Auth 세션 검증과 RLS 정책을 서버 측에서 적용(§4.4 REQ-FUNC-044) | 수동 QA: 권한 없는 계정 접근 시도 |
| REQ-NF-014 | IMPLEMENT | Next.js Server Actions 기본 CSRF 방어 및 SameSite 쿠키 사용 | 코드 리뷰: Server Actions 사용 확인 |
| REQ-NF-015 | IMPLEMENT | 폼 입력 검증과 React 기본 이스케이프로 저장 XSS 방지 | 수동 QA: 스크립트 태그 입력 테스트 |
| REQ-NF-016 | IMPLEMENT | Supabase 키 등 비밀값은 Vercel 환경변수로 관리, 클라이언트 번들 미포함 | 코드 리뷰: 빌드 산출물 내 비밀값 노출 여부 확인 |
| REQ-NF-017 | IMPLEMENT | 항공·호텔 입력값은 클라이언트 상태로만 처리(§4.2, §4.3) | 코드 리뷰: 서버 저장 경로 없음 확인 |
| REQ-NF-018 | EXCLUDED | EX-SCOPE — REQ-FUNC-045와 동일하게 개인정보 내보내기·삭제 파이프라인은 범위 밖 | 해당 없음 |

### 5.4 Safety and Moderation

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-019 | EXCLUDED | EX-OPS — 응답시간 p95 측정·부하 테스트 미실시, 기능 자체(039)는 IMPLEMENT | 해당 없음 |
| REQ-NF-020 | EXCLUDED | EX-SCOPE — 24시간 SLA 추적 체계 미구축, 관리자 탭은 상태 필터만 제공(041) | 해당 없음 |
| REQ-NF-021 | EXCLUDED | EX-OPS — 속도 제한(rate limiting) 인프라 미구축 | 해당 없음 |
| REQ-NF-022 | EXCLUDED | EX-AUDIT — Moderator 조치 추적용 감사 로그 미구축(042와 동일 사유) | 해당 없음 |

### 5.5 Accessibility

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-023 | EXCLUDED | EX-SCOPE — WCAG 2.2 AA 공식 준수 검증은 범위 밖, 기본 시맨틱 마크업만 적용 | 해당 없음 |
| REQ-NF-024 | EXCLUDED | EX-SCOPE — axe 자동 검사 파이프라인 미구축 | 해당 없음 |
| REQ-NF-025 | EXCLUDED | EX-SCOPE — 키보드·스크린리더 수동 검증 절차 미실시 | 해당 없음 |

### 5.6 Content, Freshness, SEO, Copyright

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-026 | IMPLEMENT | 정적 데이터 작성 시 REQ-FUNC-004 필드 체크리스트로 완전성 확보(자동 게이트 없음) | 수동 QA: 게시 콘텐츠 필드 체크리스트 검토 |
| REQ-NF-027 | IMPLEMENT | 소개 해외 15개국 전체 안전정보 정적 데이터 작성(046과 동일) | 수동 QA: 국가-안전정보 수 대응 확인 |
| REQ-NF-028 | IMPLEMENT(부분) | stale 배지 표시(050)는 구현하되 "7일 이내 95%" 수치 목표는 콘텐츠 운영 약속으로 코드 강제 대상 아님 | 수동 QA: stale 배지 렌더 확인, 수치 목표는 운영 체크리스트로 별도 관리 |
| REQ-NF-029 | EXCLUDED | EX-MEDIA — 라이선스 유형·작가 등 미디어 메타데이터 100% 수집을 하지 않고 URL+alt만 기록 | 해당 없음 |
| REQ-NF-030 | EXCLUDED | EX-SCOPE — REQ-FUNC-070과 동일하게 전면 SEO 메타데이터는 범위 밖 | 해당 없음 |

### 5.7 Maintainability, Monitoring, Cost

| ID | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|
| REQ-NF-031 | IMPLEMENT(부분) | TypeScript strict·ESLint는 기존 스캐폴드 설정 유지·통과 필수, 단위 테스트 대신 Playwright 핵심 Smoke Test로 대체(§1-11) | CI: `lint`/`build` 통과, Playwright smoke 실행 결과 |
| REQ-NF-032 | EXCLUDED | EX-OPS — 구조화 로그 체계 미구축 | 해당 없음 |
| REQ-NF-033 | EXCLUDED | EX-OPS(장애 알림 제외) — 5xx·외부 링크 실패 자동 알림 미구축 | 해당 없음 |
| REQ-NF-034 | IMPLEMENT | Vercel·Supabase 무료/최소 티어 사용으로 월 인프라 비용을 100,000원 이하로 유지 | 수동 QA: 사용 중인 플랜·과금 항목 확인 |

---

## 6. 요약

| 구분 | 건수 |
|---|---|
| REQ-FUNC 전체 | 80건 (001~080) |
| REQ-FUNC IMPLEMENT | 64건 |
| REQ-FUNC EXCLUDED | 16건 |
| REQ-NF 전체 | 34건 (001~034) |
| REQ-NF IMPLEMENT | 12건 |
| REQ-NF EXCLUDED | 22건 |

> 본 문서는 PRD/SRS의 모든 요구사항 ID를 삭제 없이 그대로 보존하며, MVP 구현 여부와 그 근거만 추가한다. SRS 본문의 우선순위(M/S/C)와 수용 기준은 `02_SRS_BASELINE.md`를 기준 문서로 유지한다.
