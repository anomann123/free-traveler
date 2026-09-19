#!/usr/bin/env python3
"""check_screen_contract.py

5개 고정 Screen(SCR-001~005)이 계획·구현 단계에서 계약을 벗어나지 않았는지 검사한다.

입력:
    design-reference/SCREEN_ROUTE_CONTRACT.json
    TASKS/TASK_MANIFEST.csv
    src/app (mode=ci/release에서만 실제 파일 트리를 읽는다)

실행 모드(`--mode` 또는 `npm run screen:contract -- --mode=ci`처럼 전달):
    plan     Page Owner와 경로 "계획"만 검사한다(계약 JSON + Task Manifest만 읽는다,
             src/app 파일 트리는 읽지 않는다). 기본값.
    ci       plan의 모든 검사에 더해, 실제 구현된 Page 파일(src/app/**/page.tsx)과
             공개 경로가 계약과 일치하는지 검사한다.
    release  ci의 모든 검사에 더해, 5개 Screen 전부 `docs/preview-checks/SCR-00N.md`
             Preview 확인 기록이 존재하는지 검사한다.

검사 항목(번호는 이 스크립트와 출력 보고에서 동일):
    1  고정 Screen 5개(SCR-001~005)가 계약·Manifest에 정확히 존재
    2  각 Screen의 Page Owner Task가 정확히 1개
    3  기술 경로(/auth/callback, /api/**, not-found)를 사용자 Screen으로 세지 않음
    4  여행지 상세·안전정보 등 통합 이전 Route가 새 Page로 재생성되지 않음
    5  SCR-003 Task가 여행 입력(항공·숙소 Form)과 동행 작성 양쪽을 모두 포함
    6  (release 전용) docs/preview-checks/SCR-001.md ~ SCR-005.md Preview 확인 기록 존재

오류가 있으면 관련 파일·Screen ID·수정 힌트를 포함해 출력하고 exit code 1로 끝낸다.
모두 통과하면 `SCREEN_CONTRACT_PASS <mode>`를 출력하고 exit code 0으로 끝낸다.

사용법:
    python scripts/check_screen_contract.py [--mode plan|ci|release]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = ROOT / "design-reference" / "SCREEN_ROUTE_CONTRACT.json"
MANIFEST_PATH = ROOT / "TASKS" / "TASK_MANIFEST.csv"
APP_DIR = ROOT / "src" / "app"
PREVIEW_CHECKS_DIR = ROOT / "docs" / "preview-checks"

FIXED_SCREENS = {
    "SCR-001": "/",
    "SCR-002": "/about",
    "SCR-003": "/travel-tools",
    "SCR-004": "/mates",
    "SCR-005": "/account",
}

# 기술 경로(사용자 Screen으로 세지 않음). route는 SCREEN_ROUTE_CONTRACT.json의
# technical_routes[].route 표기와 동일하게 둔다.
ALLOWED_TECHNICAL_ROUTES = {"/auth/callback", "/api/*", "not-found"}

# UI 통합 이전(구 Route Inventory, docs/06_SRS_UIUX_REVISED.md §2) 경로 중
# 5개 고정 Screen으로 흡수되어 더 이상 별도 Page로 만들면 안 되는 패턴.
# src/app 기준 상대 경로(page.tsx의 상위 디렉터리)에 대한 정규식이다.
FORBIDDEN_LEGACY_PAGE_PATTERNS = [
    (re.compile(r"^destinations(/.*)?$"), "여행지 목록/상세는 SCR-001의 Card Grid + Drawer로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^safety(/.*)?$"), "국가 안전정보는 SCR-001의 Card Grid + Drawer로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^flights$"), "항공 조건 입력은 SCR-003 `/travel-tools`의 탭으로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^hotels$"), "숙소 조건 입력은 SCR-003 `/travel-tools`의 탭으로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^mates/new$"), "동행 모집글 작성은 SCR-003 `/travel-tools`의 동행 구하기 탭으로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^mates/\[.+\]$"), "동행 모집글 상세는 SCR-004 `/mates`의 목록·상세 분할(Drawer)로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^my(/.*)?$"), "내 활동(내 글/참가요청/차단)은 SCR-005 `/account`의 Member 탭으로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^admin(/.*)?$"), "관리자 기능(신고 상태·외부 URL)은 SCR-005 `/account`의 Admin 탭으로 통합되어야 한다(별도 Page 금지)"),
    (re.compile(r"^auth(?!/callback$)(/.*)?$"), "인증 화면(가입/로그인/재설정)은 SCR-005 `/account`의 Guest 탭으로 통합되어야 한다(auth/callback 콜백 Route Handler 제외, 별도 Page 금지)"),
]


@dataclass
class Violation:
    check: int
    screen_id: str | None
    file: str | None
    message: str
    hint: str


@dataclass
class Report:
    mode: str
    violations: list[Violation] = field(default_factory=list)

    def fail(self, check: int, message: str, *, screen_id: str | None = None, file: str | None = None, hint: str = "") -> None:
        self.violations.append(Violation(check, screen_id, file, message, hint))


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_contract() -> dict:
    if not CONTRACT_PATH.exists():
        print(f"[FATAL] {CONTRACT_PATH} 가 없습니다.")
        sys.exit(1)
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def load_manifest() -> list[dict]:
    if not MANIFEST_PATH.exists():
        print(f"[FATAL] {MANIFEST_PATH} 가 없습니다. 먼저 `python scripts/audit_tasks.py`(= npm run task:contract)를 실행하십시오.")
        sys.exit(1)
    with MANIFEST_PATH.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def split_cell_list(cell: str) -> list[str]:
    if not cell or cell.strip() in ("없음", "N/A", "-", ""):
        return []
    return [c.strip() for c in cell.split(",") if c.strip()]


# ---------------------------------------------------------------------------
# Checks (plan-level: 계약 JSON + Task Manifest만 사용)
# ---------------------------------------------------------------------------

def check_1_fixed_screens_exist(report: Report, contract: dict, manifest: list[dict]) -> None:
    contract_screens = {s["screen_id"]: s.get("route", "") for s in contract.get("screens", [])}
    for sid, route in FIXED_SCREENS.items():
        if sid not in contract_screens:
            report.fail(1, f"SCREEN_ROUTE_CONTRACT.json에 {sid}가 없음", screen_id=sid,
                        file=str(CONTRACT_PATH.relative_to(ROOT)),
                        hint=f"screens[] 배열에 screen_id='{sid}', route='{route}' 항목을 추가하십시오.")
        elif contract_screens[sid] != route:
            report.fail(1, f"{sid}의 Route가 계약과 다름: 계약='{contract_screens[sid]}' vs 고정값='{route}'",
                        screen_id=sid, file=str(CONTRACT_PATH.relative_to(ROOT)),
                        hint=f"route를 '{route}'로 수정하십시오.")
    extra = sorted(set(contract_screens) - set(FIXED_SCREENS))
    if extra:
        report.fail(1, f"고정 5개 Screen 외 추가 Screen이 계약에 존재: {extra}",
                    file=str(CONTRACT_PATH.relative_to(ROOT)),
                    hint="5개 고정 Screen 외 신규 Screen을 추가하려면 사용자 승인 후 이 스크립트의 FIXED_SCREENS부터 갱신해야 한다.")
    if len(contract.get("screens", [])) != 5:
        report.fail(1, f"계약의 screens 배열 길이가 5가 아님: {len(contract.get('screens', []))}",
                    file=str(CONTRACT_PATH.relative_to(ROOT)), hint="screens 배열을 정확히 5개 항목으로 맞추십시오.")

    manifest_screen_ids = {(row.get("Screen") or "").strip() for row in manifest}
    known_non_screen = {"", "전역", "N/A"}
    unknown_screens = sorted(
        s for s in manifest_screen_ids
        if s not in known_non_screen and not any(sid in s for sid in FIXED_SCREENS)
    )
    if unknown_screens:
        report.fail(1, f"TASK_MANIFEST.csv에 고정 5개 Screen과 매칭되지 않는 Screen 값 존재: {unknown_screens}",
                    file=str(MANIFEST_PATH.relative_to(ROOT)),
                    hint="Task의 Screen 열이 SCR-001~005 중 하나를 정확히 포함하도록 수정하거나, 전역/N/A로 표기하십시오.")


def check_2_page_owner_exactly_one(report: Report, manifest: list[dict]) -> dict[str, list[str]]:
    po_by_screen: dict[str, list[str]] = {sid: [] for sid in FIXED_SCREENS}
    for row in manifest:
        tid = (row.get("Task ID") or "").strip()
        category = (row.get("Category") or "").strip()
        screen_val = (row.get("Screen") or "").strip()
        if category != "PAGE" and not tid.startswith(("PAGE-", "PO-")):
            continue
        matched = next((sid for sid in FIXED_SCREENS if sid in screen_val), None)
        if matched is None:
            report.fail(2, f"Page Owner Task '{tid}'의 Screen 값('{screen_val}')이 고정 5개 Screen과 매칭되지 않음",
                        file=str(MANIFEST_PATH.relative_to(ROOT)),
                        hint="Screen 열을 SCR-001~005 중 정확히 하나로 수정하십시오.")
            continue
        po_by_screen[matched].append(tid)

    for sid, owners in po_by_screen.items():
        if len(owners) == 0:
            report.fail(2, f"{sid}에 Page Owner Task가 없음", screen_id=sid,
                        file=str(MANIFEST_PATH.relative_to(ROOT)),
                        hint=f"{sid}({FIXED_SCREENS[sid]})를 조립하는 Category=PAGE Task를 Task List에 추가하십시오.")
        elif len(owners) > 1:
            report.fail(2, f"{sid}에 Page Owner Task가 {len(owners)}개 존재: {owners}", screen_id=sid,
                        file=str(MANIFEST_PATH.relative_to(ROOT)),
                        hint="Page Owner는 화면당 정확히 1개여야 한다. 중복 Task를 통합하거나 하나만 PAGE로 남기십시오.")
    return po_by_screen


def check_3_technical_routes_not_counted(report: Report, contract: dict) -> None:
    entries = contract.get("technical_routes", [])

    def has_auth_callback() -> bool:
        return any(t.get("route", "") == "/auth/callback" for t in entries)

    def has_api_wildcard() -> bool:
        return any(t.get("route", "").startswith("/api") for t in entries)

    def has_not_found() -> bool:
        return any("not-found" in t.get("page_entry", "") for t in entries)

    matchers = {
        "/auth/callback": has_auth_callback,
        "/api/*": has_api_wildcard,
        "not-found": has_not_found,
    }
    for route, matcher in matchers.items():
        if not matcher():
            report.fail(3, f"허용 기술 경로 '{route}'가 SCREEN_ROUTE_CONTRACT.json technical_routes에 없음",
                        file=str(CONTRACT_PATH.relative_to(ROOT)),
                        hint="technical_routes[]에 해당 경로를 counted_as_screen=false로 등록하십시오.")
    for t in contract.get("technical_routes", []):
        if t.get("counted_as_screen", False):
            report.fail(3, f"기술 경로 '{t.get('route')}'가 counted_as_screen=true로 설정되어 있음(사용자 Screen으로 셈)",
                        file=str(CONTRACT_PATH.relative_to(ROOT)),
                        hint="counted_as_screen을 false로 수정하십시오.")
    if len(contract.get("screens", [])) + len(contract.get("technical_routes", [])) < 5:
        report.fail(3, "계약에 등록된 Screen+기술 경로 합계가 5보다 작음(기술 경로가 Screen 자리를 대신 차지했을 가능성)",
                    file=str(CONTRACT_PATH.relative_to(ROOT)), hint="screens[]와 technical_routes[]를 분리해 다시 등록하십시오.")


def check_5_scr003_covers_both(report: Report, manifest: list[dict]) -> None:
    scr003_ids = {
        (row.get("Task ID") or "").strip()
        for row in manifest
        if "SCR-003" in (row.get("Screen") or "")
    }
    has_travel_input = any(re.search(r"FLIGHT-FORM|HOTEL-FORM", tid) for tid in scr003_ids)
    has_mate_write = any("MATE-WRITE" in tid for tid in scr003_ids)
    if not has_travel_input:
        report.fail(5, "SCR-003에 항공·숙소 조건 입력(FLIGHT-FORM/HOTEL-FORM) Task가 없음", screen_id="SCR-003",
                    file=str(MANIFEST_PATH.relative_to(ROOT)),
                    hint="CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM Task를 Task List/Manifest에 추가하십시오.")
    if not has_mate_write:
        report.fail(5, "SCR-003에 동행 작성(MATE-WRITE) Task가 없음", screen_id="SCR-003",
                    file=str(MANIFEST_PATH.relative_to(ROOT)),
                    hint="CMP-SCR003-MATE-WRITE Task를 Task List/Manifest에 추가하십시오.")


# ---------------------------------------------------------------------------
# Checks (구현 단계: src/app 파일 트리를 실제로 읽는다 — mode=ci/release)
# ---------------------------------------------------------------------------

def scan_app_pages() -> dict[str, Path]:
    """src/app 아래 모든 page.tsx를 찾아 {route_key: path} 로 반환한다.
    route_key는 src/app 기준 상대 디렉터리 경로(POSIX 구분자, 루트는 '')다."""
    pages: dict[str, Path] = {}
    if not APP_DIR.exists():
        return pages
    for page_file in APP_DIR.rglob("page.tsx"):
        rel_dir = page_file.parent.relative_to(APP_DIR)
        key = "" if str(rel_dir) == "." else rel_dir.as_posix()
        pages[key] = page_file
    return pages


def route_key_for(route: str) -> str:
    return "" if route == "/" else route.lstrip("/")


def check_1_ci_pages_exist(report: Report, po_by_screen: dict[str, list[str]]) -> None:
    pages = scan_app_pages()
    for sid, route in FIXED_SCREENS.items():
        key = route_key_for(route)
        if key not in pages:
            report.fail(1, f"{sid}({route})의 Page Entry가 아직 구현되지 않음(src/app/{key or '(root)'}/page.tsx 없음)",
                        screen_id=sid,
                        hint=f"{po_by_screen.get(sid, ['(Page Owner 없음)'])[0]} Task를 완료해 page.tsx를 생성하십시오.")


def check_3_4_ci_extra_pages(report: Report) -> None:
    pages = scan_app_pages()
    fixed_keys = {route_key_for(r) for r in FIXED_SCREENS.values()}
    for key, path in sorted(pages.items()):
        if key in fixed_keys:
            continue
        rel_file = str(path.relative_to(ROOT))
        legacy_hit = next((hint for pat, hint in FORBIDDEN_LEGACY_PAGE_PATTERNS if pat.match(key)), None)
        if legacy_hit:
            report.fail(4, f"통합 이전 Route가 새 Page로 재생성됨: src/app/{key}/page.tsx",
                        file=rel_file, hint=legacy_hit)
        else:
            report.fail(3, f"고정 5개 Screen·허용 기술 경로 어디에도 없는 미승인 Page 발견: src/app/{key}/page.tsx",
                        file=rel_file,
                        hint="이 Page가 정말 필요하면 먼저 SCREEN_ROUTE_CONTRACT.json과 사용자 승인을 거쳐야 한다. "
                             "그렇지 않으면 삭제하고 기존 5개 Screen의 Section/Drawer/Tab으로 흡수하십시오.")


def check_6_release_preview_checks(report: Report) -> None:
    for sid in FIXED_SCREENS:
        path = PREVIEW_CHECKS_DIR / f"{sid}.md"
        if not path.exists():
            report.fail(6, f"{sid} Preview 확인 기록이 없음", screen_id=sid,
                        file=str(path.relative_to(ROOT)),
                        hint=f"사람이 Vercel Preview에서 {sid}({FIXED_SCREENS[sid]})를 확인한 뒤 "
                             f"'docs/preview-checks/{sid}.md'에 확인 기록(확인자·시각·결과)을 작성하십시오.")
        elif path.stat().st_size == 0:
            report.fail(6, f"{sid} Preview 확인 기록 파일이 비어 있음", screen_id=sid,
                        file=str(path.relative_to(ROOT)),
                        hint="빈 파일이 아니라 실제 확인 내용을 기록하십시오.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="5개 고정 Screen 계약 검사")
    parser.add_argument("--mode", choices=["plan", "ci", "release"], default="plan")
    args = parser.parse_args()

    contract = load_contract()
    manifest = load_manifest()
    report = Report(mode=args.mode)

    # plan 단계 검사(모든 모드 공통 — 계약 JSON + Task Manifest만 사용)
    check_1_fixed_screens_exist(report, contract, manifest)
    po_by_screen = check_2_page_owner_exactly_one(report, manifest)
    check_3_technical_routes_not_counted(report, contract)
    check_5_scr003_covers_both(report, manifest)

    if args.mode in ("ci", "release"):
        check_1_ci_pages_exist(report, po_by_screen)
        check_3_4_ci_extra_pages(report)

    if args.mode == "release":
        check_6_release_preview_checks(report)

    print(f"=== check_screen_contract.py (mode={args.mode}) ===")
    if not report.violations:
        print(f"SCREEN_CONTRACT_PASS {args.mode}")
        return 0

    by_check: dict[int, list[Violation]] = {}
    for v in report.violations:
        by_check.setdefault(v.check, []).append(v)

    for check_num in sorted(by_check):
        print(f"\n[FAIL] 검사 #{check_num}")
        for v in by_check[check_num]:
            print(f"  - 화면: {v.screen_id or '해당 없음'}")
            print(f"    파일: {v.file or '해당 없음'}")
            print(f"    문제: {v.message}")
            print(f"    수정 힌트: {v.hint}")

    print(f"\nSCREEN_CONTRACT_FAIL {args.mode} — 위반 {len(report.violations)}건")
    return 1


if __name__ == "__main__":
    sys.exit(main())
