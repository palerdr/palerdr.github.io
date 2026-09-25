"""Export the data behind the Surpassing the Leader figures from the project repo.

The numbers come from the paper's one-file solver, src/dth_compact/main.py, and
its finished table src/dth_compact/artifacts/V.npy (memory-mapped, never
copied). Run from the site root, in the solver's own uv project:

    uv run --project ../usogui/stl/src/dth_compact python scripts/figures/surpassing-the-leader_export.py

It writes four small files to scripts/figures/data/surpassing-the-leader/:

- opening_round.csv: the opening round's 61 distinct payoffs and both players'
  equilibrium strategies over seconds 1..60.
- revival.json: the revival formula's constants, checked against the solver on
  every integer (s, t), and the count of reachable pairs with p > 0.
- value_surface.csv: the Dropper's win probability with both t = 0, over both
  cylinders in 2-second steps.
- fresh_checker.csv: the same probability in 1-second steps of the Dropper's
  cylinder, with the Checker at (0, 0).
- leap_minutes.csv: from the leap-aware solve, Hal's value and drop strategy at
  one pair of loads in each minute from 8:44 to 8:59. The STL repo's
  paper/make_stl_figures.py certifies these slices from the completed table
  src/stl/outputs/leap-full-native and writes paper/build/figures/stl/
  strategy_surface.json; this export copies them after checking the residuals.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

SITE = Path(__file__).resolve().parents[2]
REPO = SITE.parent / "usogui" / "stl"
COMPACT = REPO / "src" / "dth_compact"
OUT = SITE / "scripts" / "figures" / "data" / "surpassing-the-leader"

sys.path.insert(0, str(COMPACT))
import main as solver  # noqa: E402


def win(value: float) -> float:
    # main.py stores V = win - loss for the current Dropper (paper section 4), so win = (1 + V) / 2.
    return 0.5 * (1.0 + float(value))


def export_opening_round(table: solver.ProfileTable, V: np.ndarray) -> dict:
    """The opening round (0, 0, 0, 0): its payoffs S_1..S_60 and F, and the certified equalizer pair."""
    # main.encode_state / main.decode_class: the class of the starting state, Checker first.
    pc, pd = solver.decode_class(solver.encode_state(0, 0, 0, 0, table))
    # main.class_values: S_l = -V(x_l) for l = 1..60 and F = p(-V(x_f)) + 1 - p (paper section 4).
    s, f = solver.class_values(pc, pd, V, table)
    # main.try_rung2: the 59-step recurrence gives both strategies; drop[k] = check[59 - k].
    result = solver.try_rung2(s, f)
    if result is None or not result.certified:
        raise SystemExit("the opening round is not certified by the equalizer rung")
    stored = float(V[pc, pd])
    if abs(result.value - stored) > solver.MAX_SADDLE_GAP:
        raise SystemExit("the equalizer value does not match the stored root value")
    # main.full_matrix: M[d, c] = S_{c-d+1} for c >= d, else F. Count its distinct entries.
    distinct = np.unique(solver.full_matrix(s, f)).size
    with (OUT / "opening_round.csv").open("w", newline="", encoding="ascii") as handle:
        out = csv.writer(handle)
        out.writerow(["second", "drop", "check", "success_win", "fail_win"])
        for k in range(solver.LAGS):
            # success_win is S_l as the Dropper's win probability, with lag l = k + 1.
            out.writerow([k + 1, f"{result.drop[k]:.10f}", f"{result.check[k]:.10f}",
                          f"{win(s[k]):.10f}", f"{win(f):.10f}"])
    return {"root_value": stored, "root_win": win(stored), "saddle_gap": result.saddle_gap,
            "distinct_entries": int(distinct)}


def export_revival(table: solver.ProfileTable) -> dict:
    """Check the closed form against main.revival_probability on every integer (s, t), then store it."""
    s = np.arange(solver.MAX_ST + 1)[:, None]
    t = np.arange(solver.MAX_TTD + 1)[None, :]
    # main.survives_injection: s + DOSE <= MAX_ST and s + DOSE + t <= MAX_TTD, i.e. s <= 239 and s + t <= 240.
    support = (s + solver.DOSE <= solver.MAX_ST) & (s + solver.DOSE + t <= solver.MAX_TTD)
    closed = np.where(support, 0.95 * (1 - s / 240.0) * 0.75 ** (t / 60.0), 0.0)
    exact = np.array([[solver.revival_probability(int(a), int(b)) for b in range(solver.MAX_TTD + 1)]
                      for a in range(solver.MAX_ST + 1)])
    gap = float(np.abs(closed - exact).max())
    if gap > 1e-15:
        raise SystemExit(f"closed form differs from main.revival_probability by {gap}")
    # main.build_table: the reachable t values are 0 and 60..300; N_ALIVE of those pairs have p > 0.
    reachable_t = [0, *range(60, solver.MAX_TTD + 1)]
    pairs = (solver.MAX_ST + 1) * len(reachable_t)
    positive = int(np.count_nonzero(exact[:, reachable_t] > 0))
    if positive != solver.N_ALIVE:
        raise SystemExit(f"{positive} reachable pairs have p > 0, expected {solver.N_ALIVE}")
    data = {
        "source": "src/dth_compact/main.py: revival_probability, survives_injection, build_table",
        "p0": 0.95, "s_scale": 240, "t_base": 0.75, "t_scale": 60,
        "max_s_alive": solver.MAX_ST - solver.DOSE, "max_s_plus_t": solver.MAX_TTD - solver.DOSE,
        "s_max": solver.MAX_ST, "t_max": solver.MAX_TTD,
        "max_abs_gap_vs_solver": gap,
        "reachable_pairs": pairs, "reachable_positive": positive,
    }
    (OUT / "revival.json").write_text(json.dumps(data, indent=2) + "\n", encoding="ascii")
    return {"reachable_pairs": pairs, "reachable_positive": positive}


def export_value_surface(table: solver.ProfileTable, V: np.ndarray) -> dict:
    """V[pc, pd] at (s_c, 0, s_d, 0): the Dropper's win probability over both cylinders."""
    step = 2
    grid = range(0, solver.MAX_ST + 1, step)
    rows = []
    for sc in grid:
        for sd in grid:
            pc, pd = solver.decode_class(solver.encode_state(sc, 0, sd, 0, table))
            rows.append((sd, sc, win(V[pc, pd])))
    # The 1-second row at a fresh Checker, to find where the Dropper's edge runs out.
    fresh = []
    for sd in range(0, 61):
        pc, pd = solver.decode_class(solver.encode_state(0, 0, sd, 0, table))
        fresh.append((sd, win(V[pc, pd])))
    with (OUT / "value_surface.csv").open("w", newline="", encoding="ascii") as handle:
        out = csv.writer(handle)
        out.writerow(["dropper_s", "checker_s", "dropper_win"])
        for sd, sc, w in rows:
            out.writerow([sd, sc, f"{w:.6f}"])
    with (OUT / "fresh_checker.csv").open("w", newline="", encoding="ascii") as handle:
        out = csv.writer(handle)
        out.writerow(["dropper_s", "dropper_win"])
        for sd, w in fresh:
            out.writerow([sd, f"{w:.10f}"])
    last_ahead = max(sd for sd, w in fresh if w > 0.5)
    return {"last_dropper_s_above_half": last_ahead,
            "win_at_last": dict(fresh)[last_ahead], "win_after": dict(fresh)[last_ahead + 1]}


