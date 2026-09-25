"""Draw the AlgoSplit write-up figures from the exported engine data.

Refresh the data first (see scripts/figures/algosplit_export.py), then run
from the site root:

    uv run --with matplotlib --with numpy python scripts/figures/algosplit.py

It writes src/assets/figures/algosplit/per-set-stimulus.svg and
src/assets/figures/algosplit/week-timeline.svg.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

import style

SLUG = "algosplit"
DATA = Path(__file__).resolve().parent / "data" / SLUG / "schedules.json"

# Where sets 4 to 6 land in each schedule, for the label over them.
SECOND = {"one": "Sets 4 to 6", "thu": "Thursday", "tue": "Tuesday"}


def load() -> dict:
    return json.loads(DATA.read_text())


def per_set_stimulus(data: dict) -> None:
    """Stimulus of each rear-delt set, one panel per schedule."""
    rows = data["schedules"]
    top = max(s["stimulus"] for r in rows for s in r["sets"])
    fig, axes = plt.subplots(1, 3, figsize=(style.WIDTH, 2.9), sharey=True)
    fig.subplots_adjust(left=0.1, right=0.99, wspace=0.12)
    x = range(1, 7)
    for ax, row in zip(axes, rows):
        values = [s["stimulus"] for s in row["sets"]]
        colors = [style.CONTEXT] * 3 + [style.RED] * 3
        ax.bar(x, values, width=0.62, color=colors, linewidth=0)
        ax.set_xticks(list(x))
        ax.set_xlim(0.4, 6.6)
        ax.set_ylim(0, top * 1.36)
        ax.set_title(row["label"], fontsize=12, fontweight="normal", color=style.INK, pad=6)
        # The sum of sets 4 to 6, the number the prose cites.
        tail = sum(values[3:])
        ax.text(5, max(values[3:]) + top * 0.05, f"{SECOND[row['key']]}\n{tail:.3f}",
                ha="center", va="bottom", fontsize=11.5, color=style.INK, linespacing=1.15)
        ax.tick_params(axis="x", length=0)
    axes[0].set_ylabel("Stimulus per set")
    axes[0].set_yticks([0, 0.2, 0.4, 0.6, 0.8])
    for ax in axes[1:]:
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[1].set_xlabel("Set of the week")
    style.save(fig, SLUG, "per-set-stimulus")


def week_timeline(data: dict) -> None:
    """Stimulus windows and idle stretches across the 168-hour week."""
    rows = data["schedules"]
    names = {0: "Mon", 24: "Tue", 72: "Thu"}
    fig, ax = plt.subplots(figsize=(style.WIDTH, 2.7))
    # Leave room inside the 6.4 in for the row labels and the atrophy column,
    # so the saved SVG is no wider than the other figures.
    fig.subplots_adjust(left=0.31, right=0.87)
    h = 0.34
    ys = list(range(len(rows)))[::-1]
    for y, row in zip(ys, rows):
        for lo, hi in row["windows"]:
            ax.barh(y, hi - lo, left=lo, height=h, color=style.GRID, linewidth=0)
        for lo, hi in row["idle"]:
            ax.barh(y, hi - lo, left=lo, height=h, color=style.RED, linewidth=0)
            label = f"{hi - lo} h idle" if y == ys[0] else f"{hi - lo} h"
            ax.text((lo + hi) / 2, y + h / 2 + 0.06, label, ha="center", va="bottom",
                    fontsize=11.5, color=style.INK)
        for t in row["session_hours"]:
            ax.plot([t], [y], marker="o", markersize=8, color=style.INK,
                    markeredgewidth=0, clip_on=False, zorder=3)
            ax.text(t + 2.5, y - h / 2 - 0.06, names[t], ha="left", va="top",
                    fontsize=11.5, color=style.INK_DIM)
        ax.text(176, y, f"{row['atrophy']:.3f}", ha="left", va="center",
                fontsize=12, color=style.INK)
    # Name the grey mark once, in the top row.
    lo, hi = rows[0]["windows"][0]
    ax.text((lo + hi) / 2, ys[0] + h / 2 + 0.06, f"{hi - lo} h window", ha="center",
            va="bottom", fontsize=11.5, color=style.INK)
    ax.text(176, ys[0] + h / 2 + 0.06, "Atrophy", ha="left", va="bottom",
            fontsize=11.5, color=style.INK_DIM)
    ax.set_yticks(ys, [r["label"] for r in rows])
    ax.tick_params(axis="y", length=0, pad=12, labelsize=12, labelcolor=style.INK)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 168)
    ax.set_ylim(-0.75, len(rows) - 0.35)
    ax.set_xticks(range(0, 169, 24))
    ax.set_xlabel("Hours from Monday's session")
    style.save(fig, SLUG, "week-timeline")


def main() -> None:
    style.use()
    data = load()
    per_set_stimulus(data)
    week_timeline(data)


if __name__ == "__main__":
    main()
