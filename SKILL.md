---
name: r-data-lineage-plotting
description: Enforce traceable data lineage for R, ggplot2, microbiome, transcriptome, network, differential-analysis, and publication-figure workflows. Use whenever creating, revising, debugging, or rerunning R analysis/plotting scripts; reorganizing data/output/result/review directories; separating reviewer materials from scientific results; changing metadata labels, filters, thresholds, transformations, statistics, or upstream inputs; or checking that figures and reported values use synchronized computed data rather than stale, copied, or hardcoded results.
---

# R Data Lineage and Plotting

Apply this storage contract:

`data raw/base inputs -> R computation -> output intermediates -> result/tables final summaries -> result/figs figures`

Keep review artifacts on a separate branch: `review/`. Review artifacts never become analysis inputs unless explicitly promoted through a documented revision step.

Apply this execution model:

`data -> independent analysis modules -> output/module -> result/tables and result/figs`

Treat the project as a DAG rooted in authoritative inputs, not as a compulsory linear sequence such as `01_prepare_data.R -> 02_statistics.R -> 03_plot.R`. PCoA, alpha diversity, differential abundance, heatmaps, networks, and assembly-process analyses usually share base observations but are not automatically upstream of one another.

## Project layout

```
project/
├── data/                  # irreducible raw/base inputs only
├── output/<module>/       # intermediates, plot_data, audit, provenance per module
├── result/
│   ├── tables/            # final manuscript/supplement statistics only
│   └── figs/              # figures; never a data source
└── review/                # reviewer materials; never analysis inputs
```

## Start every task

1. Resolve the project root explicitly. Never infer inputs by recursively selecting the newest or similarly named file.
2. Inventory `/data`, R scripts, `/output`, `/result/tables`, and downstream reads before editing.
3. Read `references/failure-modes.md` when reorganizing an existing project or diagnosing stale results.
4. Run `scripts/audit_r_lineage.py <project-root>` before and after material changes. Exit code 0 = PASS, 2 = FAIL; the JSON report is written to `--report` (default `output/audit/r_data_lineage_audit.json`). Supply `--allowlist` when the project has a raw-input whitelist, and `--scripts dir1,dir2` to scan additional script locations beyond `script` and `scripts`.
5. Define the analysis-module boundary before proposing files or dependencies. Do not infer that a file belongs in `/data` merely because an existing script reads it.
6. Pair with `write-human-r-code` when scripts also need structural or style refactoring: this skill governs data lineage and directory roles, that one governs script structure and readability.

## Classify files

- Put only irreducible inputs in `/data`: raw/base abundance, taxonomy, metadata, sequences, upstream-authoritative transcriptome tables, and raw environmental measurements.
- Put every cleaned, filtered, aggregated, normalized, transformed, modeled, matched, residualized, bootstrapped, or plotting-ready file in `/output`.
- Put nodes, edges, network objects, robustness replicates/curves, coordinates, heatmap matrices, audit tables, QA, logs, and serialized objects in `/output`.
- Put only final manuscript/supplement statistics and durable result summaries in `/result/tables`.
- Put figures in `/result/figs`; never treat a figure-export folder as a data source.
- Put reviewer reports, response drafts, review notes, decision letters, manuscript-review annotations, and LLM/referee assessments in `/review`.
- Do not classify a scientific table as a review artifact merely because it contains a `review` column or `REVIEW` status. Require filename/path semantics, explicit front matter such as `artifact_type: review`, or a review index that designates the whole file as review material.
- If a derived file lacks its upstream generator, move it out of `/data`, label it `legacy derived`, preserve its checksum, and state that full reconstruction is not yet possible.

## Write R scripts

At the top of each script, declare exact input and output paths plus key parameters. Prefer a shared path file:

```r
project_dir <- normalizePath(file.path(script_dir, ".."), winslash = "/", mustWork = TRUE)
data_dir <- file.path(project_dir, "data")
output_dir <- file.path(project_dir, "output")
final_table_dir <- file.path(project_dir, "result", "tables")
figure_dir <- file.path(project_dir, "result", "figs")
```

