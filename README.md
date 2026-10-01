# Genomic Variants Dashboard

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-data%20processing-150458?logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-visualization-4C72B0)
![Tableau](https://img.shields.io/badge/Tableau-workbook-E97627?logo=tableau&logoColor=white)

An exploratory bioinformatics workflow for chromosome 22 variants from the 1000 Genomes Project. It reads a compressed VCF, extracts population allele frequencies, writes analysis-ready CSV files, and generates plots for variant positions, alleles, variant types, and population frequencies. A Tableau workbook is also maintained with the processed data.

## Project Goal

Transform chromosome 22 variant records into a tidy dataset for exploratory analysis, compare allele-frequency distributions across five populations, and prepare tabular data for visualization in Tableau.

Populations represented: East Asian (EAS), African (AFR), Admixed American (AMR), South Asian (SAS), and European (EUR).

## Project Structure

```text
genomic_variants_dashboard/
|
|-- data/
|   |-- raw/                         # Source VCF (local, not tracked by Git)
|   `-- processed/                  # Generated CSVs and local Tableau workbook
|
|-- results/
|   `-- figures/                     # EDA figures (.png)
|
|-- scripts/
|   `-- setup.ps1                    # uv and pre-commit bootstrap (see setup note)
|
|-- src/
|   `-- variantes_genomicas/
|       |-- EDA.py                   # Loads processed data and creates figures
|       `-- explore_vcf.py           # Reads VCF, extracts INFO fields, exports CSVs
|
|-- tests/                           # pytest tests
|-- pyproject.toml                   # Dependencies, Ruff, and pytest configuration
|-- uv.lock                          # Locked dependency versions
`-- README.md
```

The raw and processed data directories are excluded by `.gitignore`. The Tableau workbook currently resides in `data/processed/Libro1.twb`, so it is local to this checkout and is not included in a fresh clone. Generated figures are saved under `results/figures/`.

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/moralesgomez-dev/genomic-variants-dashboard.git
cd genomic-variants-dashboard
```

### 2. Create the environment

Install [uv](https://docs.astral.sh/uv/), then synchronize the locked dependencies and development tools:

```bash
uv sync --all-extras
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

### 3. Add the source VCF

Obtain the chromosome 22 Phase 3 VCF from the 1000 Genomes Project and place it in `data/raw/` with this filename:

```text
ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz
```

This large input file is intentionally not committed to the repository.

### 4. Run the workflow

Both scripts resolve their default data and output paths from their source locations, so they can be run from any current working directory. Run VCF processing first, followed by EDA:

```bash
python src/variantes_genomicas/explore_vcf.py
python src/variantes_genomicas/EDA.py
```

The first script writes processed files to `data/processed/`; the second reads `final_variants_chr22.csv` and saves the figures to `results/figures/`.

To use a different VCF or output directory, pass `--input-vcf` and `--output-dir` to `explore_vcf.py`.

## Pipeline Overview

### VCF processing

`explore_vcf.py`:

- Reads the VCF header and uses its `#CHROM` row for column names; compressed `.gz` input is supported.
- Retains chromosome, position, reference and alternate alleles, quality, filter, format, ID, and INFO data.
- Extracts `EAS_AF`, `AMR_AF`, `AFR_AF`, `EUR_AF`, `SAS_AF`, and `VT` from INFO. Allele-frequency fields are converted to numeric values; unavailable values become missing data.
- Writes these files to `data/processed/`:
	- `variants_chr22.csv` - retained VCF fields, including INFO.
	- `info_chr22.csv` - extracted population frequencies and variant type.
	- `final_variants_chr22.csv` - merged, one-row-per-variant dataset used by EDA.
	- `tableau_variants_chr22.csv` - long-form population/frequency table.
	- `tableau_variants_chr22_with_variant_id.csv` - the same long-form table with a stable `VariantID` shared across the five population rows for each variant.

### Exploratory figures

`EDA.py` creates the following existing figures; it does not alter the input data:

- `POS_Distribution.png` - chromosome position distribution in megabases.
- `REF_count.png` and `ALT_count.png` - the 15 most frequent reference and alternate alleles.
- `EAS_Distribution.png`, `AFR_Distribution.png`, `AMR_Distribution.png`, `SAS_Distribution.png`, and `EUR_Distribution.png` - allele-frequency histograms. Frequencies span 0 to 1; the log scale is applied to variant counts, not to frequency values.
- `VT_frecuency.png` - counts by variant type from the VCF INFO field.
- `boxplot.png` - population frequency boxplots, zoomed to 0-1.5% so quartiles and whiskers are legible. Individual outlier markers are hidden to avoid overplotting.
- `violinplot.png` - population frequency distributions, zoomed to 0-5%. Values above the displayed range are clipped in this view, not removed from the data.

## Dataset Snapshot

The locally processed `final_variants_chr22.csv` contains 1,103,547 variant rows. Each of the five population-frequency columns has 6,348 missing values (about 0.58%); these are kept as missing rather than treated as zero. Values in the allele-frequency fields range from 0 to 1.

## Tableau

`data/processed/Libro1.twb` is the Tableau Desktop workbook used with the processed CSVs, including the long-form file with `VariantID`. Generate the processed CSVs before opening the workbook. Its text connection uses a relative folder (`.`), so keep the workbook beside its CSV files. Tableau Desktop is required to open and interact with the workbook.

## Development and Tests

Development dependencies include pytest, Ruff, pre-commit, and ipykernel. The repository's CI workflow is configured to run Ruff and pytest:

```bash
ruff check .
python -m pytest
```

The tests use small synthetic VCF files and do not require the full chromosome dataset.

## Current Limitations

- Raw and processed data, including the Tableau workbook, are ignored by Git; users must obtain the VCF and regenerate the CSVs locally.
- Processing the complete VCF can require substantial memory because genotype columns are read before the project selects the variant fields it needs.

## Author

[moralesgomez-dev](https://github.com/moralesgomez-dev)
