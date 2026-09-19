#!/usr/bin/env python3
"""validate_harness.py

Traveler 저장소의 "Harness"(에이전트가 지켜야 할 규칙·명령·계약 체계) 자체가
온전히 갖춰져 있는지 검사한다. Task나 Wave 실행 결과가 아니라, 그것을 가능하게
하는 CLAUDE.md/Skill/Command/디자인·Screen 계약이 존재하고 서로 모순되지
않는지를 확인하는 스크립트다.

이 스크립트는 파일을 만들거나 고치지 않는다 — 읽기 전용 검사만 수행한다.

사용법:
    python scripts/validate_harness.py

종료 코드:
    0  VALIDATE_HARNESS_PASS(13개 검사 전부 통과)
    1  하나 이상 검사 실패
"""

from __future__ import annotations

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
CLAUDE_MD = ROOT / "CLAUDE.md"
SKILL_MD = ROOT / ".claude" / "skills" / "traveler-project-pipeline" / "SKILL.md"
COMMANDS_DIR = ROOT / ".claude" / "commands"
CONTRACT_PATH = ROOT / "design-reference" / "SCREEN_ROUTE_CONTRACT.json"
DESIGN_PATH = ROOT / "design-reference" / "D-001" / "DESIGN.md"

EXPECTED_COMMANDS = [
    "gen-tasklist.md",
    "gen-task-details.md",
    "audit-tasks.md",
    "prepare-task.md",
    "implement-task.md",
    "run-wave.md",
    "release-check.md",
]

