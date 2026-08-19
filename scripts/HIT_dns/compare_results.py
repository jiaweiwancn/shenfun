#!/usr/bin/env python3
"""Compare lightweight HIT DNS station products with Tables 2--4."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from reference_data import (
    finite_station_values,
    load_table2_e11,
    load_table3_e,
    load_table4_bulk,
)


STATIONS = (42.0, 98.0, 171.0)
BULK_MAPPINGS = (
    ("u_rms_cm_s", "isotropic_u_rms_cm_s", "u1_rms_cm_s"),
    ("epsilon_cm2_s3", "dissipation_cm2_s^-3", "epsilon_cm2_s3"),
    ("eta_cm", "kolmogorov_length_cm", "eta_cm"),
    ("lambda_cm", "taylor_microscale_cm", "lambda_cm"),
    ("R_lambda", "reynolds_lambda", "R_lambda"),
)


def station_slug(station: float) -> str:
    text = f"{float(station):09.4f}".rstrip("0").rstrip(".")
    return text.replace(".", "p")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dns-light-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--reduced-light-dir", type=Path)
    return parser.parse_args()


def load_dns_station(directory: Path, station: float) -> dict[str, Any]:
    slug = station_slug(station)
    e = np.genfromtxt(directory / f"station_{slug}_E.csv", delimiter=",", names=True)
    e11 = np.genfromtxt(directory / f"station_{slug}_E11.csv", delimiter=",", names=True)
    with (directory / f"station_{slug}_summary.json").open() as stream:
        summary = json.load(stream)
    return {"E": e, "E11": e11, "summary": summary}


def positive_log_interpolate(
    source_k: np.ndarray, source_values: np.ndarray, target_k: np.ndarray
) -> np.ndarray:
    """Log-log interpolate positive data, returning NaN outside its support."""

    source_k = np.asarray(source_k, dtype=float)
    source_values = np.asarray(source_values, dtype=float)
    target_k = np.asarray(target_k, dtype=float)
    valid = np.isfinite(source_k) & np.isfinite(source_values) & (source_k > 0) & (source_values > 0)
    x = source_k[valid]
    y = source_values[valid]
    order = np.argsort(x)
    result = np.full(target_k.shape, np.nan)
    inside = (target_k >= x[order][0]) & (target_k <= x[order][-1])
    result[inside] = np.exp(
        np.interp(np.log(target_k[inside]), np.log(x[order]), np.log(y[order]))
    )
    return result


def comparison_metrics(dns: np.ndarray, experiment: np.ndarray) -> dict[str, float]:
    valid = np.isfinite(dns) & np.isfinite(experiment) & (dns > 0) & (experiment > 0)
    ratio = dns[valid] / experiment[valid]
    return {
        "point_count": int(np.count_nonzero(valid)),
        "relative_l2": float(np.linalg.norm(dns[valid] - experiment[valid]) / np.linalg.norm(experiment[valid])),
        "log10_rmse": float(np.sqrt(np.mean(np.log10(ratio) ** 2))),
        "median_ratio_dns_over_experiment": float(np.median(ratio)),
        "maximum_factor_error": float(np.exp(np.max(np.abs(np.log(ratio))))),
    }


def write_point_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    table_e = load_table3_e()
    table_e11 = load_table2_e11()
    bulk = load_table4_bulk()
    all_metrics: dict[str, Any] = {"stations": {}}
    point_rows: list[dict[str, Any]] = []
    bulk_rows: list[dict[str, Any]] = []

    figure_e, axes_e = plt.subplots(1, 3, figsize=(13.2, 4.2), sharey=True)
    figure_e11, axes_e11 = plt.subplots(1, 3, figsize=(13.2, 4.2), sharey=True)
    for column, station in enumerate(STATIONS):
        dns = load_dns_station(args.dns_light_dir, station)
        station_metrics: dict[str, Any] = {}
        for name, table, dns_key, k_field, value_field, axis in (
            ("E", table_e, "E", "k_cm1", "E_cm3_s2", axes_e[column]),
            ("E11", table_e11, "E11", "k1_cm1", "E11_cm3_s2", axes_e11[column]),
        ):
            experiment_k, experiment_values = finite_station_values(table, station)
            dns_table = dns[dns_key]
            dns_k = np.asarray(dns_table[k_field])
            dns_values = np.asarray(dns_table[value_field])
            interpolated = positive_log_interpolate(dns_k, dns_values, experiment_k)
            resolved = experiment_k >= 0.2
            interpolated[~resolved] = np.nan
            station_metrics[name] = comparison_metrics(interpolated, experiment_values)
            for k, observed, simulated, is_resolved in zip(
                experiment_k, experiment_values, interpolated, resolved
            ):
                point_rows.append(
                    {
                        "station_tU0_over_M": station,
                        "spectrum": name,
                        "k_cm^-1": k,
                        "experimental_cm3_s^-2": observed,
                        "dns_interpolated_cm3_s^-2": simulated,
                        "resolved_by_box": bool(is_resolved),
                    }
                )
            positive = (dns_k > 0) & (dns_values > 0)
            axis.loglog(dns_k[positive], dns_values[positive], label="DNS", lw=1.5)
            axis.loglog(experiment_k, experiment_values, "o", ms=4, label="experiment")
            axis.axvspan(0.0, 0.2, color="0.9", label="box-unresolved" if column == 0 else None)
            axis.set_title(f"$tU_0/M={station:g}$")
            axis.set_xlabel("$k$ [cm$^{-1}$]" if name == "E" else "$k_1$ [cm$^{-1}$]")
            axis.grid(True, which="both", alpha=0.25)

        stats = dns["summary"]["statistics"]
        experimental_bulk = bulk[np.isclose(bulk["station_tU0_over_M"], station)][0]
        for quantity, dns_name, experiment_name in BULK_MAPPINGS:
            observed = float(experimental_bulk[experiment_name])
            simulated = float(stats[dns_name])
            bulk_rows.append(
                {
                    "station_tU0_over_M": station,
                    "quantity": quantity,
                    "experimental": observed,
                    "dns": simulated,
                    "relative_difference": (simulated - observed) / observed,
                }
            )
        station_metrics["cfl"] = float(stats["cfl"])
        station_metrics["kmax_eta"] = float(stats["kmax_eta"])
        all_metrics["stations"][str(int(station))] = station_metrics

    axes_e[0].set_ylabel("$E(k)$ [cm$^3$ s$^{-2}$]")
    axes_e11[0].set_ylabel("$E_{11}^{(1)}(k_1)$ [cm$^3$ s$^{-2}$]")
    axes_e[0].legend(fontsize=8)
    axes_e11[0].legend(fontsize=8)
    figure_e.tight_layout()
    figure_e11.tight_layout()
    for figure, stem in ((figure_e, "E_comparison"), (figure_e11, "E11_comparison")):
        figure.savefig(args.output_dir / f"{stem}.png", dpi=180)
        figure.savefig(args.output_dir / f"{stem}.pdf")
        plt.close(figure)

    if args.reduced_light_dir is not None:
        baseline = load_dns_station(args.dns_light_dir, 98.0)
        reduced = load_dns_station(args.reduced_light_dir, 98.0)
        resolution: dict[str, Any] = {}
        for name, key, k_field, value_field in (
            ("E", "E", "k_cm1", "E_cm3_s2"),
            ("E11", "E11", "k1_cm1", "E11_cm3_s2"),
        ):
            base_k = np.asarray(baseline[key][k_field])
            base_value = np.asarray(baseline[key][value_field])
            reduced_value = positive_log_interpolate(
                np.asarray(reduced[key][k_field]), np.asarray(reduced[key][value_field]), base_k
            )
            common = (base_k >= 0.2) & (base_k <= 20.0)
            base_common = np.where(common, base_value, np.nan)
            reduced_common = np.where(common, reduced_value, np.nan)
            resolution[name] = comparison_metrics(base_common, reduced_common)
        all_metrics["resolution_N384_vs_N256_station98"] = resolution

    write_point_rows(args.output_dir / "spectrum_comparison_points.csv", point_rows)
    write_point_rows(args.output_dir / "bulk_comparison.csv", bulk_rows)
    (args.output_dir / "comparison_metrics.json").write_text(
        json.dumps(all_metrics, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(all_metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"comparison failed: {error}", file=sys.stderr)
        raise
