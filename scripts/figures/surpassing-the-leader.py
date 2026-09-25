"""Draw the Surpassing the Leader figures from the exported data.

Run the export first (see surpassing-the-leader_export.py), then, from the site root:

    uv run --with matplotlib --with numpy python scripts/figures/surpassing-the-leader.py

Every number drawn here comes from scripts/figures/data/surpassing-the-leader/,
which the export pulls out of src/dth_compact/main.py, its table V.npy, and the
leap-aware solve's certified slices.

The page scales each SVG to the column width, so every figure fills the full
style.WIDTH after the tight crop; a narrower file would enlarge its text.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import style

SLUG = "surpassing-the-leader"
DATA = Path(__file__).resolve().parent / "data" / SLUG
NOTE = 11.5  # annotation size; phones show the figure near 55 percent


def read_csv(name: str) -> dict[str, np.ndarray]:
    with (DATA / name).open(encoding="ascii") as handle:
        rows = list(csv.DictReader(handle))
    return {key: np.array([float(r[key]) for r in rows]) for key in rows[0]}


def opening_strategies() -> None:
    """Both players' equilibrium over seconds 1..60 in the opening round (main.try_rung2 at the root)."""
    d = read_csv("opening_round.csv")
    second, drop, check = d["second"], 100 * d["drop"], 100 * d["check"]

    fig, ax = plt.subplots(figsize=(style.WIDTH, 3.0), layout="constrained")
    # A log axis holds the 27.3 percent spikes and the 0.6 to 2.1 percent curves on one scale.
    ax.set_yscale("log")
    ax.plot(second[1:], drop[1:], color=style.RED, lw=1.5)
    ax.plot(second[:-1], check[:-1], color=style.INK, lw=1.5)
    ax.plot([1], [drop[0]], "o", ms=7, color=style.RED, mec=style.PAPER, mew=1.5, zorder=4)
    ax.plot([60], [check[-1]], "o", ms=7, color=style.INK, mec=style.PAPER, mew=1.5, zorder=4)
    ax.text(3, drop[0], f"Dropper: {drop[0]:.1f}% on second 1", va="center", fontsize=NOTE)
    ax.text(58, check[-1], f"Checker: {check[-1]:.1f}% on second 60", va="center", ha="right", fontsize=NOTE)
    ax.text(40, drop[39] * 1.18, "Dropper", ha="center", va="bottom", fontsize=NOTE)
    ax.text(40, check[39] / 1.18, "Checker", ha="center", va="top", fontsize=NOTE)
    ax.set_xlim(0, 61)
    ax.set_ylim(0.4, 45)
    ax.set_xticks([1, 10, 20, 30, 40, 50, 60])
    ax.set_yticks([0.5, 1, 2, 5, 10, 20])
    ax.set_yticklabels(["0.5", "1", "2", "5", "10", "20"])
    ax.minorticks_off()
    ax.set_xlabel("Second chosen")
    ax.set_ylabel("Probability (%)")
    style.save(fig, SLUG, "opening-strategies")


def revival_map() -> None:
    """Where one player can still survive an injection: p(s, t) > 0 in red, p = 0 in grey."""
    c = json.loads((DATA / "revival.json").read_text(encoding="ascii"))
    edge = c["max_s_plus_t"]
    top = c["s_max"]

    fig, ax = plt.subplots(figsize=(style.WIDTH, 3.1), layout="constrained")
    ax.add_patch(plt.Rectangle((0, 0), top, top, color=style.GRID, lw=0, zorder=1))
    # p > 0 exactly when s <= 239 and s + t <= 240: the triangle under the line s + t = 240.
    ax.add_patch(plt.Polygon([(0, 0), (edge, 0), (0, edge)], closed=True, color=style.RED, lw=0, zorder=2))
    ax.text(50, 60, "revival possible, $p>0$", ha="left", va="center", fontsize=NOTE, color=style.PAPER, zorder=3)
    ax.text(215, 200, "$p=0$", ha="center", va="center", fontsize=13, zorder=3)
    # On the grey side of the edge, clear of the red.
    ax.text(160, 100, "$s+t=240$", rotation=-45, rotation_mode="anchor", ha="center", va="bottom",
            fontsize=NOTE, transform_rotates_text=True, zorder=3)
    ax.set_xlim(0, top)
    ax.set_ylim(0, top)
    ax.set_xticks([0, 60, 120, 180, 240, 300])
    ax.set_yticks([0, 60, 120, 180, 240, 300])
    ax.set_xlabel("Cylinder $s$ (seconds)")
    ax.set_ylabel("Time dead $t$ (seconds)")
    style.save(fig, SLUG, "revival-regions")


