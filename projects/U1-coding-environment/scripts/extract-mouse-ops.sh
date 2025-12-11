#!/bin/bash
# File: extract-mouse-ops.sh
# Author: Collin McNeil
# Course: BIN602 - Data Mining for Bioinformatics
# Date: 12-11-2025
# Purpose: Process mouse genotype data files through problem 2, 3, and 4 scripts.
#    - Problem 2: Extract SNP columns (.data -> .snp)
#    - Problem 3: Count codons (.snp -> .codon_counts)
#    - Problem 4: Calculate GC content (.snp -> .cg)

if [[ $# -lt 1 || "$1" == '-h' ]]; then
    echo "USAGE: ./extract-mouse-ops.sh <data directory> [--skip]"
    echo "Including --skip will cause existing output files to be skipped."
    exit
fi

dataDir="$1"
skipExisting=0

if [[ $# -gt 1 && "$2" == "--skip" ]]; then
    skipExisting=1
fi

if [[ ! -d "$dataDir" ]]; then
    echo "ERROR: $dataDir is not a directory!"
    exit
fi

# Process all .data files
for dataFile in "$dataDir"/chr*.Build37.data; do
    baseName="${dataFile%.data}"
    
    echo "Processing $(basename "$dataFile")..."
    
    # Problem 2: Extract SNP columns
    snpFile="${baseName}.snp"
    if [[ $skipExisting -eq 1 && -f "$snpFile" ]]; then
        echo "  Skipping $(basename "$snpFile")"
    else
        echo "  Creating $(basename "$snpFile")..."
        cut -d' ' -f7- "$dataFile" > "$snpFile"
    fi
    
    # Problem 3: Count codons
    codonsFile="${baseName}.codons"
    if [[ $skipExisting -eq 1 && -f "$codonsFile" ]]; then
        echo "  Skipping $(basename "$codonsFile")"
    else
        echo "  Creating $(basename "$codonsFile")..."
        python3 scripts/codon_counter.py < "$snpFile" > "$codonsFile"
    fi
    
    # Problem 4: Calculate GC content
    cgFile="${baseName}.cg"
    if [[ $skipExisting -eq 1 && -f "$cgFile" ]]; then
        echo "  Skipping $(basename "$cgFile")"
    else
        echo "  Creating $(basename "$cgFile")..."
        python3 scripts/cg.py < "$snpFile" > "$cgFile"
    fi
    
    echo ""
done

echo "All files processed!"