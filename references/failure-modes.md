# Failure modes and fixes

## Data-lineage bugs

- **Compulsory global preparation layer**: a project-wide `01_prepare_data.R` produces an ambiguous table intended to serve PCoA, differential abundance, heatmaps, and networks despite different filtering and transformation semantics. Let each analysis own preparation; split only substantial shared compute within a defined module.
- **Linearizing independent analyses**: heatmap selections or PCoA outputs become accidental upstream inputs to networks or iCAMP. Model the project as a DAG rooted in authoritative inputs and justify every cross-module edge scientifically.
- **Convenience reuse across modules**: one module reads another module's plotting-ready or selected table because it is available. Recompute from authoritative inputs unless the producer's scientific definition is explicitly part of the consumer, then register invalidation triggers.

- **Derived files in `/data`**: network, nodes, edges, robustness, AUC, CLR, residuals, DR-ASV matches/gates, assembly-process tables, plot coordinates, and manifests were treated as inputs. Move them to `/output`; retain only irreducible inputs in `/data`.
- **Copied legacy results**: old network objects can remain internally consistent while having no defensible connection to current abundance/metadata. Never audit them into legitimacy; rebuild from raw/base inputs or label them legacy-derived.
- **Stale downstream figures**: changing labels, filtering, thresholds, or normalized data without rerunning figures leaves plots and statistics out of sync. Maintain explicit generator-consumer paths and rerun the dependency chain.
- **Multiple authoritative networks**: constructing the plot, topology, robustness, and AUC with different packages or edge tables creates silent disagreement. Produce one formal node/edge source and make all consumers read it.
- **Hardcoded annotations**: embedded P values, stars, sample sizes, AUC, labels, or conclusions survive upstream changes. Generate annotations from saved computed outputs.
- **Final/intermediate mixing**: PCoA coordinates, heatmap matrices, curves, audit tables, and QA appeared in `/result/tables`. Route them to `/output/plot_data` or `/output/audit`.
- **Missing generator disguised as raw**: a historical iCAMP process table lacked complete upstream project inputs. Moving it to `/output` fixes classification, not reconstructability; record the boundary explicitly.
- **Substring-based review migration**: moving every file containing the word `review` can remove valid scientific tables whose `review` column is only a classification state. Classify the artifact as a whole using its path, filename, front matter, or an explicit review index before moving it to `/review`.

## Label and metadata bugs

- **Implicit CK/SC recoding**: group mapping hidden inside factor levels or filenames makes label swaps hard to detect. Save an explicit source-to-analysis mapping and sample-level audit.
- **Sample-set equality mistaken for order equality**: metadata and abundance columns can contain the same IDs in different orders. Check `setequal()`, reorder with `match()`, then require `identical()`.
- **Factor levels driving contrasts silently**: record numerator, denominator, reference level, and the meaning of positive log2FC.

## Statistical and plotting bugs

- **Temporal pooling without control**: pooled D5/D15/D25 associations can reflect common time trends. Residualize time or model it explicitly and describe the network as treatment-specific association across time.
- **Simulation replicates treated as biological replicates**: random-removal runs do not create independent biological networks. Treat single-network AUC as descriptive unless bootstrap reconstruction or a valid permutation design exists.
- **Static versus dynamic targeted attack ambiguity**: record whether degree is recomputed after every deletion and make the legend match the implementation.
- **Curve/AUC mismatch**: integrate exactly the displayed data over identical ranges and steps; state normalization and whether AUC is per replicate or from the mean curve.
- **Axis limits delete geometry**: use `coord_cartesian()` for visual y-range restriction when geoms depend on a zero baseline; avoid `scale_y_continuous(limits=...)` unless dropping data is intentional.

## Migration and execution bugs

- **PowerShell compact operators fail parsing**: write spaces around `-ne`, `-or`, and related operators.
- **Profile warnings hide the actual failure**: run noninteractive migration commands without loading the user profile when possible.
- **Timeout after successful work**: verify source absence, destination existence, file count, hashes, and persisted manifest rather than trusting the wrapper exit alone.
- **Partial move without preflight**: create a per-file checksum manifest before moving containers; validate every target afterward.
- **False-positive path scan**: use token/word boundaries so `data_dir` does not match `table_dir`; exclude the audit script from self-scanning.
- **R package false absence**: first report the actual `Rscript`, `R.version.string`, `R.home()`, and `.libPaths()` before installing or declaring a package missing.
