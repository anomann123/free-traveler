#!/usr/bin/env python3
"""build_waves.py

Traveler Task Manifest을 근거로 실행 순서(Wave)를 계산한다.

입력(실제 존재하는 경로 기준 — 지시된 `TASKS/details/TASK-*.md`는 이 저장소에
존재하지 않으며, 실제 상세 파일은 `TASKS/TASK-*.md`에 평면 구조로 있다. 이 스크립트는
후자를 읽는다):
    TASKS/TASK_MANIFEST.csv
    TASKS/TASK-*.md
    design-reference/SCREEN_ROUTE_CONTRACT.json

출력:
    TASKS/TASK_DAG.md       — Task 의존성 그래프(에지 목록 + 위상 레이어)
    TASKS/WAVE_PLAN.md      — Wave별 Task 목록 + Preview Checkpoint 표
    TASKS/WAVE_STATE.json   — Wave 실행 상태(schema_version/generated_at/waves[])
    TASKS/TASK_MANIFEST.csv — 기존 열 그대로 유지 + "Wave ID" 열 추가(덮어쓰기)

규칙(이 스크립트가 강제):
    1. Depends On을 읽어 순환 의존성을 검사한다. 순환이 있으면 출력 파일을 만들지 않고
       종료 코드 1로 중단한다.
    2. 선행 Task는 반드시 자신에 의존하는 Task보다 앞선(더 작은 번호의) Wave에 배치한다.
       같은 Wave에 두지 않는다(Wave 안에서는 Task ID 순으로 한 번에 하나씩 실행되므로,
       의존 관계가 있는 두 Task를 같은 Wave에 두면 ID 정렬이 우연히 의존 순서와 어긋날 때
       실행 순서가 깨질 수 있기 때문이다).
    3. 기본적으로 Wave당 4~7개 Task를 배치한다. 단, DB/AUTH처럼 의존 사슬이 길어
       한 단계에 준비되는 Task가 4개 미만인 구간은 규칙 2를 우선해 더 작은 Wave를
       허용한다(정확성이 균일한 크기보다 우선한다).
    4. Page Owner(PAGE-*) Task는 같은 화면 그룹의 마지막 Wave에 단독으로 배치하고
       `checkpoint_required=true`로 표시한다(`CLAUDE.md` 규칙 22의 Preview 대기 지점).
    5. Expected Files가 겹치는 Task는 같은 Wave에 넣지 않는다(파일 충돌 방지).
    6. Wave 내부에서도 Task ID 오름차순으로 한 개씩 실행한다는 전제를 유지한다
       (이 스크립트는 실행하지 않고 순서만 계획한다).
    7. 재시도/자동 수정 로직 등 복잡한 기능은 만들지 않는다.
    8. Git Branch·PR·Merge를 생성하는 기능은 포함하지 않는다(계획 산출물만 만든다).

사용법:
    python scripts/build_waves.py

종료 코드:
    0  성공(파일 생성 완료)
    1  순환 의존성 발견, 필수 입력 누락, 또는 배치 규칙(2) 위반 발생
"""

from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "TASKS"
MANIFEST_PATH = TASKS_DIR / "TASK_MANIFEST.csv"
DETAIL_GLOB = "TASK-*.md"
CONTRACT_PATH = ROOT / "design-reference" / "SCREEN_ROUTE_CONTRACT.json"

DAG_PATH = TASKS_DIR / "TASK_DAG.md"
WAVE_PLAN_PATH = TASKS_DIR / "WAVE_PLAN.md"
WAVE_STATE_PATH = TASKS_DIR / "WAVE_STATE.json"

MIN_WAVE_SIZE = 4
MAX_WAVE_SIZE = 7

GROUP_TITLES = {
    1: "Scaffold, 문서, Harness 확인",
    2: "Airbnb 스타일 공통 UI, 정적 데이터, Layout",
    3: "Supabase Auth, 6개 Table, 기본 RLS",
    4: "SCR-001 메인 Component와 Page Owner",
    5: "SCR-002 대표 소개 Component와 Page Owner",
    6: "SCR-003 여행 입력·외부 이동·동행글 입력 Component와 Page Owner",
    7: "SCR-004 동행 목록·상세·신청 Component와 Page Owner",
    8: "SCR-005 계정·내 활동·간단 관리자 Component와 Page Owner",
    9: "Unit·Playwright·접근성·CI",
    10: "Vercel Preview와 Release 확인",
}

FILE_PATH_RE = re.compile(r"`([^`\n]+\.(?:tsx?|sql|json|md|ya?ml))`")