EXPECTED_SCHEMA = "traveler-screen-route-v1"
EXPECTED_DESIGN_PATH_STR = "design-reference/D-001/DESIGN.md"
EXPECTED_CONTRACT_PATH_STR = "design-reference/SCREEN_ROUTE_CONTRACT.json"
EXPECTED_DB_TABLES = [
    "user_profile",
    "mate_post",
    "mate_application",
    "user_block",
    "report",
    "outbound_url_setting",
]


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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    checks: list[Check] = []

    def add(num: int, name: str) -> Check:
        c = Check(num, name)
        checks.append(c)
        return c

    claude_text = read(CLAUDE_MD)
    skill_text = read(SKILL_MD)
    command_files = {p.name: p for p in COMMANDS_DIR.glob("*.md")} if COMMANDS_DIR.exists() else {}
    contract_data: dict | None = None
    if CONTRACT_PATH.exists():
        try:
            contract_data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            contract_data = None

    # ------------------------------------------------------------------ #1
    c1 = add(1, "CLAUDE.md 존재")
    if not CLAUDE_MD.exists():
        c1.fail(f"{CLAUDE_MD.relative_to(ROOT)} 파일이 없습니다.")
    elif not claude_text.strip():
        c1.fail(f"{CLAUDE_MD.relative_to(ROOT)} 파일이 비어 있습니다.")
    else:
        c1.note(f"{CLAUDE_MD.relative_to(ROOT)} 확인({len(claude_text)}자)")

    # ------------------------------------------------------------------ #2
    c2 = add(2, "Claude Code Skill 파일 존재")
    if not SKILL_MD.exists():
        c2.fail(f"{SKILL_MD.relative_to(ROOT)} 파일이 없습니다.")
    elif not skill_text.strip():
        c2.fail(f"{SKILL_MD.relative_to(ROOT)} 파일이 비어 있습니다.")
    elif not re.search(r"^name:\s*\S+", skill_text, re.MULTILINE):
        c2.fail(f"{SKILL_MD.relative_to(ROOT)}에 frontmatter 'name:' 필드가 없습니다.")
    else:
        c2.note(f"{SKILL_MD.relative_to(ROOT)} 확인(frontmatter 포함)")

    # ------------------------------------------------------------------ #3
    c3 = add(3, "7개 Command 존재")
    missing_cmds = [name for name in EXPECTED_COMMANDS if name not in command_files]
    extra_cmds = [name for name in command_files if name not in EXPECTED_COMMANDS]
    if missing_cmds:
        c3.fail(f"누락된 Command 파일: {missing_cmds}")
    if len(command_files) < len(EXPECTED_COMMANDS):
        c3.fail(f".claude/commands/에 {len(command_files)}개만 있음(필요: {len(EXPECTED_COMMANDS)}개)")
    empty_cmds = [name for name, p in command_files.items() if name in EXPECTED_COMMANDS and not p.read_text(encoding="utf-8").strip()]
    if empty_cmds:
        c3.fail(f"내용이 비어 있는 Command 파일: {empty_cmds}")
    if not c3.details:
        c3.note(f"필수 Command {len(EXPECTED_COMMANDS)}개 모두 존재: {EXPECTED_COMMANDS}")
    if extra_cmds:
        c3.note(f"참고: 필수 목록 외 추가 Command 존재(문제 아님): {extra_cmds}")

    # ------------------------------------------------------------------ #4
    c4 = add(4, f"{EXPECTED_SCHEMA} Marker 존재")
    marker_in_claude = f"HARNESS_SCHEMA={EXPECTED_SCHEMA}" in claude_text
    schema_in_contract = contract_data is not None and contract_data.get("schema_version") == EXPECTED_SCHEMA
    if not marker_in_claude:
        c4.fail(f"CLAUDE.md에 'HARNESS_SCHEMA={EXPECTED_SCHEMA}' 마커가 없습니다.")
    if contract_data is None:
        c4.fail(f"{CONTRACT_PATH.relative_to(ROOT)}를 읽을 수 없어 schema_version을 확인하지 못했습니다.")
    elif not schema_in_contract:
        c4.fail(f"{CONTRACT_PATH.relative_to(ROOT)}의 schema_version이 '{EXPECTED_SCHEMA}'가 아닙니다: {contract_data.get('schema_version')!r}")
    if marker_in_claude and schema_in_contract:
        c4.note("CLAUDE.md 마커와 SCREEN_ROUTE_CONTRACT.json의 schema_version이 일치")

    # ------------------------------------------------------------------ #5
    c5 = add(5, "D-001 DESIGN 경로 일치")
    design_path_match = re.search(r"^DESIGN_PATH=(\S+)", claude_text, re.MULTILINE)
    if not design_path_match:
        c5.fail("CLAUDE.md에 'DESIGN_PATH=' 마커가 없습니다.")
    elif design_path_match.group(1) != EXPECTED_DESIGN_PATH_STR:
        c5.fail(f"CLAUDE.md의 DESIGN_PATH가 '{EXPECTED_DESIGN_PATH_STR}'가 아닙니다: {design_path_match.group(1)!r}")
    if not DESIGN_PATH.exists():
        c5.fail(f"{EXPECTED_DESIGN_PATH_STR} 파일이 실제로 존재하지 않습니다.")
    if not c5.details:
        c5.note(f"CLAUDE.md의 DESIGN_PATH와 실제 파일 경로가 '{EXPECTED_DESIGN_PATH_STR}'로 일치")

    # ------------------------------------------------------------------ #6
    c6 = add(6, "Screen Contract 경로 일치")
    contract_marker_match = re.search(r"^SCREEN_CONTRACT=(\S+)", claude_text, re.MULTILINE)
    if not contract_marker_match:
        c6.fail("CLAUDE.md에 'SCREEN_CONTRACT=' 마커가 없습니다.")
    elif contract_marker_match.group(1) != EXPECTED_CONTRACT_PATH_STR:
        c6.fail(f"CLAUDE.md의 SCREEN_CONTRACT가 '{EXPECTED_CONTRACT_PATH_STR}'가 아닙니다: {contract_marker_match.group(1)!r}")
    if not CONTRACT_PATH.exists():
        c6.fail(f"{EXPECTED_CONTRACT_PATH_STR} 파일이 실제로 존재하지 않습니다.")
    if not c6.details:
        c6.note(f"CLAUDE.md의 SCREEN_CONTRACT와 실제 파일 경로가 '{EXPECTED_CONTRACT_PATH_STR}'로 일치")

    # ------------------------------------------------------------------ #7
    c7 = add(7, "Page Owner 5개 규칙 존재")
    rule_in_claude = bool(re.search(r"Page Owner", claude_text))
    rule_in_skill = bool(re.search(r"정확히\s*5개.*Page Owner|Page Owner.*정확히\s*5개", skill_text))
    if not rule_in_claude:
        c7.fail("CLAUDE.md에 Page Owner 관련 규칙 문구가 없습니다.")
    if not rule_in_skill:
        c7.fail(f"{SKILL_MD.relative_to(ROOT)}에 'Page Owner 정확히 5개' 규칙 문구가 없습니다.")
    contract_screen_count = len(contract_data.get("screens", [])) if contract_data else None
    if contract_screen_count is not None and contract_screen_count != 5:
        c7.fail(f"SCREEN_ROUTE_CONTRACT.json의 screens 개수가 5가 아닙니다: {contract_screen_count}")
    if not c7.details:
        c7.note("CLAUDE.md/SKILL.md에 Page Owner 5개 규칙이 명시되어 있고 Screen Contract도 5개")

    # ------------------------------------------------------------------ #8
    c8 = add(8, "DB Table 6개 기본 범위 존재")
    missing_tables_in_skill = [t for t in EXPECTED_DB_TABLES if f"`{t}`" not in skill_text]
    if missing_tables_in_skill:
        c8.fail(f"{SKILL_MD.relative_to(ROOT)}에 다음 기본 테이블명이 명시되어 있지 않습니다: {missing_tables_in_skill}")
    if not re.search(r"6개\s*(테이블|Table)|정확히\s*6개", skill_text):
        c8.fail(f"{SKILL_MD.relative_to(ROOT)}에 '6개 테이블' 상한 문구가 없습니다.")
    if not c8.details:
        c8.note(f"기본 6개 테이블({EXPECTED_DB_TABLES})이 모두 {SKILL_MD.relative_to(ROOT)}에 명시됨")

    # ------------------------------------------------------------------ #9
    c9 = add(9, "외부 입력 비저장 규칙 존재")
    claude_has_rule = bool(re.search(r"항공.{0,10}숙소.{0,40}(서버|DB|URL|로그)", claude_text))
    skill_has_rule = bool(re.search(r"항공.{0,10}숙소.{0,60}(서버|전송|저장)", skill_text))
    if not claude_has_rule:
        c9.fail("CLAUDE.md에 항공·숙소 입력값 미전송 규칙 문구가 없습니다.")
    if not skill_has_rule:
        c9.fail(f"{SKILL_MD.relative_to(ROOT)}에 항공·숙소 입력값 미전송 규칙 문구가 없습니다.")
    if not c9.details:
        c9.note("CLAUDE.md와 SKILL.md 모두 항공·숙소 입력값 미전송 규칙을 명시")

    # ------------------------------------------------------------------ #10
    c10 = add(10, "Playwright Chromium Smoke 규칙 존재")
    has_enabled = "PLAYWRIGHT_ENABLED=true" in claude_text
    has_scope = "PLAYWRIGHT_SCOPE=chromium-smoke" in claude_text
    has_chromium_rule = bool(re.search(r"Chromium", skill_text)) and bool(re.search(r"Smoke", skill_text))
    if not has_enabled:
        c10.fail("CLAUDE.md에 'PLAYWRIGHT_ENABLED=true' 마커가 없습니다.")
    if not has_scope:
        c10.fail("CLAUDE.md에 'PLAYWRIGHT_SCOPE=chromium-smoke' 마커가 없습니다.")
    if not has_chromium_rule:
        c10.fail(f"{SKILL_MD.relative_to(ROOT)}에 Chromium Smoke 규칙 문구가 없습니다.")
    if not c10.details:
        c10.note("Playwright Chromium Smoke 마커와 규칙 문구가 모두 존재")

    # ------------------------------------------------------------------ #11
    c11 = add(11, "AUTO_MERGE=false")
    if "AUTO_MERGE=false" not in claude_text:
        c11.fail("CLAUDE.md에 'AUTO_MERGE=false' 마커가 없습니다.")
    else:
        c11.note("CLAUDE.md에 'AUTO_MERGE=false' 확인")

    # ------------------------------------------------------------------ #12
    c12 = add(12, "AWS_ENABLED=false")
    if "AWS_ENABLED=false" not in claude_text:
        c12.fail("CLAUDE.md에 'AWS_ENABLED=false' 마커가 없습니다.")
    else:
        c12.note("CLAUDE.md에 'AWS_ENABLED=false' 확인")

    # ------------------------------------------------------------------ #13
    c13 = add(13, "EXCLUDED 보호 규칙 존재")
    claude_has_excluded_rule = bool(re.search(r"EXCLUDED.{0,30}(임의|구현하지)", claude_text))
    skill_has_excluded_rule = bool(re.search(r"EXCLUDED", skill_text))
    audit_path = ROOT / "scripts" / "audit_tasks.py"
    audit_text = read(audit_path)
    audit_enforces = "EXCLUDED" in audit_text and "excluded" in audit_text.lower()
    if not claude_has_excluded_rule:
        c13.fail("CLAUDE.md에 'EXCLUDED 기능을 임의로 구현하지 않는다'류 규칙 문구가 없습니다.")
    if not skill_has_excluded_rule:
        c13.fail(f"{SKILL_MD.relative_to(ROOT)}에 EXCLUDED 관련 규칙 문구가 없습니다.")
    if not audit_path.exists():
        c13.fail("scripts/audit_tasks.py가 없어 EXCLUDED 보호가 기계적으로 강제되는지 확인할 수 없습니다.")
    elif not audit_enforces:
        c13.fail("scripts/audit_tasks.py에서 EXCLUDED 관련 검사를 찾지 못했습니다.")
    if not c13.details:
        c13.note("CLAUDE.md·SKILL.md에 EXCLUDED 보호 규칙이 있고 scripts/audit_tasks.py가 이를 검증함")

    # ---------------------------------------------------------------------
    overall_pass = all(c.passed for c in checks)
    passed_count = sum(c.passed for c in checks)

    print("=== validate_harness.py ===")
    for c in checks:
        status = "PASS" if c.passed else "FAIL"
        print(f"[{status}] #{c.num} {c.name}")
        for d in c.details:
            print(f"        - {d}")

    if overall_pass:
        print(f"\nVALIDATE_HARNESS_PASS {passed_count}/{len(checks)}")
        return 0

    print(f"\nVALIDATE_HARNESS_FAIL {passed_count}/{len(checks)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
