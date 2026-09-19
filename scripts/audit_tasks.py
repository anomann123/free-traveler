#!/usr/bin/env python3
"""audit_tasks.py

Traveler Task 생성 파이프라인의 최종 감사 스크립트.

입력:
    TASKS/00_TASK_LIST.md
    TASKS/TASK-*.md
    docs/PROJECT_SCOPE.md
    design-reference/SCREEN_ROUTE_CONTRACT.json

수행하는 18개 검사(번호는 이 스크립트와 TASKS/TASK_AUDIT_REPORT.md에서 동일하게 쓰인다):
    1  Task List 구현 ID와 상세 Task 파일 1:1
    2  중복 Task ID 0
    3  Depends On 누락 0(참조된 ID가 실제로 존재)
    4  Dependency Cycle 0
    5  Screen 5개 모두 Page Owner 정확히 1개
    6  Route·Page Entry·Expected Files 일치(Page Owner ↔ SCREEN_ROUTE_CONTRACT.json)
    7  Component-only Screen 0(Page Owner 없는 Screen을 참조하는 Component 없음)
    8  SCR-001 Starter 제거 AC 존재
    9  SCR-003 세 탭 조립 AC 존재
    10 SCR-005 역할별 상태 조립 AC 존재
    11 DB Schema·RLS·Access·Seed Task 존재
    12 DB Table 범위가 6개 기본 테이블을 크게 넘지 않음
    13 외부 입력 비저장 AC 존재(항공·숙소)
    14 Auth·성인·기본 RLS AC 존재
    15 Playwright Chromium Smoke Task 존재
    16 AWS·EC2·자동 Merge 구현 Task 0
    17 REQ-FUNC 80개와 REQ-NF 34개가 Task 또는 EXCLUDED 표에 존재
    18 EXCLUDED 상세 구현 파일이 생성되지 않음

출력:
    TASKS/TASK_MANIFEST.csv   — Task 1건당 1행의 메타데이터 표
    TASKS/TASK_AUDIT_REPORT.md — 18개 검사 결과 보고서

이 스크립트는 마크다운 텍스트에 대한 **정적·휴리스틱** 검사다. 일부 검사(특히
13·16)는 키워드/문맥 기반 근사 검사이며, 통과가 내용의 완전한 의미적 정확성을
보장하지는 않는다. 실패는 실제 문제를 의미하지만 최종 판단은 사람이 한다.

사용법:
    python scripts/audit_tasks.py

종료 코드:
    0  AUDIT_PASS (18개 검사 전부 통과)
    1  하나 이상 검사 실패, 또는 필수 입력 파일 누락
"""

from __future__ import annotations

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
TASKS_DIR = ROOT / "TASKS"
TASKLIST_PATH = TASKS_DIR / "00_TASK_LIST.md"
DETAIL_FILE_PREFIX = "TASK-"
PROJECT_SCOPE_PATH = ROOT / "docs" / "PROJECT_SCOPE.md"
CONTRACT_PATH = ROOT / "design-reference" / "SCREEN_ROUTE_CONTRACT.json"
MANIFEST_PATH = TASKS_DIR / "TASK_MANIFEST.csv"
REPORT_PATH = TASKS_DIR / "TASK_AUDIT_REPORT.md"

TASK_ID_PREFIXES = ("PAGE", "PO", "CMP", "DATA", "DB", "AUTH", "INFRA", "UNIT", "TEST", "E2E", "CI", "DEPLOY")
TASK_ID_RE = re.compile(r"^(" + "|".join(TASK_ID_PREFIXES) + r")-[A-Za-z0-9_-]+$")
REQ_ID_RE = re.compile(r"REQ-(?:FUNC|NF)-\d{3}")

ALLOWED_DB_TABLES = {
    "user_profile",
    "mate_post",
    "mate_application",
    "user_block",
    "report",
    "outbound_url_setting",
}
DB_TABLE_OVERAGE_TOLERANCE = 2  # "크게 넘지 않음": 6개 기준선에서 이 개수까지는 허용

