"""The shared look of the write-up figures.

Every figure script imports this module, calls `use()`, and writes its figure
with `save()`. The figures use the site's ink for text, one red for the series
the figure is about, grey for context, PT Sans, and hairline axes. Text leaves
as paths, so an SVG looks the same in any browser without the web font.

Run a figure script from the site root:

    uv run --with matplotlib --with numpy python scripts/figures/<script>.py
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("svg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1]
ASSETS = SITE / "src" / "assets" / "figures"
PROJECTS = SITE.parent

# The site's tokens (src/styles/global.css). Red and black carry the figures:
# red for the series a paragraph is about, black for the one it is set against.
# Figures use lines, points and flat marks, and no color gradients.
INK = "#0a0a0a"
INK_DIM = "#383838"
AXIS = "#c9c9c4"
GRID = "#e3e3e0"
PAPER = "#ffffff"
RED = "#c0142a"
CONTEXT = INK

# The column shows a figure at up to 36rem, so 6.4 in keeps 12.5 pt text near
# the body size on a laptop.
WIDTH = 6.4
# save() pads every SVG to this width, centred. The page scales each figure to
# the same width, so equal canvases give equal text sizes across write-ups.
CANVAS_PT = 480.0

for font in (HERE / "fonts").glob("*.ttf"):
    font_manager.fontManager.addfont(str(font))


def use() -> None:
    plt.rcParams.update(
        {
            "font.family": "PT Sans",
            "font.size": 12.5,
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.labelsize": 12.5,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.edgecolor": AXIS,
            "axes.linewidth": 0.75,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,
            "grid.color": GRID,
            "grid.linewidth": 0.75,
            "grid.linestyle": "-",
            "xtick.color": AXIS,
            "ytick.color": AXIS,
            "xtick.labelcolor": INK_DIM,
            "ytick.labelcolor": INK_DIM,
            "xtick.labelsize": 11.5,
            "ytick.labelsize": 11.5,
            "xtick.major.width": 0.75,
            "ytick.major.width": 0.75,
            "lines.linewidth": 1.5,
            "lines.solid_capstyle": "round",
            "lines.solid_joinstyle": "round",
            "legend.frameon": False,
            "legend.fontsize": 11.5,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "svg.fonttype": "path",
            # Computer Modern, so math in a label matches the page's KaTeX.
            "mathtext.fontset": "cm",
            # Stable element ids, so a rerun with the same data gives the same file.
            "svg.hashsalt": "palerdr-figures",
        }
    )


def save(fig: plt.Figure, writeup: str, name: str) -> Path:
    """Write src/assets/figures/<writeup>/<name>.svg and close the figure."""
    out = ASSETS / writeup
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.svg"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06, metadata={"Date": None})
    plt.close(fig)
    _pad_to_canvas(path)
    return path


def _pad_to_canvas(path: Path) -> None:
    """Widen the tight-cropped SVG to CANVAS_PT with equal space on both sides."""
    text = path.read_text(encoding="utf-8")
    root = re.search(r'width="([\d.]+)pt" height="([\d.]+)pt" viewBox="0 0 ([\d.]+) ([\d.]+)"', text)
    if root is None:
        raise RuntimeError(f"{path}: no pt-sized root viewBox to pad")
    width, height = float(root.group(3)), float(root.group(4))
    if width > CANVAS_PT:
        raise RuntimeError(f"{path}: {width:.1f} pt is wider than the {CANVAS_PT:.0f} pt canvas")
    left = (CANVAS_PT - width) / 2
    padded = f'width="{CANVAS_PT:g}pt" height="{height:g}pt" viewBox="{-left:.3f} 0 {CANVAS_PT:g} {height:g}"'
    path.write_text(text[: root.start()] + padded + text[root.end() :], encoding="utf-8")
