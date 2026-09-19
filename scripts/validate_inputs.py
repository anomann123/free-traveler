#!/usr/bin/env python3
"""validate_inputs.py

Traveler Task 생성 파이프라인의 1단계 검증 스크립트.
(.claude/skills/traveler-project-pipeline/SKILL.md 참조)

/gen-tasklist 실행 전에 반드시 이 스크립트를 통과해야 한다. 입력 문서 자체를
수정하지 않으며, 오직 존재 여부와 내부 일관성만 읽어서 검사한다(stdlib만 사용).

사용법:
    python scripts/validate_inputs.py

종료 코드:
    0  모든 검사 통과
    1  하나 이상의 검사 실패
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "docs/06_SRS_UIUX_REVISED.md",
    "docs/PROJECT_SCOPE.md",
    "docs/UIUX_TRACEABILITY.md",
    "design-reference/D-001/DESIGN.md",
    "design-reference/UI_CONTRACT.md",
    "design-reference/SCREEN_ROUTE_CONTRACT.json",
    "package.json",
]

EXPECTED_SCHEMA_VERSION = "traveler-screen-route-v1"
EXPECTED_FRAMEWORK = "nextjs-app-router"
EXPECTED_SCREEN_COUNT = 5
EXPECTED_CORE_COUNT = 4
EXPECTED_SUPPLEMENTARY_COUNT = 1

REQ_ROW_RE = re.compile(
    r"^\|\s*(REQ-(?:FUNC|NF)-\d{3})\s*\|\s*([^|]+?)\s*\|", re.MULTILINE
)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.info.append(msg)

    def ok(self) -> bool:
        return not self.errors


def check_required_files(report: Report) -> None:
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            report.error(f"필수 입력 파일이 없습니다: {rel}")
        elif path.stat().st_size == 0:
            report.error(f"필수 입력 파일이 비어 있습니다: {rel}")
        else:
            report.note(f"입력 파일 확인: {rel}")


def load_json(rel: str, report: Report) -> dict | None:
    path = ROOT / rel
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(f"{rel} JSON 파싱 실패: {exc}")
        return None


def check_screen_route_contract(report: Report) -> dict | None:
    data = load_json("design-reference/SCREEN_ROUTE_CONTRACT.json", report)
    if data is None:
        return None

    schema_version = data.get("schema_version")
    if schema_version != EXPECTED_SCHEMA_VERSION:
        report.error(
            f"schema_version이 '{EXPECTED_SCHEMA_VERSION}'이어야 하는데 "
            f"'{schema_version}'입니다."
        )

    framework = data.get("framework")
    if framework != EXPECTED_FRAMEWORK:
        report.error(
            f"framework가 '{EXPECTED_FRAMEWORK}'이어야 하는데 '{framework}'입니다."
        )

    screens = data.get("screens", [])
    if len(screens) != EXPECTED_SCREEN_COUNT:
        report.error(
            f"screens 배열은 정확히 {EXPECTED_SCREEN_COUNT}개여야 하는데 "
            f"{len(screens)}개입니다."
        )

    routes = [s.get("route") for s in screens]
    if len(set(routes)) != len(routes):
        report.error(f"Route 중복이 발견되었습니다: {routes}")

    page_entries = [s.get("page_entry") for s in screens]
    if len(set(page_entries)) != len(page_entries):
        report.error(f"Page Entry 중복이 발견되었습니다: {page_entries}")

    core = [s for s in screens if s.get("classification") == "core"]
    supplementary = [s for s in screens if s.get("classification") == "supplementary"]
    if len(core) != EXPECTED_CORE_COUNT:
        report.error(
            f"핵심(core) Screen은 {EXPECTED_CORE_COUNT}개여야 하는데 {len(core)}개입니다."
        )
    if len(supplementary) != EXPECTED_SUPPLEMENTARY_COUNT:
        report.error(
            f"보조(supplementary) Screen은 {EXPECTED_SUPPLEMENTARY_COUNT}개여야 하는데 "
            f"{len(supplementary)}개입니다."
        )

    for s in screens:
        for key in ("screen_id", "route", "page_entry", "classification"):
            if not s.get(key):
                report.error(f"Screen 항목에 '{key}' 필드가 없습니다: {s}")

    report.note(
        f"SCREEN_ROUTE_CONTRACT.json 확인: screens={len(screens)}, "
        f"core={len(core)}, supplementary={len(supplementary)}"
    )
    return data


def check_traceability(report: Report) -> None:
    path = ROOT / "docs/UIUX_TRACEABILITY.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")

    func_ids: set[int] = set()
    nf_ids: set[int] = set()
    status_by_id: dict[str, str] = {}
    duplicates: list[str] = []

    for match in REQ_ROW_RE.finditer(text):
        req_id, status_cell = match.group(1), match.group(2).strip()
        if req_id in status_by_id:
            duplicates.append(req_id)
            continue
        status_by_id[req_id] = status_cell

        num = int(req_id.rsplit("-", 1)[1])
        if "FUNC" in req_id:
            func_ids.add(num)
        else:
            nf_ids.add(num)

    if duplicates:
        report.error(f"UIUX_TRACEABILITY.md에 중복된 Requirement 행이 있습니다: {duplicates}")

    expected_func = set(range(1, 81))
    expected_nf = set(range(1, 35))

    if func_ids != expected_func:
        missing = sorted(expected_func - func_ids)
        extra = sorted(func_ids - expected_func)
        if missing:
            report.error(f"REQ-FUNC 누락: {missing}")
        if extra:
            report.error(f"REQ-FUNC 범위 밖 번호: {extra}")

    if nf_ids != expected_nf:
        missing = sorted(expected_nf - nf_ids)
        extra = sorted(nf_ids - expected_nf)
        if missing:
            report.error(f"REQ-NF 누락: {missing}")
        if extra:
            report.error(f"REQ-NF 범위 밖 번호: {extra}")

    bad_status = [
        req_id
        for req_id, status in status_by_id.items()
        if status != "EXCLUDED" and not status.startswith("IMPLEMENT")
    ]
    if bad_status:
        report.error(
            "Implementation Status가 IMPLEMENT* 또는 EXCLUDED가 아닌 행: "
            f"{bad_status}"
        )

    excluded = sum(1 for s in status_by_id.values() if s == "EXCLUDED")
    implement = len(status_by_id) - excluded
    report.note(
        f"UIUX_TRACEABILITY.md 확인: 총 {len(status_by_id)}건 "
        f"(IMPLEMENT* {implement} / EXCLUDED {excluded})"
    )
    if len(status_by_id) != 114:
        report.error(
            f"Requirement 총 건수는 114여야 하는데 {len(status_by_id)}건입니다."
        )


def check_package_json(report: Report) -> None:
    data = load_json("package.json", report)
    if data is None:
        return
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    if "next" not in deps:
        report.error("package.json에 'next' 의존성이 없습니다 — Next.js App Router 전제가 깨집니다.")
    else:
        report.note(f"package.json 확인: next={deps.get('next')}")


def snapshot_src_app(report: Report, contract: dict | None) -> None:
    src_app = ROOT / "src" / "app"
    if not src_app.exists():
        report.error("src/app 디렉터리가 존재하지 않습니다.")
        return

    existing = sorted(
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in src_app.rglob("*")
        if p.is_file()
    )
    report.note(f"현재 src/app 파일 트리({len(existing)}개): {', '.join(existing)}")

    if contract is None:
        return

    for screen in contract.get("screens", []):
        page_entry = screen.get("page_entry", "")
        exists = (ROOT / page_entry).exists()
        state = "기존 파일 있음 → 수정" if exists else "미존재 → 신규 생성"
        report.note(f"{screen.get('screen_id')} Page Entry '{page_entry}': {state}")


def main() -> int:
    report = Report()

    check_required_files(report)
    contract = check_screen_route_contract(report)
    check_traceability(report)
    check_package_json(report)
    snapshot_src_app(report, contract)

    print("=== validate_inputs.py 결과 ===")
    for line in report.info:
        print(f"[INFO] {line}")
    for line in report.warnings:
        print(f"[WARN] {line}")
    for line in report.errors:
        print(f"[FAIL] {line}")

    if report.ok():
        print(f"\nPASS — 위반 0건, 정보 {len(report.info)}건, 경고 {len(report.warnings)}건")
        return 0

    print(f"\nFAIL — 위반 {len(report.errors)}건. /gen-tasklist를 진행하지 마십시오.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