FORBIDDEN_INFRA_KEYWORDS = [
    "EC2", "AWS", "Auto-Merge", "auto-merge", "자동 병합 러너", "Merge Runner", "머지 러너",
]
FORBIDDEN_TEST_SCOPE = [
    "Firefox", "WebKit", "webkit", "시각적 회귀", "visual regression",
    "성능 테스트", "load test", "부하 테스트",
]
NEGATION_NEARBY_RE = re.compile(r"(없|금지|않|방지|말다|없다|없음)")


def _negated_nearby(text: str, start: int, end: int, before: int = 20, after: int = 60) -> bool:
    window = text[max(0, start - before): end + after]
    return bool(NEGATION_NEARBY_RE.search(window))


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def split_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-+:?", c) for c in cells)


def parse_task_rows(tasklist_text: str) -> list[dict]:
    """TASKS/00_TASK_LIST.md의 세로형(필드|내용) 표와 가로형(Task ID 헤더 포함) 표를
    모두 인식해 Task 레코드 목록을 만든다. 각 레코드는 소문자 키를 쓴다."""
    rows: list[dict] = []
    lines = tasklist_text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip().startswith("|"):
            i += 1
            continue
        header_cells = split_row(line)
        if i + 1 >= n or not lines[i + 1].strip().startswith("|"):
            i += 1
            continue
        sep_cells = split_row(lines[i + 1])
        if not _is_separator_row(sep_cells):
            i += 1
            continue

        header_lower = [c.lower() for c in header_cells]
        j = i + 2
        table_data_rows: list[list[str]] = []
        while j < n and lines[j].strip().startswith("|"):
            cells = split_row(lines[j])
            if cells and not _is_separator_row(cells):
                table_data_rows.append(cells)
            j += 1

        if header_lower == ["필드", "내용"] and len(header_cells) == 2:
            record: dict = {}
            for cells in table_data_rows:
                if len(cells) < 2:
                    continue
                record[cells[0].strip().lower()] = cells[1].strip()
            task_id = record.get("task id", "")
            if TASK_ID_RE.match(task_id):
                record["task_id"] = task_id
                record["_raw"] = [task_id] + list(record.values())
                rows.append(record)
        elif "task id" in header_lower:
            id_idx = header_lower.index("task id")
            for cells in table_data_rows:
                if id_idx >= len(cells):
                    continue
                task_id = cells[id_idx].strip()
                if not TASK_ID_RE.match(task_id):
                    continue
                record = dict(zip(header_lower, cells))
                record["task_id"] = task_id
                record["_raw"] = cells
                rows.append(record)

        i = j
    return rows


def parse_excluded_register(tasklist_text: str) -> set[str]:
    for marker in ("## 8. NON_IMPLEMENTATION", "NON_IMPLEMENTATION"):
        if marker in tasklist_text:
            section = tasklist_text.split(marker, 1)[1]
            if "## 9." in section:
                section = section.split("## 9.", 1)[0]
            return set(REQ_ID_RE.findall(section))
    return set()


def load_project_scope_status() -> dict[str, str]:
    status: dict[str, str] = {}
    if not PROJECT_SCOPE_PATH.exists():
        return status
    text = PROJECT_SCOPE_PATH.read_text(encoding="utf-8")
    for m in re.finditer(r"^\|\s*(REQ-(?:FUNC|NF)-\d{3})\s*\|\s*([^|]+?)\s*\|", text, re.MULTILINE):
        status.setdefault(m.group(1), m.group(2).strip())
    return status


def load_screens() -> list[dict]:
    if not CONTRACT_PATH.exists():
        return []
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8")).get("screens", [])


def depends_list(cell: str) -> list[str]:
    if not cell or cell.strip() in ("없음", "N/A", "-"):
        return []
    return [d.strip() for d in cell.split(",") if d.strip()]


def req_list(cell: str) -> list[str]:
    return REQ_ID_RE.findall(cell or "")


def detail_files() -> dict[str, Path]:
    return {
        p.stem[len(DETAIL_FILE_PREFIX):]: p
        for p in TASKS_DIR.glob(f"{DETAIL_FILE_PREFIX}*.md")
        if p.stem.startswith(DETAIL_FILE_PREFIX)
    }


# ---------------------------------------------------------------------------
# Check framework
# ---------------------------------------------------------------------------

@dataclass
class Check:
    num: int
    name: str
    passed: bool = True
    details: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.passed = False
        self.details.append(msg)

    def note(self, msg: str) -> None:
        self.details.append(msg)


