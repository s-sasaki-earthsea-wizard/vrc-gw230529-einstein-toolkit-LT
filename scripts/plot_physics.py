"""Draw the two physics figures that exist only in this talk.

Both read the TSVs under ``docs/data`` (see ``scripts/extract_run_data.py``)
and follow the look of the figures rendered by the infrastructure repository
(gw230529-einstein-toolkit-aws-tf, ``postprocessing/common.py``): the same
palette, fonts and merger line, so the deck reads as one set.

Units follow what this talk's audience reads: milliseconds for time, solar
masses for mass.

Example:
    python3 scripts/plot_physics.py
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Okabe-Ito, in the order the infrastructure repository assigns them.
BLUE = "#0072B2"
VERMILLION = "#D55E00"
GREEN = "#009E73"
INK_MUTED = "0.35"

# IAU 2015 nominal GM_sun over c^3, in milliseconds.
M_SUN_MS = 1.32712440018e20 / 2.99792458e8**3 * 1e3

# Coordinate merger time in M_sun: the Psi4 peak at r = 500 arrives at
# t = 1213, minus the extraction radius. Same value as the other figures.
MERGER_TIME = 713.0


def apply_style():
    """Set talk-oriented matplotlib defaults: big fonts, recessive grid."""
    matplotlib.rcParams.update(
        {
            "font.size": 13,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "grid.linestyle": ":",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )


def merger_line(ax, label=True):
    """Mark the merger time on an axis.

    Args:
        ax: The axis to draw on.
        label: Whether to write "merger" beside the line.
    """
    x = MERGER_TIME * M_SUN_MS
    ax.axvline(x, color="0.5", linewidth=1, linestyle="--")
    if label:
        ax.annotate(
            "merger",
            xy=(x, 1.0),
            xycoords=("data", "axes fraction"),
            xytext=(4, -12),
            textcoords="offset points",
            fontsize=11,
            color=INK_MUTED,
        )


def end_label(ax, x, y, text, dy=0):
    """Write a value beside a curve's end point, in ink rather than in colour.

    Args:
        ax: The axis to draw on.
        x: Data x of the point being labelled.
        y: Data y of the point being labelled.
        text: The label.
        dy: Vertical offset in points.
    """
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(6, dy),
        textcoords="offset points",
        va="center",
        fontsize=12,
        color="0.15",
        annotation_clip=False,
    )


def plot_bh_mass_spin(data, out):
    """Draw the black hole's mass and dimensionless spin as two stacked panels.

    Two panels rather than one with two y axes: the quantities share only the
    time axis, and a dual axis invites reading the crossing as meaningful.

    Args:
        data: Directory holding ``remnant_bh.tsv``.
        out: Directory the PNG is written to.
    """
    t, mass, _, chi, _ = np.loadtxt(data / "remnant_bh.tsv", unpack=True)
    t = t * M_SUN_MS

    fig, (ax_m, ax_s) = plt.subplots(2, 1, figsize=(7.0, 5.0), sharex=True)

    ax_m.plot(t, mass, color=BLUE, linewidth=2.0)
    ax_m.set_ylabel(r"$M_\mathrm{BH}\ [M_\odot]$")
    ax_m.set_ylim(3.4, 4.9)
    merger_line(ax_m)
    end_label(ax_m, t[0], mass[0], f"{mass[0]:.2f}", dy=12)
    end_label(ax_m, t[-1], mass[-1], f"{mass[-1]:.2f}")

    ax_s.plot(t, chi, color=VERMILLION, linewidth=2.0)
    ax_s.set_ylabel(r"spin $\chi = J/M^2$")
    ax_s.set_xlabel(r"$t\ [\mathrm{ms}]$")
    ax_s.set_ylim(-0.03, 0.7)
    merger_line(ax_s, label=False)
    end_label(ax_s, t[0], chi[0], "0", dy=12)
    end_label(ax_s, t[-1], chi[-1], f"{chi[-1]:.2f}")

    fig.align_ylabels()
    fig.tight_layout()
    path = out / "bh_mass_spin.png"
    fig.savefig(path)
    print(f"wrote {path}")


def plot_matter_outside(data, out):
    """Draw the fraction of the star's rest mass still on the grid.

    The whole-grid rest mass includes the numerical atmosphere: a floor of
    1e-10 over a 2.4e9 M_sun^3 domain weighs 0.25 M_sun, a sixth of the star.
    It is measured at t = 0 as the whole-grid integral minus the star's own
    rest mass, and subtracted as a constant. What is left is matter on the
    grid, which bounds the matter outside the horizon from above.

    Args:
        data: Directory holding ``rest_mass.tsv``.
        out: Directory the PNG is written to.
    """
    t, _, m_star, m_grid = np.loadtxt(data / "rest_mass.tsv", unpack=True)
    t = t * M_SUN_MS
    atmosphere = m_grid[0] - m_star[0]
    fraction = (m_grid - atmosphere) / m_star[0] * 100.0

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(t, fraction, color=GREEN, linewidth=2.0)
    ax.set_xlabel(r"$t\ [\mathrm{ms}]$")
    ax.set_ylabel("star's rest mass on the grid [%]")
    ax.set_ylim(0, 105)
    merger_line(ax)
    remaining = (m_grid[-1] - atmosphere)
    end_label(ax, t[-1], fraction[-1], f"{fraction[-1]:.0f} %", dy=10)
    ax.annotate(
        f"≈ {remaining:.2f} $M_\\odot$",
        xy=(t[-1], fraction[-1]),
        xytext=(6, 26),
        textcoords="offset points",
        va="center",
        fontsize=11,
        color=INK_MUTED,
        annotation_clip=False,
    )

    fig.tight_layout()
    path = out / "matter_outside.png"
    fig.savefig(path)
    print(f"wrote {path}")
    print(
        f"atmosphere {atmosphere:.4f} Msun, star {m_star[0]:.4f} Msun, "
        f"left at t = {t[-1]:.2f} ms: {remaining:.4f} Msun = {fraction[-1]:.2f} %"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path, default=Path("docs/data"))
    ap.add_argument("--out", type=Path, default=Path("slides-jp/assets/images"))
    args = ap.parse_args()

    apply_style()
    plot_bh_mass_spin(args.data, args.out)
    plot_matter_outside(args.data, args.out)


if __name__ == "__main__":
    main()
