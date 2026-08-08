"""Reference data and dimensional mapping for the Comte-Bellot--Corrsin HIT DNS.

All dimensional quantities use centimetres and seconds so that spectra can be
compared directly with Tables 2--4 of Comte-Bellot & Corrsin (1971).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"

M_CM = 5.08
U0_CM_S = 1000.0
GRID_REYNOLDS = 34000.0
NU_CM2_S = U0_CM_S * M_CM / GRID_REYNOLDS
INITIAL_STATION = 42.0
OUTPUT_STATIONS = (42.0, 98.0, 171.0)


@dataclass(frozen=True)
class SpectrumTable:
    """A common wavenumber column and station-labelled spectrum columns."""

    k: np.ndarray
    by_station: dict[float, np.ndarray]


def station_to_elapsed_seconds(station: float) -> float:
    """Return DNS elapsed time, with station 42 mapped to zero."""

    return (float(station) - INITIAL_STATION) * M_CM / U0_CM_S


def _load_named_csv(path: Path) -> np.ndarray:
    return np.genfromtxt(path, delimiter=",", names=True, dtype=float)


def load_table2_e11() -> SpectrumTable:
    """Load the one-dimensional spectrum in Table 2(a)."""

    values = _load_named_csv(DATA_DIR / "comte_bellot_table2_e11.csv")
    return SpectrumTable(
        k=np.asarray(values["k_cm1"]),
        by_station={
            42.0: np.asarray(values["E11_station42_cm3_s2"]),
            98.0: np.asarray(values["E11_station98_cm3_s2"]),
            171.0: np.asarray(values["E11_station171_cm3_s2"]),
        },
    )


def load_table3_e() -> SpectrumTable:
    """Load the isotropically reconstructed three-dimensional spectrum."""

    values = _load_named_csv(DATA_DIR / "comte_bellot_table3_e.csv")
    return SpectrumTable(
        k=np.asarray(values["k_cm1"]),
        by_station={
            42.0: np.asarray(values["E_station42_cm3_s2"]),
            98.0: np.asarray(values["E_station98_cm3_s2"]),
            171.0: np.asarray(values["E_station171_cm3_s2"]),
        },
    )


def load_table4_bulk() -> np.ndarray:
    """Load bulk turbulence properties for the 5.08 cm grid."""

    return _load_named_csv(DATA_DIR / "comte_bellot_table4_bulk.csv")


def finite_station_values(table: SpectrumTable, station: float) -> tuple[np.ndarray, np.ndarray]:
    """Return paired finite wavenumber and spectrum values for one station."""

    spectrum = table.by_station[float(station)]
    valid = np.isfinite(table.k) & np.isfinite(spectrum)
    return table.k[valid], spectrum[valid]