def main() -> int:
    checks: list[Check] = []

    def add(num: int, name: str) -> Check:
        c = Check(num, name)
        checks.append(c)
        return c

    # --- Preconditions -----------------------------------------------------
    if not TASKLIST_PATH.exists():
        print(f"[FATAL] {TASKLIST_PATH} 가 없습니다. Task List를 먼저 생성하십시오.")
        return 1

    tasklist_text = TASKLIST_PATH.read_text(encoding="utf-8")
    rows = parse_task_rows(tasklist_text)
    task_ids = [r["task_id"] for r in rows]
    by_id = {r["task_id"]: r for r in rows}
    all_id_set = set(task_ids)
    details_map_paths = detail_files()

    if not details_map_paths:
        print(f"[FATAL] {TASKS_DIR}/{DETAIL_FILE_PREFIX}*.md 상세 파일이 없습니다. Task 상세를 먼저 생성하십시오.")
        return 1

    details = {k: v.read_text(encoding="utf-8") for k, v in details_map_paths.items()}
    screens = load_screens()
    scope_status = load_project_scope_status()
    excluded_register = parse_excluded_register(tasklist_text)

    # ---------------------------------------------------------------- #1, #2
    c1 = add(1, "Task List 구현 ID와 상세 Task 파일 1:1")
    missing = sorted(all_id_set - set(details_map_paths))
    orphan = sorted(set(details_map_paths) - all_id_set)
    if missing:
        c1.fail(f"상세 파일 없는 Task ID: {missing}")
    if orphan:
        c1.fail(f"Task List에 없는 고아 상세 파일: {orphan}")
    if not missing and not orphan:
        c1.note(f"Task {len(all_id_set)}개 = 상세 파일 {len(details_map_paths)}개, 완전 일치")

    c2 = add(2, "중복 Task ID 0")
    dup = sorted({t for t in task_ids if task_ids.count(t) > 1})
    if dup:
        c2.fail(f"중복 Task ID: {dup}")
    else:
        c2.note("중복 없음")

    # -------------------------------------------------------------------- #3
    c3 = add(3, "Depends On 누락 0")
    dep_map: dict[str, list[str]] = {}
    for tid, row in by_id.items():
        deps = depends_list(row.get("depends on", ""))
        dep_map[tid] = deps
        dangling = [d for d in deps if d not in all_id_set]
        if dangling:
            c3.fail(f"{tid}의 Depends On이 존재하지 않는 Task를 참조: {dangling}")
    if c3.passed:
        c3.note("모든 Depends On 참조가 실제 Task ID를 가리킴")

    # -------------------------------------------------------------------- #4
    c4 = add(4, "Dependency Cycle 0")
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in all_id_set}
    cycle_found: list[str] = []

    def dfs(node: str, path: list[str]) -> bool:
        color[node] = GRAY
        path.append(node)
        for dep in dep_map.get(node, []):
            if dep not in all_id_set:
                continue
            if color.get(dep, WHITE) == GRAY:
                cyc = path[path.index(dep):] + [dep]
                cycle_found.append(" -> ".join(cyc))
                return True
            if color.get(dep, WHITE) == WHITE:
                if dfs(dep, path):
                    return True
        path.pop()
        color[node] = BLACK
        return False

    for tid in all_id_set:
        if color[tid] == WHITE:
            if dfs(tid, []):
                break
    if cycle_found:
        c4.fail(f"의존성 순환 발견: {cycle_found[0]}")
    else:
        c4.note("순환 의존성 없음")

    # -------------------------------------------------------------------- #5
    c5 = add(5, "Screen 5개 모두 Page Owner 정확히 1개")
    expected_screen_ids = {s["screen_id"] for s in screens} or {"SCR-001", "SCR-002", "SCR-003", "SCR-004", "SCR-005"}
    po_rows = [r for r in rows if r["task_id"].startswith(("PAGE-", "PO-"))]
    po_by_screen: dict[str, dict] = {}
    for row in po_rows:
        screen_val = (row.get("screen") or "").strip()
        matched = next((sid for sid in expected_screen_ids if sid in screen_val), None)
        if matched is None:
            c5.fail(f"Page Owner '{row['task_id']}'의 Screen 값('{screen_val}')이 알려진 Screen과 매칭되지 않음")
            continue
        if matched in po_by_screen:
            c5.fail(f"Screen '{matched}'에 Page Owner Task가 2개 이상 존재: {po_by_screen[matched]['task_id']}, {row['task_id']}")
        else:
            po_by_screen[matched] = row
    missing_screens = expected_screen_ids - set(po_by_screen)
    if missing_screens:
        c5.fail(f"Page Owner가 없는 Screen: {sorted(missing_screens)}")
    if c5.passed:
        c5.note(f"{len(po_by_screen)}개 Screen 모두 Page Owner 정확히 1개: " + ", ".join(f"{k}={v['task_id']}" for k, v in sorted(po_by_screen.items())))

    # -------------------------------------------------------------------- #6
    c6 = add(6, "Route·Page Entry·Expected Files 일치")
    screen_contract = {s["screen_id"]: s for s in screens}
    for screen_id, po_row in po_by_screen.items():
        contract = screen_contract.get(screen_id)
        if not contract:
            c6.note(f"{screen_id}: SCREEN_ROUTE_CONTRACT.json에 계약 없음(스킵)")
            continue
        row_route = (po_row.get("route") or "").strip("` ")
        row_entry = (po_row.get("page entry") or "").strip("` ")
        expected_route = contract.get("route", "")
        expected_entry = contract.get("page_entry", "")
        if row_route != expected_route:
            c6.fail(f"{po_row['task_id']} Route 불일치: Task='{row_route}' vs 계약='{expected_route}'")
        if row_entry != expected_entry:
            c6.fail(f"{po_row['task_id']} Page Entry 불일치: Task='{row_entry}' vs 계약='{expected_entry}'")
        expected_files_cell = po_row.get("expected files", "")
        if expected_entry and expected_entry not in expected_files_cell:
            c6.fail(f"{po_row['task_id']} Expected Files에 Page Entry '{expected_entry}'가 언급되지 않음: '{expected_files_cell}'")
    if c6.passed:
        c6.note("5개 Page Owner의 Route/Page Entry/Expected Files가 SCREEN_ROUTE_CONTRACT.json과 일치")

    # -------------------------------------------------------------------- #7
    c7 = add(7, "Component-only Screen 0(Page Owner 없는 Screen을 참조하는 Component 없음)")
    cmp_rows = [r for r in rows if r["task_id"].startswith("CMP-")]
    orphan_screens: set[str] = set()
    for row in cmp_rows:
        screen_val = (row.get("screen") or "").strip()
        if not screen_val or screen_val in ("전역", "N/A"):
            continue
        matched = next((sid for sid in expected_screen_ids if sid in screen_val), None)
        if matched is None:
            orphan_screens.add(screen_val)
        elif matched not in po_by_screen:
            orphan_screens.add(matched)
    if orphan_screens:
        c7.fail(f"Page Owner가 없는데 Component가 참조하는 Screen: {sorted(orphan_screens)}")
    else:
        c7.note("모든 Component의 Screen에 대응하는 Page Owner 존재")

    # -------------------------------------------------------------------- #8
    c8 = add(8, "SCR-001 Starter 제거 AC 존재")
    scr001 = po_by_screen.get("SCR-001")
    if not scr001:
        c8.fail("SCR-001 Page Owner를 찾을 수 없음")
    else:
        text = details.get(scr001["task_id"], "")
        if not any(k in text.lower() for k in ["starter", "스타터", "템플릿 제거", "create-next-app"]):
            c8.fail(f"{scr001['task_id']} 상세에 Starter 제거 AC 없음")
        else:
            c8.note(f"{scr001['task_id']}에서 Starter 제거 AC 확인")

    # -------------------------------------------------------------------- #9
    c9 = add(9, "SCR-003 세 탭 조립 AC 존재")
    scr003 = po_by_screen.get("SCR-003")
    if not scr003:
        c9.fail("SCR-003 Page Owner를 찾을 수 없음")
    else:
        text = details.get(scr003["task_id"], "")
        missing_kw = [k for k in ("항공", "숙소", "동행") if k not in text]
        if missing_kw:
            c9.fail(f"{scr003['task_id']} 상세에 탭 키워드 누락: {missing_kw}")
        else:
            c9.note(f"{scr003['task_id']}에서 항공/숙소/동행 3탭 조립 AC 확인")

    # ------------------------------------------------------------------- #10
    c10 = add(10, "SCR-005 역할별 상태 조립 AC 존재")
    scr005 = po_by_screen.get("SCR-005")
    if not scr005:
        c10.fail("SCR-005 Page Owner를 찾을 수 없음")
    else:
        text = details.get(scr005["task_id"], "").lower()
        roles = {"guest": ["guest", "게스트", "비로그인"], "member": ["member", "회원"], "admin": ["admin", "관리자"]}
        missing_roles = [r for r, kws in roles.items() if not any(k.lower() in text for k in kws)]
        if missing_roles:
            c10.fail(f"{scr005['task_id']} 상세에 역할 키워드 누락: {missing_roles}")
        else:
            c10.note(f"{scr005['task_id']}에서 Guest/Member/Admin 역할별 조립 AC 확인")

    # ------------------------------------------------------------------- #11
    c11 = add(11, "DB Schema·RLS·Access·Seed Task 존재")
    db_task_ids = [t for t in task_ids if t.startswith("DB-")]
    needed = {"SCHEMA": "SCHEMA", "RLS": "RLS", "ACCESS": "ACCESS", "SEED": "SEED"}
    found = {k: [t for t in db_task_ids if kw in t] for k, kw in needed.items()}
    missing_kinds = [k for k, v in found.items() if not v]
    if missing_kinds:
        c11.fail(f"DB Task 중 다음 종류가 없음: {missing_kinds} (존재하는 DB Task: {db_task_ids})")
    else:
        c11.note("Schema/RLS/Access/Seed Task 모두 존재: " + ", ".join(f"{k}={v}" for k, v in found.items()))

    # ------------------------------------------------------------------- #12
    c12 = add(12, "DB Table 범위가 6개 기본 테이블을 크게 넘지 않음")
    mentioned_tables: set[str] = set()
    for tid in db_task_ids:
        text = details.get(tid, "")
        for tbl in re.findall(r"`([a-z][a-z0-9_]*)`", text):
            if "_" in tbl and not tbl.endswith((".ts", ".tsx", ".sql", ".md", ".json")):
                mentioned_tables.add(tbl)
    extra = sorted(mentioned_tables - ALLOWED_DB_TABLES)
    if len(extra) > DB_TABLE_OVERAGE_TOLERANCE:
        c12.fail(f"기본 6개 테이블({sorted(ALLOWED_DB_TABLES)}) 외 {len(extra)}개 추가 식별자 발견(허용 오차 {DB_TABLE_OVERAGE_TOLERANCE} 초과): {extra}")
    else:
        c12.note(f"기본 테이블 {sorted(mentioned_tables & ALLOWED_DB_TABLES)}, 추가 식별자 {extra}(허용 범위 내)")

    # ------------------------------------------------------------------- #13
    c13 = add(13, "외부 입력 비저장 AC 존재(항공·숙소)")
    target_ids = [t for t in task_ids if t in ("CMP-SCR003-FLIGHT-FORM", "CMP-SCR003-HOTEL-FORM", "PAGE-SCR003") or "FLIGHT-FORM" in t or "HOTEL-FORM" in t]
    positive_pattern = re.compile(r"(항공|숙소|호텔)[^\n]{0,60}(서버|DB|데이터베이스|URL\s*쿼리|로그)[^\n]{0,20}(저장하지\s*않|전송하지\s*않|미저장|보내지\s*않)")
    found_positive = False
    for tid in target_ids:
        text = details.get(tid, "")
        if positive_pattern.search(text) or ("서버" in text and "저장하지 않" in text and ("항공" in text or "숙소" in text)):
            found_positive = True
            c13.note(f"{tid}에서 비저장 AC 확인")
    if not found_positive:
        c13.fail(f"항공/숙소 관련 Task({target_ids})에서 '서버/DB/로그에 저장하지 않는다'류 AC를 찾지 못함")

    danger_pattern = re.compile(r"(항공|숙소|호텔)[^\n]{0,40}(서버|DB|데이터베이스)[^\n]{0,10}(저장|전송)")
    for tid, text in details.items():
        for m in danger_pattern.finditer(text):
            if not _negated_nearby(text, m.start(), m.end(), before=20, after=20):
                c13.fail(f"{tid} 상세에 항공·숙소 입력값을 서버에 저장하는 것으로 읽히는 문장이 금지 조항 없이 존재")

    # ------------------------------------------------------------------- #14
    c14 = add(14, "Auth·성인·기본 RLS AC 존재")
    auth_task = next((t for t in task_ids if "AUTH" in t and "SUPABASE" in t), None) or next((t for t in task_ids if t.startswith("AUTH-")), None)
    adult_task = next((t for t in task_ids if "ADULT" in t), None)
    rls_task = next((t for t in task_ids if "RLS" in t), None)
    for label, tid in (("Auth 연동", auth_task), ("성인 확인", adult_task), ("기본 RLS", rls_task)):
        if not tid:
            c14.fail(f"{label} Task를 찾지 못함")
            continue
        text = details.get(tid, "")
        if not text.strip():
            c14.fail(f"{tid}({label}) 상세 파일 내용이 비어 있음")
        else:
            c14.note(f"{label} Task 확인: {tid}")

    # ------------------------------------------------------------------- #15
    c15 = add(15, "Playwright Chromium Smoke Task 존재")
    e2e_ids = [t for t in task_ids if t.startswith("E2E-")]
    if not e2e_ids:
        c15.fail("E2E- 접두어 Task가 하나도 없음")
    else:
        no_chromium = [t for t in e2e_ids if "chromium" not in details.get(t, "").lower()]
        if no_chromium:
            c15.fail(f"Chromium 언급이 없는 E2E Task: {no_chromium}")
        else:
            c15.note(f"Playwright Chromium Smoke Task {len(e2e_ids)}개 확인: {e2e_ids}")

    # ------------------------------------------------------------------- #16
    c16 = add(16, "AWS·EC2·자동 Merge 구현 Task 0")
    bad_id_task = [t for t in task_ids if re.search(r"AWS|EC2|MERGE", t, re.IGNORECASE)]
    if bad_id_task:
        c16.fail(f"Task ID 자체에 금지 인프라 키워드 포함: {bad_id_task}")
    haystacks = {"00_TASK_LIST.md": tasklist_text, **details}
    for name, text in haystacks.items():
        lowered = text.lower()
        for kw in FORBIDDEN_INFRA_KEYWORDS:
            for m in re.finditer(re.escape(kw.lower()), lowered):
                if not _negated_nearby(lowered, m.start(), m.end()):
                    c16.fail(f"'{name}'에 금지 조항 없이 '{kw}' 등장")
    if c16.passed:
        c16.note("AWS/EC2/자동 Merge 관련 구현 Task 또는 미부정 언급 없음")

    # ------------------------------------------------------------------- #17
    c17 = add(17, "REQ-FUNC 80개와 REQ-NF 34개가 Task 또는 EXCLUDED 표에 존재")
    covered_in_tasks: set[str] = set()
    for row in rows:
        covered_in_tasks |= set(req_list(" | ".join(row.get("_raw", []))))
    accounted = covered_in_tasks | excluded_register
    func_accounted = {i for i in accounted if i.startswith("REQ-FUNC-") and 1 <= int(i.rsplit("-", 1)[1]) <= 80}
    nf_accounted = {i for i in accounted if i.startswith("REQ-NF-") and 1 <= int(i.rsplit("-", 1)[1]) <= 34}
    expected_func = {f"REQ-FUNC-{i:03d}" for i in range(1, 81)}
    expected_nf = {f"REQ-NF-{i:03d}" for i in range(1, 35)}
    missing_func = sorted(expected_func - func_accounted)
    missing_nf = sorted(expected_nf - nf_accounted)
    if missing_func:
        c17.fail(f"Task/EXCLUDED 어디에도 없는 REQ-FUNC: {missing_func}")
    if missing_nf:
        c17.fail(f"Task/EXCLUDED 어디에도 없는 REQ-NF: {missing_nf}")
    if scope_status:
        scope_excluded = {k for k, v in scope_status.items() if v == "EXCLUDED"}
        scope_implement = {k for k, v in scope_status.items() if v != "EXCLUDED"}
        excluded_but_in_tasks = sorted(scope_excluded & covered_in_tasks)
        if excluded_but_in_tasks:
            c17.fail(f"docs/PROJECT_SCOPE.md 기준 EXCLUDED인데 구현 Task에 연결된 Requirement: {excluded_but_in_tasks}")
        implement_missing = sorted(scope_implement - covered_in_tasks)
        if implement_missing:
            c17.fail(f"docs/PROJECT_SCOPE.md 기준 IMPLEMENT인데 어떤 Task에도 없는 Requirement: {implement_missing}")
    else:
        c17.note("docs/PROJECT_SCOPE.md를 읽지 못해 IMPLEMENT/EXCLUDED 교차검증은 생략(80/34 전수 존재만 확인)")
    if c17.passed:
        c17.note(f"REQ-FUNC 80/80, REQ-NF 34/34 모두 Task 또는 EXCLUDED 표에 존재")

    # ------------------------------------------------------------------- #18
    c18 = add(18, "EXCLUDED 상세 구현 파일이 생성되지 않음")
    scope_excluded_ids = {k for k, v in scope_status.items() if v == "EXCLUDED"} if scope_status else excluded_register
    excluded_only_tasks = []
    for row in rows:
        refs = set(req_list(row.get("requirement ref", "")))
        if refs and refs.issubset(scope_excluded_ids):
            excluded_only_tasks.append(row["task_id"])
    if excluded_only_tasks:
        c18.fail(f"Requirement Ref가 전부 EXCLUDED인 Task(상세 구현 파일이 생성되면 안 됨): {excluded_only_tasks}")
    else:
        c18.note("EXCLUDED Requirement만으로 구성된 구현 Task 없음(상세 파일 미생성 확인)")

    # ---------------------------------------------------------------------
    # Manifest CSV
    # ---------------------------------------------------------------------
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Seq", "Task ID", "Category", "Title", "Implementation Status",
            "Screen", "Route", "Page Entry", "Depends On", "Expected Files",
            "Requirement Ref", "Priority", "Detail File", "Detail Exists",
        ])
        for row in rows:
            tid = row["task_id"]
            category = next((p for p in TASK_ID_PREFIXES if tid.startswith(p + "-")), "OTHER")
            writer.writerow([
                row.get("seq", ""),
                tid,
                category,
                row.get("제목", row.get("title", "")),
                row.get("implementation status", ""),
                row.get("screen", ""),
                row.get("route", ""),
                row.get("page entry", ""),
                row.get("depends on", ""),
                row.get("expected files", ""),
                " ".join(req_list(row.get("requirement ref", ""))),
                row.get("priority", ""),
                f"{DETAIL_FILE_PREFIX}{tid}.md",
                "Y" if tid in details_map_paths else "N",
            ])

    # ---------------------------------------------------------------------
    # Report
    # ---------------------------------------------------------------------
    overall_pass = all(c.passed for c in checks)
    passed_count = sum(c.passed for c in checks)

    report_lines = [
        "# Task Audit Report",
        "",
        f"**결과:** {'AUDIT_PASS' if overall_pass else 'AUDIT_FAIL'}",
        f"**검사 통과:** {passed_count}/{len(checks)}",
        f"**Task 총 개수:** {len(task_ids)}",
        "",
        "| # | 검사 | 결과 |",
        "|---|---|---|",
    ]
    for c in checks:
        report_lines.append(f"| {c.num} | {c.name} | {'PASS' if c.passed else 'FAIL'} |")
    report_lines.append("")
    report_lines.append("## 세부 내용")
    report_lines.append("")
    for c in checks:
        report_lines.append(f"### #{c.num} {c.name} — {'PASS' if c.passed else 'FAIL'}")
        report_lines.append("")
        if c.details:
            for d in c.details:
                report_lines.append(f"- {d}")
        else:
            report_lines.append("- (세부 내용 없음)")
        report_lines.append("")

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print("=== audit_tasks.py ===")
    for c in checks:
        status = "PASS" if c.passed else "FAIL"
        print(f"[{status}] #{c.num} {c.name}")
        if not c.passed:
            for d in c.details:
                print(f"        - {d}")
    print(f"\nManifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Report:   {REPORT_PATH.relative_to(ROOT)}")

    if overall_pass:
        print(f"\nAUDIT_PASS {passed_count}/{len(checks)}")
        return 0

    print(f"\nAUDIT_FAIL {passed_count}/{len(checks)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
