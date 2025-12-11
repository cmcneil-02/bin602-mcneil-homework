"""
codon_counter.py

Analyzes DNA sequences to count codon frequencies.
Reads DNA sequences from stdin, cleans them, and outputs the three most frequent non-overlapping codons with their proportions.

Author: Collin McNeil
Course: BIN602 - Data Mining for Bioinformatics
Date: 12-10-2025
"""

import sys
from dna_ops import clean_dna_sequence, count_codons


def main():
    for line in sys.stdin:
        cleaned = clean_dna_sequence(line.strip('\n'))
        codons = count_codons(cleaned)

        total = sum(codons.values())
        if total == 0:
            print("")
            continue

        top_three = sorted(codons.items(), key = lambda x: (-x[1], x[0]))[:3]
        output = " ".join(f"{codon}:{count/total:.2f}" for codon, count in top_three)
        print(output)


if __name__ == "__main__":
    main()