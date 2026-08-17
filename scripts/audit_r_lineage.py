#!/usr/bin/env python3
"""Audit a project for the data -> output -> result R lineage contract.

Exit codes: 0 = PASS, 2 = FAIL. Writes a JSON report to --report
(default: <project-root>/output/audit/r_data_lineage_audit.json).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


INTERMEDIATE = re.compile(
    r"plot_data|coordinates|heatmap|alpha_values|program_scores|feature_matrix|"
    r"sample_metrics|curves|replicates|nodes|edges|audit|availability|integrity|"
    r"diagnostic|recalculated|bootstrap|residual|clr",
    re.I,
)
DERIVED_IN_DATA = re.compile(
    r"network|node|edge|robust|auc|attack|removal|module|topology|threshold|"
    r"match|gate|clr|residual|normalized|relative_abundance|plot_data|coordinates",
    re.I,
)
WRITE_TO_DATA = re.compile(
    r"(?:write(?:_csv|\.csv|_table)?|saveRDS|fwrite|writeLines).*?"
    r"(?:\bdata_dir\b|\bDATA_DIR\b|[/\\]data[/\\])",
    re.I,
)
REVIEW_ARTIFACT_NAME = re.compile(r"reviewer|peer[_ -]?review|review[_ -]?(report|notes|response)|response[_ -]?to[_ -]?review|审稿|审阅|审稿回复", re.I)
GENERIC_PREPARE_NAME = re.compile(r"^(?:\d+[_-])?(?:prepare|clean)(?:[_-](?:data|final|all))?\.r$", re.I)
# Hardcoded annotation literals in plotting/statistics code (review signals, not hard failures):
#   - a numeric p/FDR/AUC value assigned to a variable, or
#   - a p/AUC/"n =" literal inside an annotation/label call.
HARDCODED_ANNOTATION = re.compile(
    r"\b(?:pvalue|pval|padj|p\.adj|fdr|qvalue|q_val|auc)\s*(?:=|<-)\s*0?\.\d+|"
    r"(?:annotate|geom_text|geom_label|ggtitle|labs|xlab|ylab|paste0)\s*\([^)]*(?:\bp\s*[=<>]\s*0?\.\d+|AUC\s*=\s*0?\.\d+|[nN]\s*=\s*\d+)|"
    r"\blabel\s*(?:=|<-)\s*[\"'][^\"']*(?:\bp\s*[=<>]\s*0?\.\d+|AUC\s*=\s*0?\.\d+|[nN]\s*=\s*\d+)",
    re.I,
)


def load_allowlist(path: Path | None) -> set[str]:
    if path is None:
        return set()
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if not rows or "file" not in rows[0]:
            raise ValueError("CSV allowlist must contain a 'file' column")
        return {row["file"].replace("\\", "/") for row in rows}
    return {line.strip().replace("\\", "/") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--allowlist", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--scripts",
        default="script,scripts",
        help="comma-separated script directory names/relative paths under the project root (default: script,scripts)",
    )
    args = parser.parse_args()

    root = args.project_root.resolve()
    data = root / "data"
    output = root / "output"
    result_tables = root / "result" / "tables"
    report = args.report or output / "audit" / "r_data_lineage_audit.json"
    allowlist = load_allowlist(args.allowlist)
    failures: list[dict[str, str]] = []
    review_signals: list[dict[str, str]] = []

    if not data.is_dir():
        failures.append({"check": "data_directory", "path": str(data), "reason": "missing"})
    else:
        for path in data.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(data).as_posix()
            if allowlist and rel not in allowlist:
                failures.append({"check": "data_allowlist", "path": rel, "reason": "not approved"})
            elif not allowlist and DERIVED_IN_DATA.search(path.name):
                failures.append({"check": "derived_name_in_data", "path": rel, "reason": "review classification"})

    code_files: list[Path] = []
    for token in [t.strip() for t in args.scripts.split(",") if t.strip()]:
        candidate = root / token
        if candidate.exists():
            code_files.extend(candidate.rglob("*.R"))
    for path in code_files:
        if GENERIC_PREPARE_NAME.match(path.name):
            review_signals.append({
                "check": "generic_prepare_script",
                "path": str(path.relative_to(root)),
                "reason": "verify that this is a substantial shared module stage, not a compulsory project-wide prepared-data layer",
            })
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if WRITE_TO_DATA.search(line):
                failures.append({"check": "write_to_data", "path": f"{path.relative_to(root)}:{number}", "reason": line.strip()})
            if HARDCODED_ANNOTATION.search(line):
                review_signals.append({
                    "check": "hardcoded_annotation",
                    "path": f"{path.relative_to(root)}:{number}",
                    "reason": line.strip(),
                })

    if result_tables.exists():
        for path in result_tables.iterdir():
            if path.is_file() and INTERMEDIATE.search(path.name):
                failures.append({"check": "intermediate_in_result_tables", "path": path.name, "reason": "move to output"})

    result_dir = root / "result"
    if result_dir.exists():
        for path in result_dir.rglob("*"):
            if path.is_file() and REVIEW_ARTIFACT_NAME.search(path.name):
                failures.append({"check": "review_artifact_in_result", "path": str(path.relative_to(root)), "reason": "move to review"})

    payload = {
        "project_root": str(root),
        "contract": "data -> independent analysis modules -> output/module -> result/tables and result/figs",
        "status": "PASS" if not failures else "FAIL",
        "n_failures": len(failures),
        "failures": failures,
        "n_review_signals": len(review_signals),
        "review_signals": review_signals,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
