"""Export the AlgoSplit numbers that the write-up figures draw.

Run from the AlgoSplit backend, in its own venv (the Rust wheel
`analysis_engine_rs` lives there):

    cd /Users/palerider/Desktop/projects/algosplit/backend && \
      PYTHONPATH=. .venv/bin/python \
      /Users/palerider/Desktop/projects/palerdr/scripts/figures/algosplit_export.py

It writes scripts/figures/data/algosplit/schedules.json: six reverse pec deck
sets a week in three schedules, per set and per week, with the stimulus
windows and the idle stretches that the model charges as atrophy.

Both engines score every schedule. The script stops if the Rust
engine and the Python reference differ by more than the site's parity
tolerance (1e-8).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

# backend/core/MainClasses.py: the Python reference engine.
from core.MainClasses import SCHOENFELD, Split
# backend/core/rust_analysis.py: adapter for the Rust engine
# (backend/rust/analysis_engine/src/engine.rs).
from core.rust_analysis import (
    NUMERIC_PARITY_TOLERANCE,
    run_rust_split_analysis,
    rust_engine_available,
)
from schemas.models import SplitRequest

OUT = Path(__file__).resolve().parent / "data" / "algosplit"

# App defaults: app/src/state/localPersistence.ts, DEFAULT_ANALYSIS_PREFERENCES
# (stimulusDuration 48, maintenanceVolume 3, dataset 'schoenfeld').
DURATION = 48
MAINTENANCE = 3
DATASET = "schoenfeld"
WEEK = 168

# Atrophy per idle hour: MuscleRegion.account_atrophy_through in
# MainClasses.py, atrophy_rate = cum[dataset][maintenance_volume - 1]
# / (168 - stimulus_duration).
S_MAINT = SCHOENFELD[MAINTENANCE - 1]
ATROPHY_RATE = S_MAINT / (WEEK - DURATION)

REAR = "posterior_deltoid"
PEC_DECK = "Reverse Pec Deck"

# The write-up's table: six rear-delt sets a week in three schedules.
# Day numbers are 1-indexed (Session.time = (day - 1) * 24 in MainClasses.py).
SCHEDULES = [
    {"key": "one", "label": "6 sets Monday", "sessions": [("Mon", 1, 6)]},
    {"key": "thu", "label": "3 Monday, 3 Thursday", "sessions": [("Mon", 1, 3), ("Thu", 4, 3)]},
    {"key": "tue", "label": "3 Monday, 3 Tuesday", "sessions": [("Mon", 1, 3), ("Tue", 2, 3)]},
]


def python_split(name, days, cycle):
    """Split.simulate_split in MainClasses.py, with per-set breakdowns."""
    split = Split(
        name, days, stimulus_duration=DURATION, maintenance_volume=MAINTENANCE,
        dataset=DATASET, cycle_length=cycle,
    )
    split.simulate_split(collect_breakdowns=True)
    return split


def rust_result(name, days, cycle):
    """analysis_engine_rs.analyze_split_json through run_rust_split_analysis."""
    req = SplitRequest(
        name=name,
        sessions=[
            {"name": n, "day": d, "exercises": [{"name": e, "sets": s} for e, s in ex]}
            for n, d, ex in days
        ],
        cycle_length=cycle, stimulus_duration=DURATION,
        maintenance_volume=MAINTENANCE, dataset=DATASET,
    )
    return {m.region_id: m for m in run_rust_split_analysis(req).muscles}


def check(label, a, b):
    if not math.isclose(a, b, rel_tol=0, abs_tol=NUMERIC_PARITY_TOLERANCE):
        raise SystemExit(f"parity failure at {label}: python {a!r} rust {b!r}")


def union(intervals):
    out = []
    for lo, hi in sorted(intervals):
        if out and lo <= out[-1][1]:
            out[-1][1] = max(out[-1][1], hi)
        else:
            out.append([lo, hi])
    return out


def export_schedules():
    rows = []
    for sched in SCHEDULES:
        days = [(n, d, [(PEC_DECK, s)]) for n, d, s in sched["sessions"]]
        py = python_split(sched["label"], days, 7)
        rust = rust_result(sched["label"], days, 7)
        muscle = py.muscles[REAR]

        # Per-set stimulus from the BreakdownRecord that
        # MuscleRegion.apply_stimulus stores for each set.
        sets = []
        for stats in py.session_stats:
            day = next(n for n, d, _ in sched["sessions"] if (d - 1) * 24 == stats["time"])
            for ex in stats["exercise_breakdowns"]:
                for bd in ex["muscle_contributions"][REAR]["sets"]:
                    sets.append({
                        "session": day,
                        "hour": stats["time"],
                        "set_in_session": bd.set_number,
                        "weight": bd.weight,
                        "marginal": bd.local_multiplier,
                        "cns": bd.global_multiplier,
                        "recovery": bd.recovery_multiplier,
                        "consecutive_day": bd.consecutive_day_multiplier,
                        "stimulus": bd.final_stimulus,
                    })

        # Windows and idle stretches, by the rule in account_atrophy_through:
        # a prime session opens a DURATION-hour window; each later hour until
        # the next prime session or the week's end is charged.
        hours = sorted((d - 1) * 24 for _, d, _ in sched["sessions"])
        windows = union([[h, min(h + DURATION, WEEK)] for h in hours])
        idle, cursor = [], 0
        for lo, hi in windows:
            if lo > cursor and cursor > 0:
                idle.append([cursor, lo])
            cursor = hi
        if cursor < WEEK:
            idle.append([cursor, WEEK])
        idle_hours = sum(hi - lo for lo, hi in idle)

        stimulus, atrophy = muscle.stimulus, muscle.atrophy
        check(f"{sched['key']} stimulus", stimulus, rust[REAR].stimulus)
        check(f"{sched['key']} atrophy", atrophy, rust[REAR].atrophy)
        check(f"{sched['key']} net", stimulus - atrophy, rust[REAR].net_stimulus)
        check(f"{sched['key']} per-set sum", sum(s["stimulus"] for s in sets), stimulus)
        check(f"{sched['key']} idle hours", idle_hours * ATROPHY_RATE, atrophy)

        rows.append({
            "key": sched["key"],
            "label": sched["label"],
            "session_hours": hours,
            "sets": sets,
            "windows": windows,
            "idle": idle,
            "idle_hours": idle_hours,
            "stimulus": stimulus,
            "atrophy": atrophy,
            "net": stimulus - atrophy,
        })

    data = {
        "source": "algosplit backend/core/MainClasses.py Split.simulate_split; "
                  "Rust parity via backend/core/rust_analysis.py",
        "stimulus_duration_h": DURATION,
        "maintenance_volume": MAINTENANCE,
        "dataset": DATASET,
        "s_maintenance": S_MAINT,
        "atrophy_rate_per_h": ATROPHY_RATE,
        "schedules": rows,
    }
    (OUT / "schedules.json").write_text(json.dumps(data, indent=1) + "\n")


def main():
    if not rust_engine_available():
        raise SystemExit("analysis_engine_rs is not importable in this venv")
    OUT.mkdir(parents=True, exist_ok=True)
    export_schedules()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
