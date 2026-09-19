# PAGE-SCR005 — SCR-005 계정·관리 페이지 조립

- Seq: 54
- Category: PAGE
- Implementation Status: IMPLEMENT
- Priority: P0

## Context

`TASKS/00_TASK_LIST.md`(Seq 54, Category PAGE)에 정의된 Task를 실제로 개발 가능한 단위로 구체화한 문서다. 이 Task는 "SCR-005 계정·관리 페이지 조립"을(를) 다룬다. 대상 Screen은 계정·관리(`/account`)이며 Route는 `/account`다. 기반 문서: `docs/06_SRS_UIUX_REVISED.md`(요구사항 원문), `docs/PROJECT_SCOPE.md`(구현 범위 판단), `design-reference/D-001/DESIGN.md`·`design-reference/UI_CONTRACT.md`(디자인 계약), `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Project Scope

`docs/PROJECT_SCOPE.md`의 요구사항 분류 기준으로 이 Task의 Implementation Status는 **IMPLEMENT**다. 이 Task에 결부된 Requirement(REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-066, REQ-FUNC-077)는 EXCLUDED가 아니므로 구현 대상이며, `TASKS/00_TASK_LIST.md` §8 NON_IMPLEMENTATION Register에는 등장하지 않는다.

## Requirement Ref

- REQ-FUNC-028
- REQ-FUNC-029
- REQ-FUNC-036
- REQ-FUNC-038
- REQ-FUNC-040
- REQ-FUNC-041
- REQ-FUNC-066
- REQ-FUNC-077

## Screen / Route / Page Entry

- Screen: SCR-005
- Route: `/account`
- Page Entry: `src/app/account/page.tsx`

## Design Ref

- `design-reference/D-001/DESIGN.md` §1 Visual Theme, §2 Color Token, §3 Typography, §4 Spacing, §5 Radius, §6 Shadow — 코랄(`#F0603F`) 포인트, semantic 색 분리, 8~20px 라운드, 단일 그림자 티어 준수
- `design-reference/D-001/DESIGN.md` §7 Header·Footer, §14 Desktop·Mobile 규칙, §15 Section 최대 폭·여백, §17 Section 계층·리듬
- `design-reference/UI_CONTRACT.md` 계정·관리(`/account`) 절
- `design-reference/D-001/DESIGN.md` §13 Loading·Empty·Error 상태, §19 완성형 Empty State·Placeholder 금지 규칙

## Depends On

- CMP-SCR005-AUTH
- CMP-SCR005-PROFILE
- CMP-SCR005-MY-ACTIVITY
- CMP-SCR005-ADMIN
- CMP-SCR005-ROLE-SHELL
- CMP-SHARED-HEADER-FOOTER
- CMP-SHARED-TOAST
- AUTH-SUPABASE-SETUP
- DB-ACCESS

## Expected Files

- 신규 생성: `src/app/account/page.tsx`
- 위 목록 밖의 파일은 이 Task 범위에서 수정하지 않는다.

## Functional AC

- [ ] 역할별 Section: **Guest** → 계정 기능 Intro+로그인·가입·비밀번호 재설정 Card+로그인 후 가능한 기능 안내+보안 안내 / **Member** → 프로필 요약+수정 Form, 내 활동(내가 쓴 동행글+새 글 CTA, 참가 요청 목록+승인·거절, 차단 목록+해제) / **Admin(Member 탭에 추가)** → 관리 Intro, 신고 목록+상태 필터(OPEN/REVIEWING/RESOLVED/DISMISSED)+행별 상태 변경, 항공·숙소 외부 URL 설정 Form(HTTPS만 허용)
- [ ] **Guest·Member·Admin 3개 역할 상태가 각각 실제 콘텐츠로 조립된다.** 역할에 없는 탭·영역은 DOM에 렌더링되지 않는다(예: Guest에게 관리자 탭이 아예 존재하지 않음)
- [ ] 데이터 출처: 프로필/내 글/참가요청/차단 = `user_profile`/`mate_post`/`mate_application`/`user_block`(DB-ACCESS), 신고 목록 = `report`, 외부 URL = `outbound_url_setting`

## Visual AC

- [ ] Desktop 좌측 세로 탭(폭 240px)+우측 콘텐츠(최대 1000px), Mobile 상단 가로 스크롤 탭+콘텐츠 풀폭
- [ ] 통계 Dashboard(차트·그래프)를 만들지 않고 목록·필터·폼으로만 구성한다
- [ ] 큰 빈 영역·Lorem ipsum·"준비 중"·"정보 확인 필요" 금지
- [ ] 내 글·참가요청·차단·신고 목록이 0건이면 각각 "아직 ~이 없어요" 안내 문장 + 다음 행동(글 작성, 다음 확인 주기 등) CTA를 갖춘 완성형 Empty State를 표시한다

## Security/Privacy AC

- [ ] 정확한 생년월일은 저장하지 않고 `is_adult`, `adult_verified_at`만 저장한다(REQ-FUNC-028)
- [ ] RLS로 본인 데이터·Admin만 비공개 데이터를 조회한다(`DB-RLS-BASE`)
- [ ] 외부 URL은 HTTPS 허용목록 검증을 통과해야 저장된다(REQ-FUNC-077)

## Test Cases

- TC-FUNC-028: 대응하는 Functional AC 시나리오를 재현해 통과 여부를 확인한다.

## Verify

- TC-FUNC-028, 029, 036, 038, 040, 041, 066, 077 + `E2E-MATE-AUTH`

## Definition of Done

- [ ] Functional AC·Visual AC·Security/Privacy AC 항목이 모두 충족되어 체크된다.
- [ ] Expected Files에 명시된 파일만 신규 생성/수정되었고 그 밖의 파일은 건드리지 않았다.
- [ ] 연결된 Requirement(REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-066, REQ-FUNC-077)가 `docs/UIUX_TRACEABILITY.md` 상태와 모순되지 않는다.
- [ ] Test Cases(TC-FUNC-028)가 통과한다.
- [ ] Depends On의 모든 Component/Data/Auth/DB Task가 완료된 뒤 이 Screen에 실제로 조립되어 있다(신규 Component 생성 아님).
- [ ] Guest/Member/Admin 3개 역할 상태가 각각 실제로 조립되어 있고 역할 밖 탭은 렌더링되지 않는다.
- [ ] 이 Task 수행 중 구현 코드 이외의 Git Branch/Commit이 생성되지 않았다(계획 단계 산출물인 경우 코드 자체도 생성하지 않는다).

## Forbidden

- Expected Files 목록 밖의 파일을 수정하지 않는다.
- 이 Task 수행 과정에서 Git Branch·Commit을 생성하지 않는다(계획/구현 산출물만 만든다).
- Lorem ipsum·"준비 중"·"정보 확인 필요" 문구나 내용 없는 빈 Card를 남기지 않는다.
- Airbnb 상표 요소, 구매·예약·결제 UI, 실시간 가격·별점·광고를 추가하지 않는다(`design-reference/D-001/DESIGN.md` §20).
- 역할(Guest/Member/Admin)에 없는 탭·영역을 DOM에 렌더링하지 않는다.
- 통계 Dashboard(차트·그래프)를 추가하지 않는다.
