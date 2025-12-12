# Unit 1 - Coding Environments

A comprehensive bioinformatics toolkit for analyzing mouse genome SNP data, featuring modular Python libraries, automated processing pipelines, and interactive Jupyter notebooks.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Workflow](#workflow)
- [Core Library](#core-library)
- [Data Processing Scripts](#data-processing-scripts)
- [Automation Scripts](#automation-scripts)
- [Jupyter Notebooks](#jupyter-notebooks)
- [Installation & Setup](#installation--setup)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)

---

## Overview

This project provides a complete pipeline for processing and analyzing mouse chromosome genotype data. It includes tools for extracting SNP sequences, analyzing codon frequencies, calculating GC content, and visualizing results through interactive notebooks.

### Key Features

- **Modular design** - Reusable DNA operation functions in a centralized library
- **Automated processing** - Batch processing of all 20 mouse chromosomes
- **Comprehensive analysis** - SNP extraction, codon counting, and GC content calculation
- **Interactive exploration** - Jupyter notebooks for data visualization and analysis
- **Production-ready** - Error handling, skip flags, and progress reporting

---

## Project Structure

```
U1-coding-environment/
├── README.md                      # This file
├── data/                          # Hidden
│   └── mouse/
│       ├── chr1.Build37.data      # Original genotype data (chr1-20)
│       ├── chr1.Build37.snp       # Extracted SNP sequences
│       ├── chr1.Build37.codons    # Codon frequency analysis
│       └── chr1.Build37.cg        # GC content analysis
├── notebooks/
│   └── problem-set-1.ipynb        # Interactive data analysis notebook
└── scripts/
    ├── dna_ops.py                 # Core DNA operations library
    ├── codon_counter.py           # Codon frequency analyzer
    ├── cg.py                      # GC content calculator
    ├── download-mouse-data.sh     # Data download script
    └── extract-mouse-ops.sh       # Automated processing pipeline
```

---

## Data Sources

### Mouse Genome SNP Data (Build 37)

**Source:** University College London - Heterogeneous Stock Mice Database  
**URL:** http://mtweb.cs.ucl.ac.uk/HSMICE/GENOTYPES/  
**Format:** Space-delimited text files

#### File Structure

Each chromosome file (`chr1.Build37.data` through `chr20.Build37.data`) contains:

```
SAMPLE_ID  INFO  META1  META2  META3  NA  NUCLEOTIDE_SEQUENCE...
1_47       6.13  0      0      1      NA  A G A G C C T G G A...
```

**Columns:**
- **1-5:** Sample metadata (ID, lineage information, indices)
- **6:** "NA" marker (separates metadata from sequence data)
- **7+:** SNP genotype calls (A, T, G, C nucleotides, space-separated)

#### Data Characteristics

- **Coverage:** All 20 mouse autosomes
- **Build:** Mouse genome Build 37
- **Samples:** Multiple mouse strains with heterogeneous genetic backgrounds
- **SNPs:** High-density single nucleotide polymorphism data
- **File sizes:** Varies by chromosome (typically 1-10 MB per file)

#### Biological Context

This data comes from the Heterogeneous Stock (HS) mouse population, which is used for high-resolution genetic mapping. The SNP data represents genetic variation across different chromosomal positions, useful for:
- Quantitative trait locus (QTL) mapping
- Genetic diversity studies
- Genome-wide association studies (GWAS)
- Understanding evolutionary relationships

---

## Workflow

### Complete Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  1. DATA ACQUISITION                                        │
│     download-mouse-data.sh                                  │
│     ↓                                                        │
│     chr1-20.Build37.data (raw genotype files)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. AUTOMATED PROCESSING                                    │
│     extract-mouse-ops.sh                                    │
│                                                             │
│     For each chromosome:                                    │
│     ┌─────────────────────────────────────────────┐        │
│     │ a) SNP Extraction (cut command)             │        │
│     │    → chr*.Build37.snp                       │        │
│     ├─────────────────────────────────────────────┤        │
│     │ b) Codon Analysis (codon_counter.py)        │        │
│     │    → chr*.Build37.codons                    │        │
│     ├─────────────────────────────────────────────┤        │
│     │ c) GC Content (cg.py)                       │        │
│     │    → chr*.Build37.cg                        │        │
│     └─────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. INTERACTIVE ANALYSIS                                    │
│     Jupyter Notebooks (problem-set-1.ipynb)                │
│     - Codon frequency visualization                         │
│     - GC content statistics                                 │
│     - Comparative analysis across chromosomes               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Raw Data** → Contains metadata + SNP sequences
2. **SNP Files** → Pure nucleotide sequences (metadata removed)
3. **Analysis Outputs** → Codon frequencies and GC percentages
4. **Visualization** → Interactive exploration in Jupyter

---

## Core Library

### `dna_ops.py`

**Purpose:** Centralized library of reusable DNA sequence operations

**Location:** `scripts/dna_ops.py`

#### Functions

##### 1. `clean_dna_sequence(dna_string)`

Prepares raw DNA sequences for analysis by normalizing format.

**Parameters:**
- `dna_string` (str): Raw DNA sequence with potential spaces, mixed case, and "NA" markers

**Returns:**
- `str`: Cleaned sequence (uppercase, no spaces, NA→_)

**Example:**
```python
>>> from dna_ops import clean_dna_sequence
>>> clean_dna_sequence("a t g NA c g")
'ATG_CG'
```

**Use Cases:**
- Preprocessing raw genotype data
- Standardizing sequence format across datasets
- Handling missing data markers

---

##### 2. `count_codons(dna_sequence)`

Analyzes non-overlapping 3-nucleotide codon frequencies.

**Parameters:**
- `dna_sequence` (str): Cleaned DNA sequence (uppercase)

**Returns:**
- `dict`: Dictionary mapping codons to their occurrence counts

**Algorithm:**
- Scans sequence in non-overlapping windows of 3 nucleotides
- Starts at position 0, 3, 6, 9, etc.
- Ignores incomplete codons at sequence end

**Example:**
```python
>>> from dna_ops import count_codons
>>> count_codons("ATGATGCCC")
{'ATG': 2, 'CCC': 1}
```

**Biological Significance:**
- Codons are the fundamental units of genetic translation
- Codon usage patterns vary across organisms and genes
- Frequency analysis reveals coding region characteristics

---

##### 3. `calculate_gc_content(dna_sequence)`

Calculates the percentage of guanine (G) and cytosine (C) nucleotides.

**Parameters:**
- `dna_sequence` (str): DNA sequence (should be uppercase)

**Returns:**
- `float`: GC content as percentage (0.0 to 100.0)

**Formula:**
```
GC% = ((count_G + count_C) / total_nucleotides) × 100
```

**Example:**
```python
>>> from dna_ops import calculate_gc_content
>>> calculate_gc_content("ATCGATCG")
50.0
>>> calculate_gc_content("AAAA")
0.0
>>> calculate_gc_content("CCGG")
100.0
```

**Biological Significance:**
- GC content affects DNA stability (GC pairs have 3 hydrogen bonds vs AT's 2)
- Varies across genomes: bacteria (25-75%), mammals (~40%)
- Gene-rich regions often have higher GC content
- Important for PCR primer design and sequencing

---

#### Testing

The library includes built-in unit tests:

```bash
python3 scripts/dna_ops.py
```

**Expected Output:**
```
✓ All tests passed
```

---

## Data Processing Scripts

### `codon_counter.py`

**Purpose:** Analyzes codon frequency patterns in DNA sequences

**Location:** `scripts/codon_counter.py`

**Dependencies:** `dna_ops.py` (clean_dna_sequence, count_codons)

#### Functionality

Reads DNA sequences from standard input, processes each line independently, and outputs the three most frequent codons with their proportions.

#### Algorithm

1. Read each line from stdin
2. Clean the sequence (remove spaces, handle NA values)
3. Count all codons in the sequence
4. Sort by frequency (descending) and alphabetically (for ties)
5. Select top 3 codons
6. Calculate proportions relative to total codon count
7. Format as `CODON:proportion` (2 decimal places)

#### Usage

```bash
# Single file processing
cat data/mouse/chr1.Build37.snp | python3 scripts/codon_counter.py > output.codons

# Pipeline integration
python3 scripts/codon_counter.py < input.snp > output.codons
```

#### Input Format

Space-separated nucleotide sequences (one per line):
```
A G A G A G A G C C A T G G A G
C C C G G G A A A T T T
```

#### Output Format

Top 3 codons per line with proportions:
```
AGA:0.20 AGC:0.20 CAT:0.20
AAA:0.25 CCC:0.25 GGG:0.25
```

**Format Specification:**
- Each line corresponds to one input line
- Space-separated triplets: `CODON:proportion`
- Proportions sum to ≤1.00 (only top 3 shown)
- Sorted by frequency (highest first)

#### Example Analysis

**Input sequence:**
```
A T G A T G A T G C C C
```

**Processing:**
1. Cleaned: `ATGATGATGCCC`
2. Codons extracted: `ATG ATG ATG CCC` (4 total)
3. Frequencies: `{'ATG': 3, 'CCC': 1}`
4. Proportions: ATG=0.75, CCC=0.25
5. Output: `ATG:0.75 CCC:0.25`

---

### `cg.py`

**Purpose:** Calculates GC content for genomic sequences

**Location:** `scripts/cg.py`

**Dependencies:** `dna_ops.py` (clean_dna_sequence, calculate_gc_content)

#### Functionality

Reads DNA sequences from standard input and calculates the percentage of G and C nucleotides in each sequence.

#### Algorithm

1. Read each line from stdin
2. Clean the sequence
3. Count G and C nucleotides
4. Calculate percentage: (G+C)/total × 100
5. Output percentage with 2 decimal places

#### Usage

```bash
# Single file processing
cat data/mouse/chr1.Build37.snp | python3 scripts/cg.py > output.cg

# Pipeline integration
python3 scripts/cg.py < input.snp > output.cg
```

#### Input Format

Space-separated nucleotide sequences:
```
A T C G A T C G
C C C G G G
A A A A
```

#### Output Format

One percentage per line:
```
50.00
100.00
0.00
```

#### Interpretation

- **<40%:** AT-rich regions (often intergenic, repetitive elements)
- **40-50%:** Average mammalian GC content
- **50-60%:** Gene-rich regions, active transcription
- **>60%:** CG islands (promoter regions, regulatory elements)

#### Example Analysis

**Input:** `A T C G A T C G`

**Processing:**
1. Cleaned: `ATCGATCG` (8 nucleotides)
2. G count: 2
3. C count: 2
4. Total GC: 4
5. Percentage: (4/8) × 100 = 50.00%

**Output:** `50.00`

---

## Automation Scripts

### `download-mouse-data.sh`

**Purpose:** Automated download of mouse genome data files

**Location:** `scripts/download-mouse-data.sh`

#### Functionality

Downloads all 20 mouse chromosome genotype files from the UCL HSMICE database using curl. Supports incremental downloads with optional skip flag.

#### Usage

```bash
./download-mouse-data.sh <destination_directory> [--skip]
```

**Arguments:**
- `destination_directory` (required): Directory where files will be saved
- `--skip` (optional): Skip files that already exist locally

#### Examples

```bash
# Download all chromosomes
./download-mouse-data.sh data/mouse

# Resume interrupted download (skip existing files)
./download-mouse-data.sh data/mouse --skip

# Show help
./download-mouse-data.sh -h
```

#### Features

- **Batch download:** Retrieves chr1.Build37.data through chr20.Build37.data
- **Progress indication:** Reports each file as it downloads
- **Error handling:** Validates destination directory exists
- **Resume capability:** Skip flag prevents re-downloading existing files
- **Rate limiting:** 0.5 second delay between downloads
- **Robust:** Uses curl with output file specification

#### Output

Downloads 20 files (approximately 50-200 MB total):
```
data/mouse/chr1.Build37.data
data/mouse/chr2.Build37.data
...
data/mouse/chr20.Build37.data
```

#### Implementation Details

- **URL pattern:** `http://mtweb.cs.ucl.ac.uk/HSMICE/GENOTYPES/chr{N}.Build37.data`
- **Loop range:** Chromosomes 1-20
- **Download tool:** curl with `-o` flag for output naming
- **Polite delay:** 0.5s sleep between requests

---

### `extract-mouse-ops.sh`

**Purpose:** Automated batch processing pipeline for mouse genome analysis

**Location:** `scripts/extract-mouse-ops.sh`

#### Functionality

Processes all mouse chromosome data files through a three-stage analysis pipeline, generating SNP extracts, codon frequencies, and GC content for each chromosome.

#### Usage

```bash
./scripts/extract-mouse-ops.sh <data_directory> [--skip]
```

**Arguments:**
- `data_directory` (required): Directory containing `.data` files
- `--skip` (optional): Skip generation of existing output files

#### Examples

```bash
# Process all chromosomes
./scripts/extract-mouse-ops.sh data/mouse

# Reprocess with skip (useful after fixing issues)
./scripts/extract-mouse-ops.sh data/mouse --skip

# Show help
./scripts/extract-mouse-ops.sh -h
```

#### Three-Stage Pipeline

##### Stage 1: SNP Extraction

**Operation:** Extract nucleotide columns from raw data

**Tool:** `cut` command

**Input:** `chr*.Build37.data`  
**Output:** `chr*.Build37.snp`

**Command:**
```bash
cut -d' ' -f7- input.data > output.snp
```

**What it does:**
- Uses space as delimiter (`-d' '`)
- Selects fields 7 through end (`-f7-`)
- Removes sample metadata columns
- Preserves nucleotide sequences

**Before (input):**
```
1_47 6.13:E2.5(4) 0 0 1 NA A G A G C C T G
```

**After (output):**
```
A G A G C C T G
```

---

##### Stage 2: Codon Frequency Analysis

**Operation:** Count and rank non-overlapping codons

**Tool:** `codon_counter.py`

**Input:** `chr*.Build37.snp`  
**Output:** `chr*.Build37.codons`

**Command:**
```bash
python3 scripts/codon_counter.py < input.snp > output.codons
```

**What it does:**
- Processes each sequence line independently
- Identifies all 3-nucleotide codons
- Calculates frequency distribution
- Reports top 3 with proportions

**Example transformation:**
```
Input:  A G A G A G C C T
Output: AGA:0.33 GAG:0.33 CCT:0.33
```

---

##### Stage 3: GC Content Calculation

**Operation:** Calculate genomic GC percentage

**Tool:** `cg.py`

**Input:** `chr*.Build37.snp`  
**Output:** `chr*.Build37.cg`

**Command:**
```bash
python3 scripts/cg.py < input.snp > output.cg
```

**What it does:**
- Counts G and C nucleotides per line
- Calculates percentage
- Outputs one value per sequence

**Example transformation:**
```
Input:  A T C G A T C G
Output: 50.00
```

---

#### Features

- **Batch processing:** Handles all 20 chromosomes automatically
- **Progress reporting:** Clear messages for each file and stage
- **Skip functionality:** Avoids regenerating existing files
- **Error handling:** Validates directory existence
- **Dependency management:** Ensures required scripts are accessible
- **Consistent naming:** Maintains filename conventions

#### Output Structure

For each input file `chrN.Build37.data`, creates three outputs:

```
data/mouse/
├── chrN.Build37.data     # Original (input)
├── chrN.Build37.snp      # Stage 1 output
├── chrN.Build37.codons   # Stage 2 output
└── chrN.Build37.cg       # Stage 3 output
```

**Total files after processing:**
- 20 original `.data` files
- 20 `.snp` files (SNP sequences)
- 20 `.codons` files (codon analysis)
- 20 `.cg` files (GC content)
- **Total: 80 files**

#### Performance

Processing time for all 20 chromosomes:
- **Typical runtime:** 5-15 minutes (depends on file sizes)
- **Bottleneck:** Python script processing (not disk I/O)
- **Memory usage:** Minimal (line-by-line processing)

#### Dependencies

**System utilities:**
- `bash` (shell)
- `cut` (text processing)

**Python scripts (must be in `scripts/` directory):**
- `codon_counter.py`
- `cg.py`
- `dna_ops.py`

---

## Jupyter Notebooks

### `problem-set-1.ipynb`

**Purpose:** Interactive analysis and visualization of mouse genome SNP data

**Location:** `notebooks/problem-set-1.ipynb`

#### Overview

This Jupyter notebook demonstrates the use of the `dna_ops` library for analyzing specific sequences from the mouse genome dataset. It provides examples of codon frequency analysis and GC content calculation with formatted output and summary statistics.

#### Structure

The notebook is organized into several cells:

##### 1. Introduction (Markdown)

Provides context about:
- Notebook purpose and goals
- Data source information
- Analysis methods overview
- Expected outcomes

##### 2. Setup & Data Loading (Code)

```python
import sys
sys.path.append('../scripts')
from dna_ops import clean_dna_sequence, count_codons, calculate_gc_content

# Read SNP file
with open('../data/mouse/chr1.Build37.snp', 'r') as f:
    lines = f.readlines()
```

**What it does:**
- Imports functions from the dna_ops library
- Loads entire SNP file into memory as list of lines
- Handles relative paths from notebooks/ subdirectory

##### 3. Codon Analysis - Line 3 (Code)

**Analysis performed:**
- Extracts the third line from chr1 SNP data
- Cleans the sequence
- Counts all codon frequencies
- Displays total and unique codon counts
- Shows top 10 most frequent codons

**Output format:**
```
Codon Counts for Line 3:
========================================
Total codons: 337
Unique codons: 62

Top 10 most frequent codons:
  AAA: 45
  GGG: 38
  AGA: 32
  ...
```

**Biological insights:**
- High codon diversity indicates complex genetic sequence
- Codon frequency patterns can reveal coding vs non-coding regions
- Abundance of certain codons reflects organism-specific usage bias

##### 4. GC Content Analysis - First 10 Lines (Code)

**Analysis performed:**
- Processes first 10 sequences from chr1
- Calculates GC percentage for each
- Displays results in tabular format
- Computes summary statistics (mean, min, max)

**Output format:**
```
GC Content for First 10 Lines:
========================================
Line   GC Content (%)
----------------------------------------
1      52.45%
2      48.32%
3      51.67%
...
========================================
Average GC content: 50.23%
Min GC content: 48.12%
Max GC content: 54.67%
```

**Biological insights:**
- Mouse genome average GC content: ~42%
- Values above 50% may indicate gene-rich regions
- Variation across samples reflects genomic diversity

#### Running the Notebook

**Prerequisites:**
1. Jupyter Notebook or JupyterLab installed
2. Project files in correct directory structure
3. SNP data files generated (via extract-mouse-ops.sh)

**Launch methods:**

```bash
# From project root directory
cd ~/Desktop/bin602/projects/U1-coding-environment

# Option 1: Jupyter Notebook
jupyter notebook

# Option 2: JupyterLab
jupyter lab

# Then open: notebooks/problem-set-1.ipynb
```

**Execution:**
- Click "Cell" → "Run All" to execute all cells
- Or press `Shift+Enter` on each cell individually

#### Customization Ideas

Extend the notebook with:

**Additional analyses:**
- Compare codon frequencies across chromosomes
- Plot GC content distribution histograms
- Identify regions with extreme GC content
- Analyze correlation between codon usage and GC content

**Visualization examples:**
```python
import matplotlib.pyplot as plt

# GC content histogram
plt.hist(gc_values, bins=20)
plt.xlabel('GC Content (%)')
plt.ylabel('Frequency')
plt.title('GC Content Distribution')
plt.show()

# Codon frequency bar chart
top_codons = sorted(codon_counts.items(), key=lambda x: -x[1])[:10]
codons, counts = zip(*top_codons)
plt.bar(codons, counts)
plt.xlabel('Codon')
plt.ylabel('Frequency')
plt.title('Top 10 Codons')
plt.show()
```

**Statistical analyses:**
- Standard deviation of GC content
- Coefficient of variation
- Codon usage entropy (measure of diversity)

---

## Installation & Setup

### System Requirements

- **Operating System:** Unix-like (Linux, macOS) or WSL on Windows
- **Python:** 3.7 or higher
- **Bash:** 4.0 or higher
- **Disk Space:** ~500 MB for data files
- **Memory:** 2 GB RAM minimum

### Quick Start

```bash
# 1. Clone or download the repository
cd ~/Desktop/bin602/projects
git clone <repository_url> U1-coding-environment
cd U1-coding-environment

# 2. Create directory structure
mkdir -p data/mouse notebooks scripts

# 3. Make scripts executable
chmod +x download-mouse-data.sh
chmod +x scripts/extract-mouse-ops.sh

# 4. Download data
./download-mouse-data.sh data/mouse

# 5. Process data
./scripts/extract-mouse-ops.sh data/mouse

# 6. Verify installation
python3 scripts/dna_ops.py  # Should output: ✓ All tests passed
ls data/mouse/*.snp | wc -l  # Should output: 20
```

### Detailed Setup

#### Step 1: Python Scripts

Place these files in `scripts/`:
- `dna_ops.py` (library)
- `codon_counter.py`
- `cg.py`
- `download-mouse-data.sh`
- `extract-mouse-ops.sh`

#### Step 2: Test Core Library

```bash
python3 scripts/dna_ops.py
```

Expected output:
```
✓ All tests passed
```

If tests fail, check:
- Python version (should be 3.7+)
- File permissions
- Syntax errors in dna_ops.py

#### Step 3: Download Sample Data

```bash
# Create data directory
mkdir -p data/mouse

# Download first chromosome only (for testing)
curl -o data/mouse/chr1.Build37.data \
  http://mtweb.cs.ucl.ac.uk/HSMICE/GENOTYPES/chr1.Build37.data
```

#### Step 4: Test Processing Pipeline

```bash
# Process single chromosome
cut -d' ' -f7- data/mouse/chr1.Build37.data > data/mouse/chr1.Build37.snp
python3 scripts/codon_counter.py < data/mouse/chr1.Build37.snp > data/mouse/chr1.Build37.codons
python3 scripts/cg.py < data/mouse/chr1.Build37.snp > data/mouse/chr1.Build37.cg

# Verify outputs
head -5 data/mouse/chr1.Build37.snp
head -5 data/mouse/chr1.Build37.codons
head -5 data/mouse/chr1.Build37.cg
```

#### Step 5: Full Dataset Processing

```bash
# Download all chromosomes
./download-mouse-data.sh data/mouse

# Process everything
./scripts/extract-mouse-ops.sh data/mouse

# Verify completion
ls data/mouse/ | wc -l  # Should be 80 (20 × 4 file types)
```

#### Step 6: Jupyter Setup (Optional)

```bash
# Install Jupyter (if not already installed)
pip3 install jupyter

# Launch notebook
cd ~/Desktop/bin602/projects/U1-coding-environment
jupyter notebook

# Open notebooks/problem-set-1.ipynb in browser
```

### Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'dna_ops'`

**Solution:**
```bash
# Ensure dna_ops.py is in scripts/
ls scripts/dna_ops.py

# Run Python from correct directory
cd ~/Desktop/bin602/projects/U1-coding-environment
python3 scripts/codon_counter.py  # Not from scripts/ directory
```

---

**Issue:** `FileNotFoundError: [Errno 2] No such file or directory: 'data/mouse/chr1.Build37.snp'`

**Solution:**
```bash
# Check if data directory exists
ls data/mouse/

# Verify .snp files were created
ls data/mouse/*.snp

# If missing, run extraction
cut -d' ' -f7- data/mouse/chr1.Build37.data > data/mouse/chr1.Build37.snp
```

---

**Issue:** Empty output files (0 bytes)

**Solution:**
```bash
# Check if source data exists and has content
ls -lh data/mouse/chr1.Build37.data
head -1 data/mouse/chr1.Build37.data

# Verify cut command works
cut -d' ' -f7- data/mouse/chr1.Build37.data | head -1

# Check Python scripts for errors
python3 scripts/codon_counter.py < /dev/null  # Should produce empty line, not error
```

---

**Issue:** Jupyter notebook can't import dna_ops

**Solution:**
```python
# In notebook, adjust path to go up from notebooks/
import sys
sys.path.append('../scripts')  # Use ../ not scripts/
from dna_ops import clean_dna_sequence
```

---

## Usage Examples

### Example 1: Process Single Chromosome

```bash
# Extract SNPs
cut -d' ' -f7- data/mouse/chr5.Build37.data > data/mouse/chr5.Build37.snp

# Analyze codons
python3 scripts/codon_counter.py < data/mouse/chr5.Build37.snp > data/mouse/chr5.Build37.codons

# Calculate GC content
python3 scripts/cg.py < data/mouse/chr5.Build37.snp > data/mouse/chr5.Build37.cg

# View results
head data/mouse/chr5.Build37.codons
head data/mouse/chr5.Build37.cg
```

---

### Example 2: Compare GC Content Across Chromosomes

```bash
# Calculate average GC content per chromosome
for i in {1..20}; do
    avg=$(awk '{sum+=$1; count++} END {print sum/count}' data/mouse/chr${i}.Build37.cg)
    echo "Chr $i: $avg%"
done > gc_summary.txt

# Find chromosome with highest GC content
sort -t: -k2 -rn gc_summary.txt | head -1
```

---

### Example 3: Extract Most Common Codons Genome-Wide

```bash
# Combine all codon files
cat data/mouse/chr*.Build37.codons > all_codons.txt

# Extract just the codon names (before colons)
grep -oP '\w{3}(?=:)' all_codons.txt | sort | uniq -c | sort -rn | head -20

# This shows the 20 most frequently appearing codons across all chromosomes
```

---

### Example 4: Custom Analysis with Python

```python
from scripts.dna_ops import clean_dna_sequence, count_codons, calculate_gc_content

# Read a sequence
with open('data/mouse/chr1.Build37.snp', 'r') as f:
    sequence = f.readline().strip()

# Clean and analyze
cleaned = clean_dna_sequence(sequence)
codons = count_codons(cleaned)
gc = calculate_gc_content(cleaned)

# Find most abundant codon
most_common = max(codons.items(), key=lambda x: x[1])
print(f"Most common codon: {most_common[0]} ({most_common[1]} occurrences)")
print(f"GC content: {gc:.2f}%")

# Calculate codon diversity (entropy)
import math
total = sum(codons.values())
entropy = -sum((count/total) * math.log2(count/total) for count in codons.values())
print(f"Codon diversity (entropy): {entropy:.2f} bits")
```

---

### Example 5: Batch Processing with Custom Filters

```bash
# Process only chromosomes 1-5
for i in {1..5}; do
    echo "Processing chr$i..."
    cut -d' ' -f7- data/mouse/chr${i}.Build37.data > data/mouse/chr${i}.Build37.snp
    python3 scripts/codon_counter.py < data/mouse/chr${i}.Build37.snp > data/mouse/chr${i}.Build37.codons
    python3 scripts/cg.py < data/mouse/chr${i}.Build37.snp > data/mouse/chr${i}.Build37.cg
done

# Or use the automated script with selective processing
# (modify extract-mouse-ops.sh to filter by chromosome number)
```

---

## Dependencies

### Required

**System utilities (standard Unix tools):**
- `bash` (>= 4.0) - Shell scripting
- `cut` - Text field extraction
- `curl` - File download
- `cat` - File concatenation
- `head` / `tail` - File preview

**Python (>= 3.7):**
- No external libraries required
- Uses only built-in modules: `sys`

### Optional

**For Jupyter notebooks:**
- `jupyter` - Interactive notebook interface
- `matplotlib` (optional) - Data visualization
- `pandas` (optional) - Data manipulation
- `numpy` (optional) - Numerical computing

**Installation:**
```bash
pip3 install jupyter matplotlib pandas numpy
```

### Compatibility

**Tested on:**
- macOS 12+ (Monterey and later)
- Ubuntu 20.04+ LTS
- Windows 10/11 with WSL2

**Python versions:**
- 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.14

**Known issues:**
- Windows (native): Bash scripts require Git Bash or WSL
- Python 2.x: Not supported (use Python 3.7+)

---

**Last Updated:** 11 December 2025