def round_payoffs() -> None:
    """The opening round's 61 distinct payoffs (main.full_matrix): S at each lag c - d, and F."""
    d = read_csv("opening_round.csv")
    success, fail = d["success_win"], float(d["fail_win"][0])
    lag = np.arange(success.size)  # c - d = 0 .. 59

    fig, ax = plt.subplots(figsize=(style.WIDTH, 2.9), layout="constrained")
    ax.hlines(0.5, 0, 59, color=style.AXIS, lw=0.75, zorder=1)
    ax.hlines(fail, 0, 59, color=style.INK, lw=1.5, zorder=2)
    ax.plot(lag, success, color=style.RED, lw=1.5, zorder=3)
    for x, y in ((0, success[0]), (59, success[-1])):
        ax.plot([x], [y], "o", ms=7, color=style.RED, mec=style.PAPER, mew=1.5, zorder=4)
    ax.text(1.5, success[0], f"{success[0]:.3f}", va="center", fontsize=NOTE)
    ax.text(57.5, success[-1] + 0.004, f"{success[-1]:.3f}", ha="right", va="bottom", fontsize=NOTE)
    ax.text(30, success[30] - 0.012, "check succeeds, $c\\geq d$: $S_{c-d}$", ha="left", va="top", fontsize=NOTE)
    ax.text(1, fail + 0.006, f"check fails, $c<d$: $F={fail:.3f}$", ha="left", va="bottom", fontsize=NOTE)
    ax.set_xlim(-1, 60)
    ax.set_ylim(0.44, 0.63)
    ax.set_xticks([0, 10, 20, 30, 40, 50, 59])
    ax.set_yticks([0.45, 0.5, 0.55, 0.6])
    ax.set_xlabel("Lag $c-d$ in seconds")
    ax.set_ylabel("Dropper's win probability")
    style.save(fig, SLUG, "round-payoffs")


