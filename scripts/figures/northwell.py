"""Figures for the Northwell write-up (src/content/projects/northwell.md).

Run from the site root:

    uv run --with matplotlib --with numpy python scripts/figures/northwell.py

term_overlap.svg is a method diagram. The page stays at method level, so its
document and questions are an invented example, with no Northwell table,
column or question in it. group_folds.svg reads
scripts/figures/data/northwell/group_folds.json, which northwell_export.py
writes from the Kaggle repo's splitters.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.lines import Line2D

import style

DATA = Path(__file__).resolve().parent / "data" / "northwell"
SLUG = "northwell"


# --- term_overlap -------------------------------------------------------------

# An invented schema entry and two questions that ask for the same count. The
# first question names the column. The second uses business words and shares
# no word with the entry, so a keyword (BM25) search scores the entry 0 for it.
DOC = "Readmission flag: marks a stay that follows a recent discharge"
Q_COLUMN = "Readmission flag count per stay"
Q_BUSINESS = "How many patients came back soon after they went home?"

# Links drawn to the document: (question word index, document word index).
# Word indices count the whitespace-separated words of each string from 0.
SAME_WORD = [(0, 0), (1, 1), (4, 4)]  # readmission, flag, stay
SAME_MEANING = [((3, 4), 0), (5, 8), ((8, 9), 9)]  # came back, soon, went home


def words(s: str) -> set[str]:
    return set(re.findall(r"[a-z]+", s.lower()))


def place_words(ax, text: str, x0: float, y: float, **kw) -> list[tuple[float, float]]:
    """Draw text word by word from x0 and return each word's (left, right) in data units.

    The axes fill the figure and the data units are inches, so a width in
    pixels divided by the dpi is a width in data units.
    """
    fig = ax.figure
    # Measure with an Agg renderer at the figure's dpi. The SVG canvas measures
    # at 72 dpi, so its widths do not divide by fig.dpi. savefig still writes SVG.
    renderer = FigureCanvasAgg(fig).get_renderer()

    def width(s: str) -> float:
        t = ax.text(0, 0, s, **kw)
        w = t.get_window_extent(renderer).width / fig.dpi
        t.remove()
        return w

    w_space = width("a a") - width("aa")
    spans = []
    x = x0
    for w in text.split(" "):
        ax.text(x, y, w, ha="left", va="baseline", **kw)
        right = x + width(w)
        spans.append((x, right))
        x = right + w_space
    return spans


def mid(spans, idx) -> float:
    if isinstance(idx, tuple):
        return (spans[idx[0]][0] + spans[idx[-1]][1]) / 2
    return (spans[idx][0] + spans[idx][1]) / 2


def term_overlap() -> None:
    # The example must hold: three shared words for the first question, none for the second.
    assert words(Q_COLUMN) & words(DOC) == {"stay", "readmission", "flag"}
    assert not words(Q_BUSINESS) & words(DOC)

    W, H = style.WIDTH, 2.55
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    label = dict(fontsize=11.5, color=style.INK_DIM)
    body = dict(fontsize=12.5, color=style.INK)
    x0 = 0.02

    # Rows, top to bottom (baselines, in inches).
    y_label_a, y_a, y_doc, y_b, y_label_b = 2.36, 2.05, 1.18, 0.40, 0.08
    cap = 0.13  # height of lowercase letters above the baseline, near enough for link ends

    ax.text(x0, y_label_a, "Question that names the column", va="baseline", **label)
    ax.text(W - 0.02, y_label_a, "3 shared words", ha="right", va="baseline", **label)
    a = place_words(ax, Q_COLUMN, x0, y_a, **body)

    doc = place_words(ax, DOC, x0 + 0.12, y_doc, **body)
    # The document sits in an ink box, the way a retrieved entry would.
    ax.add_patch(
        plt.Rectangle(
            (x0, y_doc - 0.13),
            doc[-1][1] + 0.12 - x0,
            0.42,
            fill=False,
            edgecolor=style.INK,
            linewidth=0.9,
            joinstyle="round",
        )
    )
    ax.text(doc[-1][1] + 0.24, y_doc + 0.03, "Schema\nentry", va="center", linespacing=1.1, **label)

    b = place_words(ax, Q_BUSINESS, x0, y_b, **body)
    ax.text(x0, y_label_b, "Question in business language", va="baseline", **label)
    ax.text(W - 0.02, y_label_b, "0 shared words", ha="right", va="baseline", **label)

    box_top, box_bottom = y_doc + 0.29, y_doc - 0.13
    for qi, di in SAME_WORD:
        ax.plot([mid(a, qi), mid(doc, di)], [y_a - 0.07, box_top], color=style.CONTEXT, lw=1.5)
    for qi, di in SAME_MEANING:
        ax.plot([mid(b, qi), mid(doc, di)], [y_b + cap + 0.07, box_bottom], color=style.RED, lw=1.5)

    # Each link label sits just right of its rightmost link.
    x_word = max(mid(a, qi) for qi, _ in SAME_WORD) + 0.16
    ax.text(x_word, (y_a + box_top) / 2 - 0.03, "same word", ha="left", va="center", **label)
    x_meaning = max(mid(doc, di) for _, di in SAME_MEANING) + 0.14
    ax.text(
        x_meaning,
        (y_b + cap + box_bottom) / 2 + 0.02,
        "same meaning,\nno shared word",
        ha="left",
        va="center",
        linespacing=1.1,
        **label,
    )
    style.save(fig, SLUG, "term_overlap")


# --- group_folds --------------------------------------------------------------


def group_folds() -> None:
    data = json.loads((DATA / "group_folds.json").read_text())
    rows = data["passengers"]

    # One x slot per passenger, with an empty slot between groups.
    xs, groups, x = [], [], 0
    for i, r in enumerate(rows):
        if i and r["group"] != rows[i - 1]["group"]:
            x += 1
        xs.append(x)
        groups.append(r["group"])
        x += 1

    fig, axes = plt.subplots(2, 1, figsize=(style.WIDTH, 3.35), sharex=True)
    panels = [("fold_plain", "Plain stratified split"), ("fold_grouped", "Grouped split")]
    order = list(dict.fromkeys(groups))

    for ax, (key, name) in zip(axes, panels):
        for g in order:
            idx = [i for i, gg in enumerate(groups) if gg == g]
            gx = [xs[i] for i in idx]
            gy = [rows[i][key] for i in idx]
            split = len(set(gy)) > 1
            color = style.RED if split else style.CONTEXT
            ax.plot(
                gx,
                gy,
                color=color,
                lw=1.5,
                marker="o",
                ms=6.5,
                mec=style.PAPER,
                mew=0,
                zorder=3 if split else 2,
            )
        ax.set_ylim(5.6, 0.4)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_ylabel("Fold")
        ax.text(0, 1.04, name, transform=ax.transAxes, fontsize=12.5, color=style.INK, va="bottom")
        ax.tick_params(axis="x", length=0)

    centres = [sum(xs[i] for i, gg in enumerate(groups) if gg == g) / groups.count(g) for g in order]
    axes[1].set_xticks(centres, order)
    axes[1].set_xlabel("Travel group, the first part of the passenger ID")
    axes[1].set_xlim(-0.8, xs[-1] + 0.8)
    for ax in axes:
        ax.spines["bottom"].set_visible(False)

    handles = [
        Line2D([], [], color=style.RED, lw=1.5, marker="o", ms=6.5, mec=style.PAPER, mew=0),
        Line2D([], [], color=style.CONTEXT, lw=1.5, marker="o", ms=6.5, mec=style.PAPER, mew=0),
    ]
    axes[0].legend(
        handles,
        ["group split across folds", "group in one fold"],
        loc="lower left",
        bbox_to_anchor=(-0.012, 1.2),
        ncol=2,
        handlelength=1.8,
        columnspacing=1.2,
        borderaxespad=0.1,
        labelcolor=style.INK,
    )
    fig.subplots_adjust(hspace=0.5)
    style.save(fig, SLUG, "group_folds")


if __name__ == "__main__":
    style.use()
    term_overlap()
    group_folds()
