# Unit 1 - Coding Environments

# Contents

  * `README.md` -- This file.
  * `data` -- contains mouse genome file(s).
  * `notebooks` -- Jupyter notebooks exploring the data.
  * `scripts` -- Scripts for processing the data.

# Data Exploration

# Key Scripts

## `dna_ops.py`

### Overview

This solution consolidates all DNA sequence operation functions in a single library module (`dna_ops.py`) and refactors the original scripts to import and use this library.

### Library Module: `dna_ops.py`

#### Functions Included:

1. **`clean_dna_sequence(dna_string)`**
  - Replaces 'NA' with '_'
  - Removes spaces
  - Normalizes to uppercase
  - Used by: codon_counter.py, cg.py

2. **`count_codons(dna_sequence)`**
  - Counts non-overlapping 3-nucleotide codons
  - Returns dictionary of codon frequencies
  - Used by: codon_counter.py

3. **`calculate_gc_content(dna_sequence)`**
  - Calculates percentage of G and C nucleutides
  - Returns float (0-100)
  - Used by: cg.py

#### Unit Tests

The library includes built-in unit tests that can be run with:
```bash
python3 scripts/dna_ops.py
```

### Refactored Scripts
  - **Before**: many lines with function definitions
  - **After**: fewer lines, imports from dna_ops
  - **Imports**: `clean_dna_sequence`, `count_codons`, `calculate_gc_content`

### Testing

All scripts have been tested and work identically to their original versions:

```bash
# Test codon_counter.py
cat data/mosue/chr1.Build37.snp | python3 scripts/codon_counter.py > data/mouse/chr1.Build37.codons
head -5 data/mouse chr1.Build37.codons

# Test cg.py
cat data/mouse/chr1.Build.snp | python3 scripts/cg.py > data/mouse/chr1.Build37.cg
head -5 data/mouse/chr1.Build37.cg

# Test library
python3 scripts/dna_ops.py
```

### Usage Examples

#### Using the library in a new script:

```python
from dna_ops import clean_dna_sequence, count_codons, calculate_gc_content

# Clean a sequence
cleaned = clean_dna_sequence("a t g NA c g")
# Result: "ATG_CG"

# Count codons
codons = count_codons("ATGATGCCC")
# Result: {'ATG': 2, 'CCC': 1}

# Calculate GC content
gc = calculate_gc_content("ATCGATCG")
# Result: 50.0
```

# Dependencies