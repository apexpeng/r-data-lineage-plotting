<p align="center">
  <img src="assets/banner.svg" width="100%" alt="r-data-lineage-plotting banner">
</p>

<div align="center">

[![R](https://img.shields.io/badge/R-Data%20Lineage-276DC3?style=flat-square&logo=r)](#)
[![Scientific Plotting](https://img.shields.io/badge/scientific-plotting-2EA44F?style=flat-square)](#)
[![Reproducibility](https://img.shields.io/badge/reproducibility-first-0A66C2?style=flat-square)](#)
[![AI Agent Skill](https://img.shields.io/badge/AI-Agent%20Skill-6C63FF?style=flat-square)](#)
[![Status](https://img.shields.io/badge/status-active-2EA44F?style=flat-square)](#)

**English** · [简体中文](./README.zh-CN.md)

</div>

---

## 📌 Overview

A scientific figure is never just a figure. Behind one panel may be a long dependency chain of source tables, filtering rules, transformations, models and intermediate objects.

`r-data-lineage-plotting` helps AI build R workflows where every result remains connected to its true source:

> **raw data → processing → analysis → plot object → figure → formal output**

The goal is to make figure generation **traceable, reproducible and resistant to stale intermediate files**.

## 🌱 Data lineage pipeline

```mermaid
flowchart LR
    A["🗃 Raw data"] --> B["🔽 Processing"]
    B --> C["⚙ Analysis"]
    C --> D["📊 Plot object"]
    D --> E["🖼 Figure"]
    E --> F["📁 Output"]
```

Every arrow should be reproducible.

## ✅ Key features

| Feature | Purpose |
|---|---|
| 🌿 **Explicit data lineage** | Every figure can be traced back to true source inputs |
| 🔗 **Dependency-aware workflow** | Upstream changes propagate through downstream analysis |
| 🧪 **Right-sized intermediates** | Save intermediate objects only when computationally justified |
| 📊 **Modular plotting scripts** | Keep input, preparation, analysis, plotting and export visible |
| 🧾 **Reproducible outputs** | Formal figures and tables are regenerated, not manually copied |

## 🗂 Directory philosophy

| Directory | Role | Typical content |
|---|---|---|
| `/data` | Stable source inputs | raw sequencing data, OTU/ASV tables, taxonomy, metadata, upstream omics tables |
| `/output` | Reproducible derived objects | ordinations, network objects, model outputs, intermediate statistics |
| `/result` | Formal deliverables | publication figures, final tables, supplementary tables |

The key rule is simple:

> **Derived data should not quietly become a new source of truth.**

## 🚨 The failure mode this Skill tries to prevent

```mermaid
flowchart TD
    A["data/raw.csv"] --> B["analysis"]
    B --> C["derived.csv"]
    C --> D["manually copied derived_v2.csv"]
    D --> E["plot_final.R"]
    A -. source changed later .-> F["❌ Figure remains stale"]
```

The figure still exists — but it may no longer represent the current source data.

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
     ↓
save
```

For a genuinely expensive workflow:

```text
prepare_network.R
       ↓
network object
       ↓
plot_network.R
```

The distinction is intentional: intermediate files exist because the analysis needs them, not because every script automatically writes them.

## 🧬 Dependency graph thinking

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

## 🧠 What AI should ask before plotting

```text
What are the true source data?
        ↓
What must be calculated?
        ↓
Which intermediate objects are worth preserving?
        ↓
Which outputs are formal deliverables?
        ↓
How should dependencies be encoded?
```

Not:

```text
Which CSV is most convenient to read right now?
```

## 🎯 Suitable for

- ecology and microbial ecology
- microbiome analysis
- soil and environmental science
- transcriptomics and metabolomics
- multi-omics workflows
- publication-quality figures
- complex multi-panel scientific figures

---

> **A publication figure should be the end of a reproducible data lineage — not the end of a chain of copied files.**
