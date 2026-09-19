# Free Traveler — Wave Plan

`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK-*.md`·`design-reference/SCREEN_ROUTE_CONTRACT.json`을 근거로 생성했다. `/run-wave`는 이 문서와 `TASKS/WAVE_STATE.json`을 정본으로 사용한다.

## Wave 요약

| Wave | 그룹 | Task 수 | Preview Checkpoint |
|---|---|---:|:---:|
| W01 | Airbnb 스타일 공통 UI, 정적 데이터, Layout | 3 |  |
| W02 | Airbnb 스타일 공통 UI, 정적 데이터, Layout | 3 |  |
| W03 | Supabase Auth, 6개 Table, 기본 RLS | 1 |  |
| W04 | Supabase Auth, 6개 Table, 기본 RLS | 3 |  |
| W05 | Supabase Auth, 6개 Table, 기본 RLS | 2 |  |
| W06 | SCR-001 메인 Component와 Page Owner | 7 |  |
| W07 | SCR-001 메인 Component와 Page Owner | 3 |  |
| W08 | SCR-001 메인 Component와 Page Owner — Page Owner 통합 | 1 | Y |
| W09 | SCR-002 대표 소개 Component와 Page Owner | 7 |  |
| W10 | SCR-002 대표 소개 Component와 Page Owner | 1 |  |
| W11 | SCR-002 대표 소개 Component와 Page Owner — Page Owner 통합 | 1 | Y |
| W12 | SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 1 |  |
| W13 | SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 1 |  |
| W14 | SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 4 |  |
| W15 | SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner | 1 |  |
| W16 | SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner — Page Owner 통합 | 1 | Y |
| W17 | SCR-004 동행 목록·상세·신청 Component와 Page Owner | 2 |  |
| W18 | SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 |  |
| W19 | SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 |  |
| W20 | SCR-004 동행 목록·상세·신청 Component와 Page Owner | 2 |  |
| W21 | SCR-004 동행 목록·상세·신청 Component와 Page Owner | 1 |  |
| W22 | SCR-004 동행 목록·상세·신청 Component와 Page Owner — Page Owner 통합 | 1 | Y |
| W23 | SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner | 5 |  |
| W24 | SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner — Page Owner 통합 | 1 | Y |
| W25 | Unit·Playwright·접근성·CI | 7 |  |
| W26 | Unit·Playwright·접근성·CI | 1 |  |
| W27 | Vercel Preview와 Release 확인 | 2 |  |

## Wave별 Task 목록

| Wave | Task ID | Preview Checkpoint |
|---|---|---|
| W01 | CMP-SHARED-HEADER-FOOTER |  |
| W01 | CMP-SHARED-TOAST |  |
| W01 | DATA-DESTINATIONS |  |
| W02 | CMP-SHARED-ERROR-PAGES |  |
| W02 | DATA-REPRESENTATIVE |  |
| W02 | DATA-SAFETY |  |
| W03 | DB-SCHEMA-BASE |  |
| W04 | AUTH-SUPABASE-SETUP |  |
| W04 | DB-RLS-BASE |  |
| W04 | DB-SEED-BASE |  |
| W05 | AUTH-ADULT-VERIFICATION |  |
| W05 | DB-ACCESS |  |
| W06 | CMP-SCR001-DEST-DOMESTIC |  |
| W06 | CMP-SCR001-DEST-DRAWER |  |
| W06 | CMP-SCR001-DEST-OVERSEAS |  |
| W06 | CMP-SCR001-FOUNDER-SUMMARY |  |
| W06 | CMP-SCR001-HERO |  |
| W06 | CMP-SCR001-RECENT-MATES |  |
| W06 | CMP-SCR001-SAFETY-DRAWER |  |
| W07 | CMP-SCR001-FAVORITES |  |
| W07 | CMP-SCR001-SAFETY-GRID |  |
| W07 | CMP-SCR001-THEME-CHIPS |  |
| W08 | PAGE-SCR001 | Y |
| W09 | CMP-SCR002-CONTACT-LINKS |  |
| W09 | CMP-SCR002-COUNTRIES |  |
| W09 | CMP-SCR002-GALLERY |  |
| W09 | CMP-SCR002-HERO |  |
| W09 | CMP-SCR002-INTRO |  |
| W09 | CMP-SCR002-STATS |  |
| W09 | CMP-SCR002-TIMELINE |  |
| W10 | CMP-SCR002-TOP-PICKS |  |
| W11 | PAGE-SCR002 | Y |
| W12 | CMP-SCR003-INTRO |  |
| W13 | CMP-SCR003-TABS |  |
| W14 | CMP-SCR003-FLIGHT-FORM |  |
| W14 | CMP-SCR003-HOTEL-FORM |  |
| W14 | CMP-SCR003-MATE-LOGIN-PROMPT |  |
| W14 | CMP-SCR003-MATE-WRITE |  |
| W15 | CMP-SCR003-TIPS |  |
| W16 | PAGE-SCR003 | Y |
| W17 | CMP-SCR004-FILTER |  |
| W17 | CMP-SCR004-INTRO |  |
| W18 | CMP-SCR004-LIST |  |
| W19 | CMP-SCR004-DETAIL |  |
| W20 | CMP-SCR004-APPLICATION |  |
| W20 | CMP-SCR004-REPORT |  |
| W21 | CMP-SCR004-SAFETY-NOTICE |  |
| W22 | PAGE-SCR004 | Y |
| W23 | CMP-SCR005-ADMIN |  |
| W23 | CMP-SCR005-AUTH |  |
| W23 | CMP-SCR005-MY-ACTIVITY |  |
| W23 | CMP-SCR005-PROFILE |  |
| W23 | CMP-SCR005-ROLE-SHELL |  |
| W24 | PAGE-SCR005 | Y |
| W25 | E2E-MATE-AUTH |  |
| W25 | E2E-PUBLIC-SMOKE |  |
| W25 | E2E-TRAVEL-TOOLS |  |
| W25 | TEST-RLS-BASIC |  |
| W25 | UNIT-CONTACT-DETECTION |  |
| W25 | UNIT-MATE-STATE |  |
| W25 | UNIT-TRAVEL-DATES |  |
| W26 | CI-LINT-BUILD |  |
| W27 | DEPLOY-SUPABASE-CHECK |  |
| W27 | DEPLOY-VERCEL |  |

## 참고

- Wave ID는 그룹 순서(1. Scaffold/문서/Harness → 10. Vercel Preview/Release)에 따라 순차 부여되었으며 W00~W10으로 미리 고정되지 않았다.
- Page Owner(PAGE-*) Task는 해당 화면 그룹의 마지막 Wave에 단독 배치되고 `Preview Checkpoint=Y`다(`CLAUDE.md` 규칙 22).
- DB/AUTH 그룹처럼 의존 사슬이 긴 구간은 4~7개 기본 범위보다 작은 Wave가 발생할 수 있다(의존 순서 정확성이 우선).
- 이 문서는 계획 문서다. 자동 Branch 생성·PR 생성·Merge 기능은 포함하지 않는다.
