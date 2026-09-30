"""Extract the small time series the slides quote from a synced run directory.

The production run's output is about 10 GB and lives outside this repository
(``make fetch-results`` in gw230529-einstein-toolkit-aws-tf). The slides only
need three short time series, so this script copies those into ``docs/data``
as TSV. ``scripts/plot_physics.py`` then draws from the TSVs alone, which
keeps the figures reproducible after the run directory is gone.

Example:
    python3 scripts/extract_run_data.py /path/to/results/<run_name>/run
"""

import argparse
import re
from pathlib import Path

import numpy as np

# QuasiLocalMeasures surface 1 follows the black hole's apparent horizon from
# t = 0 through the merger (SphericalSurface 1 = AHFinderDirect horizon 1).
QLM_SURFACE = 1


def dedup_sorted(rows, time_col):
    """Return rows sorted by time with duplicated times removed.

    A run resumed from a checkpoint rewinds and re-emits the iterations it had
    already written, so every ASCII output carries repeated rows.

    Args:
        rows: 2-D array of samples.
        time_col: Index of the column holding simulation time.

    Returns:
        The rows with unique, increasing time.
    """
    _, idx = np.unique(rows[:, time_col], return_index=True)
    return rows[idx]


def qlm_columns(path):
    """Map QuasiLocalMeasures variable names to zero-based column indices.

    Args:
        path: The ``quasilocalmeasures-qlm_scalars..asc`` file.

    Returns:
        A dict from names such as ``qlm_mass[1]`` to column indices.
    """
    cols = {}
    with open(path) as f:
        for line in f:
            if not line.startswith("#"):
                break
            for m in re.finditer(r"(\d+):(\S+)", line):
                cols[m.group(2)] = int(m.group(1)) - 1
    return cols


def extract_remnant(run, out):
    """Write the black hole's mass, angular momentum and spin over time."""
    path = run / "data" / "quasilocalmeasures-qlm_scalars..asc"
    cols = qlm_columns(path)
    rows = dedup_sorted(np.loadtxt(path, ndmin=2), cols["time"])
    t = rows[:, cols["time"]]
    mass = rows[:, cols[f"qlm_mass[{QLM_SURFACE}]"]]
    ang = rows[:, cols[f"qlm_spin[{QLM_SURFACE}]"]]
    m_irr = rows[:, cols[f"qlm_irreducible_mass[{QLM_SURFACE}]"]]
    table = np.column_stack([t, mass, ang, ang / mass**2, m_irr])
    header = (
        "Black hole quasi-local measures, QuasiLocalMeasures surface "
        f"{QLM_SURFACE}.\n"
        "Geometric units, G = c = M_sun = 1.\n"
        "t[Msun]\tM[Msun]\tJ[Msun^2]\tchi=J/M^2\tM_irr[Msun]"
    )
    np.savetxt(out / "remnant_bh.tsv", table, fmt="%.6f", delimiter="\t", header=header)


def extract_rest_mass(run, out):
    """Write the rest mass on the grid and inside the star's tracking sphere."""
    path = run / "volume_integration" / "volume_integrals-GRMHD.asc"
    rows = dedup_sorted(np.loadtxt(path, ndmin=2), 0)
    # Column 2 is the grid volume, column 6 the rest mass inside the sphere
    # that tracks the neutron star, column 8 the rest mass on the whole grid.
    table = rows[:, [0, 1, 5, 7]]
    header = (
        "Rest mass integrals from VolumeIntegrals_GRMHD.\n"
        "The whole-grid integral includes the numerical atmosphere.\n"
        "Geometric units, G = c = M_sun = 1.\n"
        "t[Msun]\tgrid_volume[Msun^3]\tM0_star_sphere[Msun]\tM0_grid[Msun]"
    )
    np.savetxt(out / "rest_mass.tsv", table, fmt="%.9e", delimiter="\t", header=header)


def extract_rho_max(run, out):
    """Write the maximum rest-mass density on the grid over time."""
    path = run / "data" / "hydrobase-rho.maximum.asc"
    rows = dedup_sorted(np.loadtxt(path, ndmin=2), 1)
    header = (
        "Maximum rest-mass density on the grid.\n"
        "Geometric units, G = c = M_sun = 1.\n"
        "t[Msun]\trho_max[Msun^-2]"
    )
    np.savetxt(out / "rho_max.tsv", rows[:, [1, 2]], fmt="%.9e", delimiter="\t", header=header)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run", type=Path, help="synced run directory (contains data/)")
    ap.add_argument("--out", type=Path, default=Path("docs/data"), help="output directory")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    extract_remnant(args.run, args.out)
    extract_rest_mass(args.run, args.out)
    extract_rho_max(args.run, args.out)
    print(f"wrote remnant_bh.tsv, rest_mass.tsv, rho_max.tsv to {args.out}")


if __name__ == "__main__":
    main()
