#!/usr/bin/env python
"""Generate a Markdown audit report for selected-mode resolvent workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import h5py
import numpy as np


DEFAULT_REPORT_NAME = "MKM_channel_resolvent_selected_modes_report.md"
CONSTRAINT_WARN = 1e-8
CONSTRAINT_FAIL = 1e-6
ENERGY_WARN = 1e-8
ENERGY_FAIL = 1e-6
PARSEVAL_WARN_RECTANGULAR = 1e-6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Selected-mode workflow manifest JSON.")
    parser.add_argument(
        "--output",
        help=f"Markdown report path. Default: manifest directory/{DEFAULT_REPORT_NAME}.",
    )
    parser.add_argument("--include-hdf5-schema", action="store_true")
    parser.add_argument("--max-modes", type=int, help="Limit printed mode sections.")
    parser.add_argument("--max-omega", type=int, help="Limit printed frequency rows per mode.")
    return parser.parse_args()


def _decode(value: Any) -> Any:
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, np.bytes_):
        return value.astype(str).item()
    if isinstance(value, np.generic):
        return value.item()
    return value


def path_from_manifest(value: str | None, manifest_dir: Path) -> Path | None:
    if not value:
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = manifest_dir / path
    return path


def file_size_label(path: Path | None) -> str:
    if path is None:
        return "n/a"
    if not path.exists():
        return "missing"
    size = path.stat().st_size
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    value = float(size)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{size} B"
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{size} B"


def max_abs_or_nan(values: np.ndarray) -> float:
    values = np.asarray(values)
    if values.size == 0:
        return float("nan")
    return float(np.nanmax(np.abs(values)))


def status_for(value: float, warn: float, fail: float) -> str:
    if not np.isfinite(value):
        return "WARN"
    if value > fail:
        return "FAIL"
    if value > warn:
        return "WARN"
    return "PASS"


def format_float(value: float) -> str:
    if value is None:
        return "n/a"
    if not np.isfinite(value):
        return "nan"
    return f"{value:.6e}"


def format_compact(value: float) -> str:
    if value is None:
        return "n/a"
    if not np.isfinite(value):
        return "nan"
    return f"{value:.6g}"


def hdf5_schema(path: Path) -> list[str]:
    lines: list[str] = []
    if not path.exists():
        return [f"{path}: missing"]
    with h5py.File(path, "r") as f:
        def visitor(name: str, obj: h5py.Dataset | h5py.Group) -> None:
            if isinstance(obj, h5py.Dataset):
                lines.append(f"{name}: shape={obj.shape} dtype={obj.dtype}")

        f.visititems(visitor)
    return sorted(lines)


def read_scalar_or_none(f: h5py.File, path: str) -> Any:
    if path not in f:
        return None
    return _decode(f[path][()])


def read_array_or_empty(f: h5py.File, path: str, dtype: Any = float) -> np.ndarray:
    if path not in f:
        return np.array([], dtype=dtype)
    return np.asarray(f[path][:], dtype=dtype)


def collect_csd_summary(csd_path: Path | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "path": str(csd_path) if csd_path is not None else None,
        "exists": bool(csd_path is not None and csd_path.exists()),
        "size": file_size_label(csd_path),
    }
    if csd_path is None or not csd_path.exists():
        return summary

    with h5py.File(csd_path, "r") as f:
        parseval = read_array_or_empty(f, "diagnostics/parseval_relative_error")
        starts = read_array_or_empty(f, "metadata/segment_start_indices", dtype=np.int64)
        omega = read_array_or_empty(f, "frequencies/omega")
        mode_index = read_array_or_empty(f, "mode/index", dtype=np.int32)
        summary.update({
            "source": _decode(f.attrs.get("source", read_scalar_or_none(f, "metadata/source"))),
            "sample_dt": read_scalar_or_none(f, "metadata/sample_dt"),
            "segment_length": read_scalar_or_none(f, "metadata/segment_length"),
            "overlap": read_scalar_or_none(f, "metadata/overlap"),
            "window": read_scalar_or_none(f, "metadata/window"),
            "n_segments": int(starts.size) if starts.size else None,
            "n_omega": int(omega.size),
            "mode_count": int(mode_index.shape[0]) if mode_index.ndim >= 2 else int(mode_index.size > 0),
            "parseval_relative_error": parseval,
            "max_parseval_relative_error": max_abs_or_nan(parseval),
        })
    return summary


def collect_resolvent_summary(path: Path | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "path": str(path) if path is not None else None,
        "exists": bool(path is not None and path.exists()),
        "size": file_size_label(path),
    }
    if path is None or not path.exists():
        return summary

    with h5py.File(path, "r") as f:
        singular_values = read_array_or_empty(f, "resolvent/singular_values")
        omega = read_array_or_empty(f, "frequencies/omega")
        critical_count = read_array_or_empty(f, "critical_layers/count", dtype=np.int32)
        response_constraint = read_array_or_empty(f, "diagnostics/constraint_residual_response")
        forcing_constraint = read_array_or_empty(f, "diagnostics/constraint_residual_forcing")
        response_energy = read_array_or_empty(f, "diagnostics/response_energy_norm_error")
        forcing_energy = read_array_or_empty(f, "diagnostics/forcing_energy_norm_error")
        summary.update({
            "mode_index": read_array_or_empty(f, "mode/index", dtype=np.int32),
            "kappa": read_scalar_or_none(f, "mode/kappa"),
            "lambda": read_scalar_or_none(f, "mode/lambda"),
            "omega": omega,
            "singular_values": singular_values,
            "critical_count": critical_count,
            "max_response_constraint_residual": max_abs_or_nan(response_constraint),
            "max_forcing_constraint_residual": max_abs_or_nan(forcing_constraint),
            "max_response_energy_norm_error": max_abs_or_nan(response_energy),
            "max_forcing_energy_norm_error": max_abs_or_nan(forcing_energy),
        })
    return summary


def collect_projection_summary(path: Path | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "path": str(path) if path is not None else None,
        "exists": bool(path is not None and path.exists()),
        "size": file_size_label(path),
    }
    if path is None or not path.exists():
        return summary

    with h5py.File(path, "r") as f:
        energy_fraction = read_array_or_empty(f, "projection/energy_fraction")
        cumulative = read_array_or_empty(f, "projection/cumulative_energy_fraction")
        fro = read_array_or_empty(f, "projection/weighted_frobenius_relative_error")
        freq_error = read_array_or_empty(f, "diagnostics/frequency_match_error")
        summary.update({
            "energy_fraction": energy_fraction,
            "cumulative_energy_fraction": cumulative,
            "weighted_frobenius_relative_error": fro,
            "frequency_match_error": freq_error,
            "max_frequency_match_error": max_abs_or_nan(freq_error),
            "negative_fraction_count": int(read_scalar_or_none(f, "diagnostics/negative_fraction_count") or 0),
            "zero_or_negative_total_energy_count": int(
                read_scalar_or_none(f, "diagnostics/zero_or_negative_total_energy_count") or 0
            ),
        })
    return summary


def figure_summaries(entry: dict[str, Any], manifest_dir: Path) -> list[dict[str, Any]]:
    figures = []
    for value in entry.get("figures", []) or []:
        path = path_from_manifest(value, manifest_dir)
        figures.append({
            "path": str(path),
            "exists": bool(path is not None and path.exists()),
            "size": file_size_label(path),
        })
    return figures


def diagnostics_threshold_table(mode_summaries: list[dict[str, Any]], csd_summary: dict[str, Any], frequency_tolerance: float | None) -> list[tuple[str, float, str, str]]:
    rows: list[tuple[str, float, str, str]] = []
    for mode in mode_summaries:
        label = f"mode {tuple(mode['mode_index'])}"
        res = mode["resolvent"]
        proj = mode["projection"]
        for key, warn, fail, desc in (
            ("max_response_constraint_residual", CONSTRAINT_WARN, CONSTRAINT_FAIL, "response constraint residual"),
            ("max_forcing_constraint_residual", CONSTRAINT_WARN, CONSTRAINT_FAIL, "forcing constraint residual"),
            ("max_response_energy_norm_error", ENERGY_WARN, ENERGY_FAIL, "response energy norm error"),
            ("max_forcing_energy_norm_error", ENERGY_WARN, ENERGY_FAIL, "forcing energy norm error"),
        ):
            value = float(res.get(key, np.nan))
            rows.append((f"{label}: {desc}", value, status_for(value, warn, fail), f"warn>{warn:g}, fail>{fail:g}"))
        if proj.get("exists"):
            value = float(proj.get("max_frequency_match_error", np.nan))
            warn = frequency_tolerance if frequency_tolerance is not None else 1e-10
            rows.append((f"{label}: projection frequency match error", value, status_for(value, warn, max(warn * 100.0, 1e-6)), f"warn>{warn:g}"))

    if csd_summary.get("exists"):
        parseval = float(csd_summary.get("max_parseval_relative_error", np.nan))
        window = str(csd_summary.get("window", "unknown"))
        if window == "none":
            rows.append((
                "shared CSD: Parseval relative error",
                parseval,
                status_for(parseval, PARSEVAL_WARN_RECTANGULAR, max(PARSEVAL_WARN_RECTANGULAR * 100.0, 1e-4)),
                "rectangular/full-record check",
            ))
        else:
            rows.append(("shared CSD: Parseval relative error", parseval, "INFO", f"diagnostic only for window={window}"))
    return rows


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def collect_report_data(manifest_path: Path, max_modes: int | None) -> dict[str, Any]:
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_dir = manifest_path.parent
    csd_path = None
    if manifest.get("csd"):
        csd_path = path_from_manifest(manifest["csd"].get("path"), manifest_dir)
    csd_summary = collect_csd_summary(csd_path)

    entries = manifest.get("modes", [])
    if max_modes is not None:
        entries = entries[:max_modes]
    mode_summaries: list[dict[str, Any]] = []
    for entry in entries:
        resolvent_path = path_from_manifest(entry.get("resolvent_h5"), manifest_dir)
        projection_path = path_from_manifest(entry.get("projection_h5"), manifest_dir)
        mode_summaries.append({
            "manifest_entry": entry,
            "mode_index": entry.get("mode_index", []),
            "resolvent": collect_resolvent_summary(resolvent_path),
            "projection": collect_projection_summary(projection_path),
            "figures": figure_summaries(entry, manifest_dir),
        })

    return {
        "manifest": manifest,
        "manifest_path": manifest_path,
        "csd": csd_summary,
        "modes": mode_summaries,
        "truncated_mode_count": max(0, len(manifest.get("modes", [])) - len(mode_summaries)),
    }


def render_report(data: dict[str, Any], include_hdf5_schema: bool, max_omega: int | None) -> str:
    manifest = data["manifest"]
    manifest_path = data["manifest_path"]
    csd_summary = data["csd"]
    modes = data["modes"]
    frequency_tolerance = None
    for entry in manifest.get("modes", []):
        projection_summary = entry.get("projection_summary") or {}
        if "max_frequency_match_error" in projection_summary:
            frequency_tolerance = manifest.get("frequency_tolerance")
            break

    lines: list[str] = []
    lines.append("# MKM Channel Resolvent Selected-Mode Report")
    lines.append("")
    lines.append("## Summary")
    lines.extend(markdown_table(
        ["Item", "Value"],
        [
            ["Manifest", str(manifest_path)],
            ["Output directory", str(manifest.get("output_dir", "n/a"))],
            ["Selected modes", str(manifest.get("selected_modes", []))],
            ["Reported modes", str(len(modes))],
            ["Truncated modes", str(data["truncated_mode_count"])],
            ["n_singular", str(manifest.get("n_singular", "n/a"))],
            ["Re_tau", str(manifest.get("re_tau", "n/a"))],
        ],
    ))
    lines.append("")

    lines.append("## Inputs")
    lines.extend(markdown_table(
        ["Input", "Path"],
        [
            ["Target HDF5", str(manifest.get("target_h5", "n/a"))],
            ["Constraint HDF5", str(manifest.get("constraint_file", "n/a"))],
            ["Shared CSD HDF5", str(csd_summary.get("path", "n/a"))],
        ],
    ))
    lines.append("")

    lines.append("## Shared CSD")
    if csd_summary.get("exists"):
        parseval = np.asarray(csd_summary.get("parseval_relative_error", []))
        parseval_values = ", ".join(format_float(float(value)) for value in parseval[:8])
        if parseval.size > 8:
            parseval_values += ", ..."
        lines.extend(markdown_table(
            ["Field", "Value"],
            [
                ["Path", str(csd_summary["path"])],
                ["Size", str(csd_summary["size"])],
                ["Source", str(csd_summary.get("source", "n/a"))],
                ["Mode count", str(csd_summary.get("mode_count", "n/a"))],
                ["n_omega", str(csd_summary.get("n_omega", "n/a"))],
                ["sample_dt", format_compact(csd_summary.get("sample_dt"))],
                ["segment_length", str(csd_summary.get("segment_length", "n/a"))],
                ["n_segments", str(csd_summary.get("n_segments", "n/a"))],
                ["window", str(csd_summary.get("window", "n/a"))],
                ["max Parseval relative error", format_float(csd_summary.get("max_parseval_relative_error", np.nan))],
                ["Parseval relative errors", parseval_values or "n/a"],
            ],
        ))
    else:
        lines.append("Shared CSD file was not present or was not part of this workflow.")
    lines.append("")

    lines.append("## Mode Results")
    for mode in modes:
        entry = mode["manifest_entry"]
        res = mode["resolvent"]
        proj = mode["projection"]
        mode_index = tuple(entry.get("mode_index", mode.get("mode_index", [])))
        lines.append(f"### Mode {mode_index}")
        if not res.get("exists"):
            lines.append(f"Resolvent file missing: `{res.get('path')}`")
            lines.append("")
            continue

        omega = np.asarray(res.get("omega", []), dtype=float)
        singular_values = np.asarray(res.get("singular_values", []), dtype=float)
        critical_count = np.asarray(res.get("critical_count", []), dtype=int)
        energy_fraction = np.asarray(proj.get("energy_fraction", []), dtype=float)
        cumulative = np.asarray(proj.get("cumulative_energy_fraction", []), dtype=float)
        fro = np.asarray(proj.get("weighted_frobenius_relative_error", []), dtype=float)

        lines.extend(markdown_table(
            ["Field", "Value"],
            [
                ["kappa", format_compact(float(res.get("kappa", np.nan)))],
                ["lambda", format_compact(float(res.get("lambda", np.nan)))],
                ["Resolvent HDF5", str(res.get("path"))],
                ["Resolvent size", str(res.get("size"))],
                ["Projection HDF5", str(proj.get("path", "n/a"))],
                ["Projection size", str(proj.get("size", "n/a"))],
                ["Omega selection", str(entry.get("omega_selection", {}).get("kind", "n/a"))],
            ],
        ))
        lines.append("")

        row_count = omega.size if max_omega is None else min(omega.size, max_omega)
        rows: list[list[str]] = []
        for idx in range(row_count):
            sigma1 = singular_values[idx, 0] if singular_values.ndim == 2 and singular_values.shape[1] else np.nan
            sigma2 = singular_values[idx, 1] if singular_values.ndim == 2 and singular_values.shape[1] > 1 else np.nan
            leading_fraction = (
                energy_fraction[idx, 0]
                if energy_fraction.ndim == 2 and idx < energy_fraction.shape[0] and energy_fraction.shape[1]
                else np.nan
            )
            final_fraction = (
                cumulative[idx, -1]
                if cumulative.ndim == 2 and idx < cumulative.shape[0] and cumulative.shape[1]
                else np.nan
            )
            rank1_fro = (
                fro[idx, 0]
                if fro.ndim == 2 and idx < fro.shape[0] and fro.shape[1]
                else np.nan
            )
            roots = critical_count[idx] if idx < critical_count.size else 0
            rows.append([
                str(idx),
                format_compact(omega[idx]),
                format_compact(sigma1),
                format_compact(sigma2),
                str(int(roots)),
                format_compact(float(leading_fraction)),
                format_compact(float(final_fraction)),
                format_compact(float(rank1_fro)),
            ])
        lines.extend(markdown_table(
            ["idx", "omega", "sigma1", "sigma2", "critical roots", "lead fraction", "cum fraction", "rank1 Fro err"],
            rows,
        ))
        if row_count < omega.size:
            lines.append(f"Only first {row_count} of {omega.size} frequencies shown.")
        lines.append("")

        lines.extend(markdown_table(
            ["Diagnostic", "Value", "Status"],
            [
                [
                    "max response constraint residual",
                    format_float(res.get("max_response_constraint_residual", np.nan)),
                    status_for(float(res.get("max_response_constraint_residual", np.nan)), CONSTRAINT_WARN, CONSTRAINT_FAIL),
                ],
                [
                    "max forcing constraint residual",
                    format_float(res.get("max_forcing_constraint_residual", np.nan)),
                    status_for(float(res.get("max_forcing_constraint_residual", np.nan)), CONSTRAINT_WARN, CONSTRAINT_FAIL),
                ],
                [
                    "max response energy norm error",
                    format_float(res.get("max_response_energy_norm_error", np.nan)),
                    status_for(float(res.get("max_response_energy_norm_error", np.nan)), ENERGY_WARN, ENERGY_FAIL),
                ],
                [
                    "max forcing energy norm error",
                    format_float(res.get("max_forcing_energy_norm_error", np.nan)),
                    status_for(float(res.get("max_forcing_energy_norm_error", np.nan)), ENERGY_WARN, ENERGY_FAIL),
                ],
                [
                    "max projection frequency match error",
                    format_float(proj.get("max_frequency_match_error", np.nan)),
                    "PASS" if proj.get("exists") else "n/a",
                ],
            ],
        ))
        lines.append("")

    lines.append("## Figures")
    figure_rows: list[list[str]] = []
    for mode in modes:
        mode_index = tuple(mode["manifest_entry"].get("mode_index", []))
        for fig in mode["figures"]:
            figure_rows.append([
                str(mode_index),
                str(fig["path"]),
                str(fig["size"]),
                "yes" if fig["exists"] else "missing",
            ])
    if figure_rows:
        lines.extend(markdown_table(["Mode", "Figure", "Size", "Exists"], figure_rows))
    else:
        lines.append("No figure paths were recorded in the manifest.")
    lines.append("")

    lines.append("## Diagnostics and Thresholds")
    diag_rows = diagnostics_threshold_table(modes, csd_summary, frequency_tolerance)
    lines.extend(markdown_table(
        ["Check", "Value", "Status", "Threshold"],
        [[label, format_float(value), status, threshold] for label, value, status, threshold in diag_rows],
    ))
    lines.append("")

    lines.append("## Caveats")
    lines.append("- Projection fractions quantify DNS CSD alignment with the stored response subspace; they do not by themselves model forcing statistics or DNS amplitudes.")
    lines.append("- Resolvent/projection comparison requires frequency bins to match the CSD grid within tolerance.")
    lines.append("- Hann-window or overlapping CSD Parseval values are reported as estimator diagnostics, not strict pass/fail conservation tests.")
    lines.append("- This selected-mode report is not an exhaustive mode sweep and should not be used for broad scaling claims without additional runs.")
    lines.append("")

    lines.append("## Reproduction Command/Config")
    lines.append("```json")
    config = {
        "target_h5": manifest.get("target_h5"),
        "constraint_file": manifest.get("constraint_file"),
        "output_dir": manifest.get("output_dir"),
        "selected_modes": manifest.get("selected_modes"),
        "n_singular": manifest.get("n_singular"),
        "re_tau": manifest.get("re_tau"),
        "csd": manifest.get("csd"),
        "omega_selection_by_mode": [
            {
                "mode_index": entry.get("mode_index"),
                "omega": entry.get("omega"),
                "omega_selection": entry.get("omega_selection"),
            }
            for entry in manifest.get("modes", [])
        ],
    }
    lines.append(json.dumps(config, indent=2))
    lines.append("```")
    lines.append("")

    if include_hdf5_schema:
        lines.append("## HDF5 Schema")
        schema_paths: list[Path] = []
        if csd_summary.get("path"):
            schema_paths.append(Path(csd_summary["path"]))
        for mode in modes:
            for key in ("resolvent", "projection"):
                path = mode[key].get("path")
                if path:
                    schema_paths.append(Path(path))
        for path in schema_paths:
            lines.append(f"### {path}")
            lines.append("```text")
            lines.extend(hdf5_schema(path))
            lines.append("```")
            lines.append("")

    return "\n".join(lines)


def write_report(
    manifest: str | Path,
    output: str | Path | None = None,
    *,
    include_hdf5_schema: bool = False,
    max_modes: int | None = None,
    max_omega: int | None = None,
) -> dict[str, Any]:
    manifest_path = Path(manifest).expanduser().resolve()
    output_path = (
        Path(output).expanduser().resolve()
        if output is not None
        else manifest_path.with_name(DEFAULT_REPORT_NAME)
    )
    data = collect_report_data(manifest_path, max_modes)
    report = render_report(data, include_hdf5_schema, max_omega)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return {
        "output": str(output_path),
        "mode_count": len(data["modes"]),
        "csd_present": bool(data["csd"].get("exists")),
        "line_count": len(report.splitlines()),
    }


def main() -> int:
    args = parse_args()
    result = write_report(
        args.manifest,
        args.output,
        include_hdf5_schema=args.include_hdf5_schema,
        max_modes=args.max_modes,
        max_omega=args.max_omega,
    )
    print(f"wrote_report={result['output']}")
    print(f"mode_count={result['mode_count']}")
    print(f"csd_present={result['csd_present']}")
    print(f"line_count={result['line_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
