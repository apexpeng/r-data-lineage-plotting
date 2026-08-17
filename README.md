<p align="center">
  <img src="assets/banner.svg" width="100%" alt="r-data-lineage-plotting banner">
</p>

<div align="center">

# 🌿 r-data-lineage-plotting

**Every figure should know where it came from.**

[![R](https://img.shields.io/badge/R-Data%20Lineage-276DC3?style=flat-square&logo=r)](#)
[![Scientific Plotting](https://img.shields.io/badge/scientific-plotting-success?style=flat-square)](#)
[![Reproducibility](https://img.shields.io/badge/reproducibility-first-blue?style=flat-square)](#)

**English** · [简体中文](./README.zh-CN.md)

</div>

---

## 📊 A figure is never just a figure

A final panel may look simple:

```text
Figure 5D
```

but behind it may be:

```text
OTU / ASV table
→ filtering
→ transformation
→ model / statistics
→ intermediate object
→ plotting
→ final figure
```

When these steps are disconnected, reproducibility disappears.

`r-data-lineage-plotting` keeps the lineage explicit.

## 🌱 The central idea

```mermaid
flowchart LR
    A["📦 Raw data"] --> B["🧹 Data preparation"]
    B --> C["🧪 Analysis"]
    C --> D["📊 Plot-ready object"]
    D --> E["🎨 Figure"]
    E --> F["📁 Final output"]
```

Every arrow should be reproducible.

## 🔍 Every result should answer four questions

```mermaid
mindmap
  root((Figure))
    Source
      Raw dataset
      Metadata
    Processing
      Filtering
      Transformation
    Analysis
      Method
      Parameters
    Output
      Script
      Figure
      Table
```

A researcher should be able to ask:

> Where did this figure come from?  
> Which script generated it?  
> Which transformations occurred?  
> If the source data change, will the figure change too?

## 🗂 Data directory philosophy

### `/data`

Stable source inputs, for example:

```text
raw sequencing data
OTU / ASV tables
taxonomy tables
metadata
upstream transcriptome tables
environmental measurements
```

### `/output`

Reproducible derived data:

```text
ordination objects
network tables
model outputs
intermediate statistics
```

### `/result`

Formal deliverables:

```text
figures
publication tables
supplementary tables
```

## 🚨 The problem this Skill tries to prevent

```mermaid
flowchart TD
    A["data/raw.csv"] --> B["analysis"]
    B --> C["derived.csv"]
    C --> D["manually copied derived_v2.csv"]
    D --> E["plot_final.R"]
    A -. changed later .-> F["❌ Figure unchanged"]
```

The figure still exists, but it may no longer represent the current source data.

## ✅ Preferred pattern

For a simple figure:

```text
01_plot_pcoa.R
     ↓
read_data
     ↓
prepare_data
     ↓
statistics
     ↓
plot
```

For computationally expensive analyses:

```text
prepare_network.R
       ↓
network object
       ↓
plot_network.R
```

Intermediate files should exist because the analysis requires them — not because every script automatically writes them.

## 🧬 Data lineage as a dependency graph

```mermaid
flowchart TD
    META["metadata.csv"] --> PREP["prepare_data()"]
    OTU["otu_table.tsv"] --> PREP
    TAX["taxonomy.tsv"] --> PREP

    PREP --> PCOA["PCoA object"]
    PREP --> NET["Network input"]

    PCOA --> FIGA["Fig. 5A"]
    NET --> FIGD["Fig. 5D"]
    PCOA --> TAB1["Supplementary table"]
```

Change a source once. Recompute everything downstream.

## 🧠 AI behavior encouraged by this Skill

Before writing a plotting script, AI should ask:

```text
What are the true source data?
        ↓
What must be calculated?
        ↓
Which intermediates are worth preserving?
        ↓
Which outputs are formal deliverables?
        ↓
How should dependencies be encoded?
```

Not:

```text
Which CSV is most convenient to read right now?
```

## 🔬 Designed for scientific workflows

Especially useful for:

- ecology
- microbial ecology and microbiome analysis
- soil and environmental science
- transcriptomics
- metabolomics
- multi-omics
- publication figures
- complex multi-panel figures

## 🌿 Philosophy

> **A publication figure should be the end of a reproducible data lineage — not the end of a chain of copied files.**
