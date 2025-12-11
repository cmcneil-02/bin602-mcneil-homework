"""
cg.py

Calculates the GC content (percentage of G and C nucleotides) in DNA sequences.
Reads DNA sequences from stdin, cleans them, and outputs the GC content percentage.

Author: Collin McNeil
Course: BIN602 - Data Mining for Bioinformatics
Date: 12-10-2024
"""

import sys
from dna_ops import clean_dna_sequence, calculate_gc_content


def main():
    for line in sys.stdin:
        cleaned = clean_dna_sequence(line.rstrip('\n'))
        gc_content = calculate_gc_content(cleaned)
        print(f"{gc_content:.2f}")


if __name__ == "__main__":
    main()