# ANDD: Fully Reproducible Construction Pipeline

**Antibody and Nanobody Design Dataset (ANDD)**

---

## 1. Purpose and Scope

This repository provides a **fully scripted, end-to-end computational pipeline** for reconstructing the **Antibody and Nanobody Design Dataset (ANDD)** from raw public data sources.

All dataset construction steps—including data acquisition, parsing, harmonisation, de-duplication, filtering, labelling, affinity standardisation, prediction, and validation—are implemented as **command-line scripts**.
**No manual web-interface operations are required to reproduce the released version of ANDD.**

The pipeline is designed to be:

* **Deterministic**: identical inputs yield identical outputs
* **Transparent**: all rules are explicit and version-controlled
* **Extensible**: new sources can be added via configuration files

---

## 2. Data Sources Covered

ANDD integrates data from **15 authoritative resources**, grouped as follows.

### 2.1 Antibody/Nanobody–specific databases

#### Databases containing both antibody and nanobody

* **abYbank**

  * Access mode: official bulk download
  * Content: curated antibody and nanobody sequences and structures

#### Antibody-focused databases

* **SAbDab**

  * Access mode: official downloadable release (CSV + structure mapping)
  * Content: antibody structures, sequences, antigen annotations
* **OAS (Observed Antibody Space)**

  * Access mode: bulk download via OAS data portal
  * Content: large-scale antibody repertoire sequences
* **AB-Bind**

  * Access mode: curated release (structure + affinity annotations)
  * Content: experimentally measured binding affinities
* **PaddlePaddle antibody datasets**

  * Access mode: published dataset releases
  * Content: antibody sequences and annotations

#### Nanobody-focused databases

* **INDI**

  * Access mode: downloadable structured files
  * Content: nanobody-related interaction data
* **SAbDab-nano**

  * Access mode: official extension of SAbDab
  * Content: nanobody structures and antigens
* **sdAb-DB**

  * Access mode: downloadable tables
  * Content: single-domain antibody (VHH) sequences and annotations
* **PLAbDab**

  * Access mode: official patent-annotated dataset release
  * Content: nanobody and antibody sequences from literature and patents

---

### 2.2 General protein databases

* **PDB (RCSB Protein Data Bank)**

  * Access mode: REST Search API and Data API
  * Used for: structure files (PDB/mmCIF), experimental metadata

* **UniProt**

  * Access mode: UniProt REST API
  * Used for: protein sequences, organism annotations

* **PDBbind**

  * Access mode: official versioned dataset release
  * Used for: structure–affinity mappings

* **SKEMPI 2.0**

  * Access mode: curated dataset download
  * Used for: mutation-level affinity changes

* **DACUM**

  * Access mode: dataset release
  * Used for: mutation and interaction annotations

* **MpdPPI**

  * Access mode: dataset release
  * Used for: mutation effects on protein–protein interactions

---

## 3. Environment Setup

### 3.1 System requirements

* Linux (Ubuntu 20.04+) or macOS
* ≥16 GB RAM recommended
* Internet connection for API access

### 3.2 Create environment

```bash
conda create -n andd python=3.10 -y
conda activate andd
pip install pandas numpy biopython requests tqdm pyyaml scikit-learn
```

---

## 4. Repository Structure

```
ANDD_pipeline/
├── config/
│   ├── sources.yaml        # API endpoints, dataset versions
│   ├── schema.yaml         # consensus data model
│   └── vocabularies.yaml   # controlled vocabularies
│
├── scripts/
│   ├── 01_download_sources.py
│   ├── 02_parse_sources.py
│   ├── 03_filter_antibody_nanobody.py
│   ├── 04_harmonize_schema.py
│   ├── 05_deduplicate.py
│   ├── 06_affinity_standardize.py
│   ├── 07_antipasti_predict.py
│   ├── 08_validation_qc.py
│   └── 09_export_dataset.py
│
├── data/
│   ├── raw/               # untouched source data
│   ├── intermediate/      # parsed and harmonised data
│   └── final/             # ANDD.csv and All_structures/
└── README.md
```

---

## 5. Configuration Files

### 5.1 `config/sources.yaml`