Obtain `script_dir` robustly (e.g. from `commandArgs(trailingOnly = FALSE)` or `rstudioapi::getSourceEditorContext()`); never rely on `setwd()`.

Follow these rules:

- Read raw inputs only from `data_dir`.
- Read upstream computed inputs only from `output_dir`.
- Never write into `/data`.
- Never hardcode P values, significance labels, sample sizes, AUC values, topology metrics, or group classifications in plotting code.
- Compute plot annotations from standardized upstream tables in the same run.
- Use one authoritative object/table for network figures, topology, robustness, and AUC.
- Record seeds, thresholds, filtering rules, transformations, factor levels, contrast direction, and package versions.
- When metadata, mapping, thresholds, or upstream files change, rerun all affected upstream and downstream scripts.

## Let each analysis own its preparation

- Default to a self-contained analysis script for an ordinary figure or test: configure -> read authoritative inputs -> validate and align samples -> prepare data for this analysis -> compute statistics -> write module outputs -> plot -> save figure.
- Do not create a project-wide `01_prepare_data.R` or generic `prepared_data.csv` before the downstream scientific questions and transformations are known.
- Do not split a script merely to make the directory look like a pipeline. A moderately complex script with one coherent scientific purpose may remain one file.
- Split an independent `prepare` or compute script only when preparation is computationally expensive or conceptually substantial and its formal outputs are reused by multiple consumers within the same analysis module. Network construction, iCAMP, SEM, and multi-omics integration are common candidates, but the decision remains evidence-based.
- When split, write formal module outputs to a dedicated `/output/<module>/` namespace and make every downstream panel consume the same authoritative objects. Document the generator, consumers, parameters, seed, and invalidation triggers.
- Permit `/output` reuse inside a module. Treat cross-module reuse as an explicit scientific dependency: document why the producer's definition is part of the consumer's analysis, or let the consumer start again from authoritative `/data` inputs.
- Never use another module's convenient selection, plotting table, or cached result as an undocumented fact source.

Use two questions to decide whether to split preparation:

1. Does the prepared object serve only one figure or result? Keep preparation in that analysis script.
2. Is preparation expensive or scientifically substantial, and is the same formal object consumed by several downstream outputs? Split it and register the dependency.

## Migrate safely

1. Resolve every source and destination to absolute paths inside the project.
2. Generate a preflight manifest with source, destination, classification, size, modified time, and SHA-256.
3. Move only explicit files or directories; never use ambiguous recursive name matching for destructive operations.
4. Recompute SHA-256 after moving and require exact equality.
5. Update generators before consumers, then search for stale paths with `rg`.
6. Parse all affected R scripts and rerun representative affected panels.
7. Keep migration and provenance registries under `/output/provenance` and QA under `/output/audit`.
8. When moving review artifacts, preserve their relative substructure under `/review`, record checksums, and update any review index. Do not move final scientific results referenced by manuscript figures.
9. Audit and classify first; migrate only after the authoritative-input set and reconstruction boundaries are known. Never backfill `/data` by searching historical projects for whatever filenames current scripts happen to miss.

## Gate completion

Require all of the following:

- no unapproved file in `/data`;
- no script writes to `/data`;
- no script reads a moved derived file from `/data`;
- no plotting script reads a manually edited or unexplained table;
- no intermediate-pattern file remains in `/result/tables`;
- no review artifact remains under `/result`; status fields named `review` are exempt unless the whole file is explicitly review material;
- all moved files pass checksum verification;
- affected R scripts parse and execute;
- limitations from missing upstream generators are explicit.
- no unexplained project-wide prepared-data layer exists;
- module-internal and cross-module dependencies are distinguished and every cross-module edge has a scientific justification and invalidation rule;

Report counts, failures, migrated paths, validation commands, and reconstruction boundaries. Do not claim complete reproducibility when a legacy-derived input has only a migration record.