@dataclass
class TaskRow:
    task_id: str
    category: str
    screen: str
    depends_on: list[str]
    expected_files: set[str] = field(default_factory=set)
    group: int = 1


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_manifest() -> tuple[list[dict], list[str]]:
    if not MANIFEST_PATH.exists():
        print(f"[FATAL] {MANIFEST_PATH} 가 없습니다. 먼저 scripts/audit_tasks.py를 실행해 매니페스트를 생성하십시오.")
        sys.exit(1)
    with MANIFEST_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    return rows, fieldnames


def split_cell_list(cell: str) -> list[str]:
    if not cell or cell.strip() in ("없음", "N/A", "-", ""):
        return []
    return [c.strip() for c in cell.split(",") if c.strip()]


def load_expected_files_from_details() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for path in TASKS_DIR.glob(DETAIL_GLOB):
        if path.name in ("TASK_AUDIT_REPORT.md",):
            continue
        task_id = path.stem[len("TASK-"):]
        text = path.read_text(encoding="utf-8")
        section = text
        if "## Expected Files" in text:
            section = text.split("## Expected Files", 1)[1]
            if "## Functional AC" in section:
                section = section.split("## Functional AC", 1)[0]
        result[task_id] = set(FILE_PATH_RE.findall(section))
    return result


def load_screens() -> dict[str, dict]:
    if not CONTRACT_PATH.exists():
        return {}
    data = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    return {s["screen_id"]: s for s in data.get("screens", [])}


def classify_group(task_id: str, category: str, screen: str) -> int:
    if task_id.startswith("CMP-SHARED") or category == "DATA":
        return 2
    if category in ("DB", "AUTH"):
        return 3
    if category in ("UNIT", "TEST") or task_id.startswith("E2E-") or task_id == "CI-LINT-BUILD":
        return 9
    if task_id.startswith("DEPLOY-"):
        return 10
    screen_group = {
        "SCR-001": 4, "SCR-002": 5, "SCR-003": 6, "SCR-004": 7, "SCR-005": 8,
    }
    for sid, grp in screen_group.items():
        if sid in (screen or ""):
            return grp
    return 1


# ---------------------------------------------------------------------------
# Cycle detection (3-color DFS)
# ---------------------------------------------------------------------------

def find_cycles(all_ids: set[str], dep_map: dict[str, list[str]]) -> list[str]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in all_ids}
    cycles: list[str] = []

    def dfs(node: str, path: list[str]) -> None:
        color[node] = GRAY
        path.append(node)
        for dep in dep_map.get(node, []):
            if dep not in all_ids:
                continue
            if color.get(dep) == GRAY:
                cyc = path[path.index(dep):] + [dep]
                cycles.append(" -> ".join(cyc))
            elif color.get(dep) == WHITE:
                dfs(dep, path)
        path.pop()
        color[node] = BLACK

    for tid in sorted(all_ids):
        if color[tid] == WHITE:
            dfs(tid, [])
    return cycles


# ---------------------------------------------------------------------------
# Wave building
# ---------------------------------------------------------------------------

@dataclass
class Wave:
    wave_id: str
    title: str
    task_ids: list[str]
    checkpoint_required: bool = False


def build_waves(tasks: dict[str, TaskRow]) -> list[Wave]:
    scheduled: set[str] = set()
    waves: list[Wave] = []
    wave_counter = 1

    for group_index in sorted(GROUP_TITLES):
        group_task_ids = [tid for tid, t in tasks.items() if t.group == group_index]
        page_ids = sorted(tid for tid in group_task_ids if tid.startswith("PAGE-") or tid.startswith("PO-"))
        nonpage_ids = set(tid for tid in group_task_ids if tid not in page_ids)

        while nonpage_ids:
            ready = sorted(
                tid for tid in nonpage_ids
                if set(tasks[tid].depends_on) <= scheduled
            )
            if not ready:
                unresolved = sorted(nonpage_ids)
                print(f"[FATAL] Wave 배치 실패: {GROUP_TITLES[group_index]} 그룹에서 준비되지 않는 Task {unresolved} "
                      f"(의존 Task가 아직 스케줄되지 않음, 그룹 순서 또는 Depends On을 확인하십시오)")
                sys.exit(1)

            chunk: list[str] = []
            used_files: set[str] = set()
            deferred: list[str] = []
            for tid in ready:
                if len(chunk) >= MAX_WAVE_SIZE:
                    deferred.append(tid)
                    continue
                files = tasks[tid].expected_files
                if files & used_files:
                    deferred.append(tid)
                    continue
                chunk.append(tid)
                used_files |= files
            if not chunk:
                # 전부 파일 충돌로 미뤄졌다면 최소 1개는 강제로 배치해 진행을 보장한다.
                chunk = [ready[0]]
                deferred = ready[1:]

            wave_id = f"W{wave_counter:02d}"
            waves.append(Wave(wave_id, GROUP_TITLES[group_index], chunk, checkpoint_required=False))
            scheduled.update(chunk)
            nonpage_ids -= set(chunk)
            wave_counter += 1

        for pid in page_ids:
            wave_id = f"W{wave_counter:02d}"
            waves.append(Wave(wave_id, f"{GROUP_TITLES[group_index]} — Page Owner 통합", [pid], checkpoint_required=True))
            scheduled.add(pid)
            wave_counter += 1

    return waves