```yaml
PDB:
  search_api: https://search.rcsb.org/rcsbsearch/v2/query
  data_api: https://data.rcsb.org/rest/v1/core/entry
  snapshot: 2025-06-01

UniProt:
  api: https://rest.uniprot.org/uniprotkb/search
  release: 2025_06

SAbDab:
  release: official_csv
  date: 2025-08-14

SAbDab-nano:
  release: official_csv
  date: 2025-08-14

OAS:
  release: bulk_download
  snapshot: 2021-10

AB-bind:
  version: v1.0
  release_date: 2023-03

PaddlePaddle-Ab:
  version: official_published_release
  release_date: 2023-05

INDI:
  version: v1.0
  release_date: 2022-11

sdAb-DB:
  version: v1.0
  release_date: 2022-09

PLAbDab:
  version: curated_release
  release_date: 2024-01

PDBbind:
  version: v2020

SKEMPI:
  version: 2.0

DACUM:
  version: original_published_release
  release_date: 2021

MpdPPI:
  version: original_published_release
  release_date: 2020

abYbank:
  version: latest_public_release
  release_date: 2023-06

---

## 6. End-to-End Rebuild Procedure

### Step 1 — Automated data retrieval

```bash
python scripts/01_download_sources.py
```

This script:

* Queries **PDB Search API** to retrieve antibody/nanobody-related PDB IDs
* Downloads structure metadata via **PDB Data API**
* Retrieves UniProt entries using keyword-based REST queries
* Loads official dataset releases for SAbDab, OAS, PDBbind, SKEMPI, DACUM, MpdPPI

All raw files are stored **unchanged** in `data/raw/`.

---

### Step 2 — Parsing heterogeneous formats

```bash
python scripts/02_parse_sources.py
```

* Parses CSV, TSV, JSON, XML, mmCIF
* Extracts sequences, chains, antigen entities, affinity values
* Preserves original source identifiers and provenance

---

### Step 3 — Antibody/nanobody filtering

```bash
python scripts/03_filter_antibody_nanobody.py
```

* Removes T-cell receptors and non-immunoglobulin proteins
* Classifies entries into **Antibody / VHH / scFv / BJ**
* Uses IMGT-inspired domain rules and chain composition

---

### Step 4 — Schema harmonisation

```bash
python scripts/04_harmonize_schema.py
```

* Maps all sources into the **ANDD consensus schema**
* Enforces controlled vocabularies
* Explicitly assigns `NA` for missing fields

---

### Step 5 — De-duplication and conflict resolution

```bash
python scripts/05_deduplicate.py
```

Duplicate detection is based on:

* PDB ID + chain identifiers
* Sequence identity ≥ 99%

Conflict resolution priority:

1. Experimentally validated databases
2. Curated antibody/nanobody databases
3. Automated or inferred annotations

---

### Step 6 — Affinity standardisation

```bash
python scripts/06_affinity_standardize.py
```

* Converts all affinity values to **Kd (M)**
* Computes ΔG only when assay and temperature are available
* Assigns `Reason_Code` (`not_reported`, `conflicting`, `inferred`)

---

### Step 7 — Affinity prediction (optional)

```bash
python scripts/07_antipasti_predict.py
```

* Runs **ANTIPASTI** on structure-available entries
* Clearly marks predicted values
* Never overwrites experimental measurements

---

### Step 8 — Validation and quality control

```bash
python scripts/08_validation_qc.py
```

Generates:

* Field-level completeness statistics
* Duplicate counts
* Cross-source consistency reports

---

### Step 9 — Final export

```bash
python scripts/09_export_dataset.py
```

Produces:

* `data/final/ANDD.csv`
* `data/final/All_structures/`

---

### Step 10 — DiffAb fine-tuning and evaluation

This workflow is provided solely as a proof-of-concept demonstration of dataset usability.
It is not intended as a benchmark or comparative evaluation of DiffAb or any other generative model.
No claims regarding model performance or state-of-the-art results are made.

---


## 7. Reproducibility Statement

All steps required to construct ANDD are implemented as executable scripts.
**The complete dataset can be rebuilt from raw public sources in a clean environment without any manual intervention or web-based operations.**

---

## 8. License and Data Usage

All source datasets are used in accordance with their original licenses.
ANDD is released under **CC BY 4.0**; users must cite the ANDD publication when using the dataset.

