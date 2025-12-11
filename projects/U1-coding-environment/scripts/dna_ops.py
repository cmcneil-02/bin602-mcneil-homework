"""
dna_ops.py - DNA sequence operations library
Author: Collin McNeil
Course: BIN602 - Data Mining for Bioinformatics
Date: 12-10-2024
"""


def clean_dna_sequence(dna_string):
    """Clean DNA: replace NA with _, remove spaces, uppercase."""
    return dna_string.replace('NA', '_').replace(' ', '').upper()


def count_codons(dna_sequence):
    """Count non-overlapping 3-nucleutide codons."""
    codon_dict = {}
    for i in range(0, len(dna_sequence) -2, 3):
        codon = dna_sequence[i:i+3]
        if len(codon) == 3:
            codon_dict[codon] = codon_dict.get(codon, 0) + 1
    return codon_dict


def calculate_gc_content(dna_sequence):
    """Calculate GC content as percentage (0-100)."""
    if len(dna_sequence) == 0:
        return 0.0
    gc_count = dna_sequence.count('C') + dna_sequence.count ('G')
    return (gc_count / len(dna_sequence)) * 100


# Unit tests
if __name__ == "__main__":
    assert clean_dna_sequence("a t g NA c g") == "ATG_CG"
    assert count_codons("ATGATGCCC") == {'ATG': 2, 'CCC': 1}
    assert calculate_gc_content("ATCGATCG") == 50.0
    assert calculate_gc_content("AAAA") == 0.0
    print("All tests passed.")
