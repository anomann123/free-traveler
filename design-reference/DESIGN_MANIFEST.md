# Design Manifest

**Active Design Version:** D-001
**Status:** LOCKED
**Active File:** `design-reference/D-001/DESIGN.md`
**Vendor Reference:** `design-reference/vendor/airbnb/DESIGN.md`
**Locked Date:** 2026-09-19

---

## Approved Screens

| Screen | Route | Device | Status | Screen ID(Stitch, canonical) |
|---|---|---|---|---|
| SCR-001 | `/` 메인 | Desktop 1440 | Approved | `a482ca45c55c4ebab0c51f2b9925ffa1` |
| SCR-002 | `/about` 대표 소개 | Desktop 1440 | Approved | `4fb00e0ddafe48f6a5e939adde28ec83` |
| SCR-003 | `/travel-tools` 통합 여행 준비 | Desktop 1440 | Approved | `7be58bc38217407faa6fefd9a8e303f8` |
| SCR-004 | `/mates` 동행 조회 | Desktop 1440 | Approved | `f16524ce9c2f4428b840f56e473567cf` |
| SCR-005 | `/account` 계정·관리 | Desktop 1440 | Approved | `c60112d500414a07961b82edd72409f1` |

## Mobile Variants

| Screen | Device | Status | Screen ID(Stitch, canonical) |
|---|---|---|---|
| SCR-001 | Mobile 390 | Approved | `9f862d3f881f4bb7950e3e529b7d93f1` |
| SCR-003 | Mobile 390 | Approved | `3e4e85ab173c49debea20fb05e92a92f` |

> SCR-002, SCR-004, SCR-005는 Mobile 변형이 이번 승인 범위에 포함되지 않는다. Stitch 프로젝트 재조회 결과 SCR-001 Mobile·SCR-004 Desktop·SCR-005 Desktop에 중복 화면이 남아 있으며(`docs/STITCH_VALIDATION_REPORT.md` §1, §4 참조), 이 표의 Screen ID는 그중 승인된 canonical 화면만을 가리킨다. 나머지 중복 화면은 Stitch UI에서 소유자가 직접 삭제해야 한다.

## Source Documents

| 문서 | 역할 |
|---|---|
| `docs/04_UIUX_PLAN.md` | Screen별 Section 계약, 상태(State) 정의, 반응형 규칙의 1차 근거 |
| `docs/STITCH_VALIDATION_REPORT.md` | 위 5개 Screen + 2개 Mobile 변형의 PASS 판정 근거, 수정 이력(SCR-002 한국어 라벨링, SCR-005 Admin 영역 추가) |
| `design-reference/vendor/airbnb/DESIGN.md` | 레이아웃 문법(카드 밀도, 1단계 그림자, 여백 리듬) 참고용 원본 — 색상·폰트·상표는 인용하지 않음 |
| `design-reference/D-001/DESIGN.md` | 위 세 문서를 종합한 Traveler 전용 디자인 정본(현재 LOCKED 버전) |

## Governance

- **LOCKED 상태 의미:** `design-reference/D-001/DESIGN.md`의 Color Token·Typography·Spacing·Radius·Shadow·Section 계약은 별도 버전(D-002 등) 없이 임의로 수정하지 않는다.
- **변경 절차:** 토큰이나 Section 계약을 바꿔야 할 경우, 새 버전 디렉터리(`design-reference/D-002/`)를 만들고 이 Manifest의 `Active Design Version`/`Active File`을 갱신한 뒤 이전 버전은 보관용으로 남긴다. D-001 파일을 직접 덮어써서 이력 없이 변경하지 않는다.
- **금지 사항(전 버전 공통):**
  - Airbnb 상표 요소(로고·워드마크·문구·색상·폰트) 사용 금지
  - 구매·예약·결제 UI(가격 표시, 결제 수단, 발권/체크아웃) 추가 금지
  - Proprietary 폰트 파일 번들 금지 — Inter + OS 기본 한글 폰트만 허용
  - `design-reference/D-001/DESIGN.md`의 Color Token 표에 없는 임의 색상 추가 금지