def validate_wave_order(waves: list[Wave], tasks: dict[str, TaskRow]) -> list[str]:
    wave_index_of: dict[str, int] = {}
    for idx, w in enumerate(waves):
        for tid in w.task_ids:
            wave_index_of[tid] = idx
    violations = []
    for tid, t in tasks.items():
        for dep in t.depends_on:
            if dep not in wave_index_of or tid not in wave_index_of:
                continue
            if wave_index_of[dep] >= wave_index_of[tid]:
                violations.append(f"{tid}(Wave {waves[wave_index_of[tid]].wave_id})가 선행 Task {dep}"
                                   f"(Wave {waves[wave_index_of[dep]].wave_id})보다 먼저 또는 같은 Wave에 배치됨")
    return violations


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_manifest_with_wave(rows: list[dict], fieldnames: list[str], wave_of: dict[str, str]) -> None:
    out_fields = list(fieldnames)
    if "Wave ID" not in out_fields:
        out_fields.append("Wave ID")
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["Wave ID"] = wave_of.get(row.get("Task ID", ""), "")
            writer.writerow(row)


def write_dag(tasks: dict[str, TaskRow], waves: list[Wave]) -> None:
    wave_of = {tid: w.wave_id for w in waves for tid in w.task_ids}
    lines = [
        "# Task Dependency Graph (TASK_DAG.md)",
        "",
        "`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`의 Depends On 열로부터 생성했다. "
        "사람이 직접 편집하지 않는다 — 의존 관계를 바꾸려면 각 Task 상세 파일의 Depends On을 고치고 이 스크립트를 다시 실행한다.",
        "",
        "## 에지 목록 (선행 Task → 후행 Task)",
        "",
        "| 선행 Task | 후행 Task | 선행 Wave | 후행 Wave |",
        "|---|---|---|---|",
    ]
    edges = []
    for tid, t in sorted(tasks.items()):
        for dep in sorted(t.depends_on):
            edges.append((dep, tid))
    for dep, tid in edges:
        lines.append(f"| {dep} | {tid} | {wave_of.get(dep, '?')} | {wave_of.get(tid, '?')} |")
    if not edges:
        lines.append("| (없음) | | | |")

    lines += ["", "## Task별 Depends On", "", "| Task ID | Category | Screen | Depends On | Wave |", "|---|---|---|---|---|"]
    for tid, t in sorted(tasks.items()):
        deps = ", ".join(sorted(t.depends_on)) or "없음"
        lines.append(f"| {tid} | {t.category} | {t.screen or 'N/A'} | {deps} | {wave_of.get(tid, '?')} |")

    DAG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wave_plan(waves: list[Wave]) -> None:
    lines = [
        "# Free Traveler — Wave Plan",
        "",
        "`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`·`TASKS/TASK-*.md`·"
        "`design-reference/SCREEN_ROUTE_CONTRACT.json`을 근거로 생성했다. "
        "`/run-wave`는 이 문서와 `TASKS/WAVE_STATE.json`을 정본으로 사용한다.",
        "",
        "## Wave 요약",
        "",
        "| Wave | 그룹 | Task 수 | Preview Checkpoint |",
        "|---|---|---:|:---:|",
    ]
    for w in waves:
        lines.append(f"| {w.wave_id} | {w.title} | {len(w.task_ids)} | {'Y' if w.checkpoint_required else ''} |")

    lines += ["", "## Wave별 Task 목록", "", "| Wave | Task ID | Preview Checkpoint |", "|---|---|---|"]
    for w in waves:
        for i, tid in enumerate(w.task_ids):
            checkpoint = "Y" if (w.checkpoint_required and i == len(w.task_ids) - 1) else ""
            lines.append(f"| {w.wave_id} | {tid} | {checkpoint} |")

    lines += [
        "",
        "## 참고",
        "",
        "- Wave ID는 그룹 순서(1. Scaffold/문서/Harness → 10. Vercel Preview/Release)에 따라 순차 부여되었으며 W00~W10으로 미리 고정되지 않았다.",
        "- Page Owner(PAGE-*) Task는 해당 화면 그룹의 마지막 Wave에 단독 배치되고 `Preview Checkpoint=Y`다(`CLAUDE.md` 규칙 22).",
        "- DB/AUTH 그룹처럼 의존 사슬이 긴 구간은 4~7개 기본 범위보다 작은 Wave가 발생할 수 있다(의존 순서 정확성이 우선).",
        "- 이 문서는 계획 문서다. 자동 Branch 생성·PR 생성·Merge 기능은 포함하지 않는다.",
    ]
    WAVE_PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_wave_state(waves: list[Wave]) -> None:
    state = {
        "schema_version": "traveler-wave-state-v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "waves": [
            {
                "wave_id": w.wave_id,
                "title": w.title,
                "task_ids": w.task_ids,
                "status": "pending",
                "checkpoint_required": w.checkpoint_required,
                "checkpoint_result": None,
            }
            for w in waves
        ],
    }
    WAVE_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    rows, fieldnames = load_manifest()
    expected_files_map = load_expected_files_from_details()
    screens = load_screens()  # noqa: F841 (읽어서 존재 확인만 하며, Screen 값은 Manifest의 Screen 열을 신뢰한다)

    tasks: dict[str, TaskRow] = {}
    for row in rows:
        tid = row.get("Task ID", "").strip()
        if not tid:
            continue
        category = row.get("Category", "").strip()
        screen = row.get("Screen", "").strip()
        deps = split_cell_list(row.get("Depends On", ""))
        t = TaskRow(
            task_id=tid,
            category=category,
            screen=screen,
            depends_on=deps,
            expected_files=expected_files_map.get(tid, set()),
        )
        t.group = classify_group(tid, category, screen)
        tasks[tid] = t

    all_ids = set(tasks)
    for t in tasks.values():
        unknown = [d for d in t.depends_on if d not in all_ids]
        if unknown:
            print(f"[FATAL] {t.task_id}의 Depends On이 Manifest에 없는 Task를 참조: {unknown}")
            return 1

    dep_map = {tid: t.depends_on for tid, t in tasks.items()}
    cycles = find_cycles(all_ids, dep_map)
    if cycles:
        print(f"[FATAL] 순환 의존성 {len(cycles)}건 발견 — Wave Plan을 생성하지 않았습니다.")
        for c in cycles:
            print(f"  - {c}")
        return 1

    waves = build_waves(tasks)

    violations = validate_wave_order(waves, tasks)
    if violations:
        print(f"[FATAL] 배치 규칙(2) 위반 {len(violations)}건 — Wave Plan을 생성하지 않았습니다.")
        for v in violations:
            print(f"  - {v}")
        return 1

    wave_of = {tid: w.wave_id for w in waves for tid in w.task_ids}
    unassigned = sorted(all_ids - set(wave_of))
    if unassigned:
        print(f"[FATAL] Wave에 배치되지 않은 Task: {unassigned}")
        return 1

    write_dag(tasks, waves)
    write_wave_plan(waves)
    write_wave_state(waves)
    write_manifest_with_wave(rows, fieldnames, wave_of)

    page_owner_positions = [
        (tid, w.wave_id) for w in waves for tid in w.task_ids if tid.startswith("PAGE-") or tid.startswith("PO-")
    ]

    print("=== build_waves.py ===")
    print(f"순환 의존성: {len(cycles)}건")
    print(f"Wave 총 개수: {len(waves)}")
    print("")
    print("Wave별 Task 수:")
    for w in waves:
        marker = " [Preview Checkpoint]" if w.checkpoint_required else ""
        print(f"  {w.wave_id} ({w.title}): {len(w.task_ids)}개{marker}")
    print("")
    print("Page Owner 위치:")
    for tid, wid in page_owner_positions:
        print(f"  {tid} -> {wid}")
    print("")
    print(f"생성 완료: {DAG_PATH.relative_to(ROOT)}, {WAVE_PLAN_PATH.relative_to(ROOT)}, "
          f"{WAVE_STATE_PATH.relative_to(ROOT)}, {MANIFEST_PATH.relative_to(ROOT)}(Wave ID 열 추가)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