def export_leap_minutes() -> dict:
    """Hal as Dropper at (0, 180) against Baku at (60, 120), one certified slice per minute."""
    evidence = json.loads((REPO / "paper" / "build" / "figures" / "stl" / "strategy_surface.json").read_text())
    rows = []
    for r in evidence["records"]:
        drop = np.array(r["drop"])
        if r["bellman_residual"] > 1e-6 or r["gap"] > 1e-6 or abs(drop.sum() - 1) > 1e-9:
            raise SystemExit(f"minute {r['minute']}: slice fails its certificate")
        # V is Hal's win minus loss as the Dropper (stl.tex section 3), so his win is (1 + V) / 2.
        rows.append((r["minute"], win(r["value"]), drop[0], drop[1]))
    with (OUT / "leap_minutes.csv").open("w", newline="", encoding="ascii") as handle:
        out = csv.writer(handle)
        out.writerow(["minute", "hal_win", "drop_second_1", "drop_second_2"])
        for minute, w, p1, p2 in rows:
            out.writerow([minute, f"{w:.6f}", f"{p1:.6f}", f"{p2:.6f}"])
    return {"source": evidence["source"], "hal": evidence["hal"], "baku": evidence["baku"],
            "minutes": [r[0] for r in rows], "hal_win_range": [min(r[1] for r in rows), max(r[1] for r in rows)]}


def main() -> None:
    values = COMPACT / "artifacts" / "V.npy"
    V = np.load(values, mmap_mode="r")
    if V.shape != (solver.N, solver.N + 1):
        raise SystemExit(f"{values} has shape {V.shape}, expected {(solver.N, solver.N + 1)}")
    OUT.mkdir(parents=True, exist_ok=True)
    table = solver.build_table()
    summary = {
        "opening_round": export_opening_round(table, V),
        "revival": export_revival(table),
        "value_surface": export_value_surface(table, V),
        "leap_minutes": export_leap_minutes(),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