def value_by_poison() -> None:
    """The Dropper's win probability as one cylinder fills, the other player fresh (V.npy, 2 s steps)."""
    d = read_csv("value_surface.csv")
    fresh = read_csv("fresh_checker.csv")
    own = d["checker_s"] == 0      # the Dropper's own cylinder fills, the Checker at (0, 0)
    other = d["dropper_s"] == 0    # the Checker's cylinder fills, the Dropper at (0, 0)
    root = float(d["dropper_win"][own & other][0])
    # The last whole second of Dropper poison that still leaves the Dropper ahead of a fresh Checker.
    ahead = int(fresh["dropper_s"][fresh["dropper_win"] > 0.5].max())
    assert ahead == 16, ahead

    fig, ax = plt.subplots(figsize=(style.WIDTH, 2.9), layout="constrained")
    ax.hlines(0.5, 0, 298, color=style.AXIS, lw=0.75, zorder=1)
    ax.plot(d["checker_s"][other], d["dropper_win"][other], color=style.INK, lw=1.5, zorder=2)
    ax.plot(d["dropper_s"][own], d["dropper_win"][own], color=style.RED, lw=1.5, zorder=3)
    ax.plot([0], [root], "o", ms=7, color=style.INK, mec=style.PAPER, mew=1.5, zorder=5, clip_on=False)
    ax.plot([ahead], [0.5], "o", ms=7, color=style.RED, mec=style.PAPER, mew=1.5, zorder=5)
    # Above the black line, which reaches 0.74 only near 75 s, with a leader down to the start.
    ax.annotate(f"start: {root:.4f}", xy=(0, root), xytext=(8, 0.74), ha="left", va="bottom",
                fontsize=NOTE, annotation_clip=False,
                arrowprops=dict(arrowstyle="-", color=style.INK, lw=0.75, relpos=(0, 0), shrinkA=1, shrinkB=5))
    # In the gap between the 0.5 line and the black line.
    ax.text(ahead + 6, 0.515, f"even at {ahead} s", ha="left", va="bottom", fontsize=NOTE)
    ax.text(150, 0.93, "Checker's cylinder fills", ha="center", va="bottom", fontsize=NOTE)
    ax.text(150, 0.24, "Dropper's cylinder fills", ha="left", va="bottom", fontsize=NOTE)
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 1.02)
    ax.set_xticks([0, 60, 120, 180, 240, 300])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xlabel("Seconds of poison in one cylinder, the other player fresh")
    ax.set_ylabel("Dropper's win probability")
    style.save(fig, SLUG, "value-by-poison")


def leap_minutes() -> None:
    """Leap-aware solve: Hal as Dropper at (0, 180) against Baku at (60, 120), minute by minute."""
    d = read_csv("leap_minutes.csv")
    minute = d["minute"]
    fig, (top, low) = plt.subplots(2, 1, sharex=True, figsize=(style.WIDTH, 3.5), layout="constrained",
                                   gridspec_kw={"height_ratios": [1, 1]})
    top.hlines(0.5, 44, 59, color=style.AXIS, lw=0.75, zorder=1)
    top.plot(minute, d["hal_win"], color=style.INK, lw=1.5, marker="o", ms=5.5, mec=style.PAPER, mew=1.0)
    top.set_ylim(0, 1)
    top.set_yticks([0, 0.5, 1])
    top.set_ylabel("Hal wins")
    hi, lo = int(np.argmax(d["hal_win"])), int(np.argmin(d["hal_win"]))
    top.text(minute[lo], d["hal_win"][lo] - 0.07, f"{d['hal_win'][lo]:.2f}", ha="center", va="top", fontsize=NOTE)
    top.text(minute[hi], d["hal_win"][hi] + 0.07, f"{d['hal_win'][hi]:.2f}", ha="center", va="bottom", fontsize=NOTE)

    low.plot(minute, d["drop_second_1"], color=style.RED, lw=1.5, marker="o", ms=5.5, mec=style.PAPER, mew=1.0)
    low.plot(minute, d["drop_second_2"], color=style.INK, lw=1.5, marker="o", ms=5.5, mec=style.PAPER, mew=1.0)
    low.set_ylim(-0.05, 1.05)
    low.set_yticks([0, 0.5, 1])
    low.set_ylabel("Drop weight")
    low.text(59.4, d["drop_second_1"][-1], "second 1", va="center", fontsize=NOTE)
    low.text(59.4, d["drop_second_2"][-1], "second 2", va="center", fontsize=NOTE)
    low.set_xlim(43.6, 62.6)
    low.set_xticks([44, 47, 50, 53, 56, 59])
    low.set_xticklabels(["8:44", "8:47", "8:50", "8:53", "8:56", "8:59"])
    low.set_xlabel("Clock when Hal drops")
    for ax in (top, low):
        ax.spines["bottom"].set_bounds(44, 59)
    fig.align_ylabels((top, low))
    style.save(fig, SLUG, "leap-minutes")


def main() -> None:
    style.use()
    opening_strategies()
    revival_map()
    round_payoffs()
    value_by_poison()
    leap_minutes()


if __name__ == "__main__":
    main()
