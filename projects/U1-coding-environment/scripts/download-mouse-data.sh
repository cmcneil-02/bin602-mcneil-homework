#!/bin/bash
    # File: download_mouse_data.sh
    # Author: Hank Feild
        # Transcribed by: Collin McNeil
    # Course: BIN602 - Data Mining for Bioinformatics
    # Date: 12-11-2025
    # Purpose: Downloads the files chr1.Build37.data -- chr20.Build37.data from
    #   http://mtweb.cs.ucl.ac.uk/HSMICE/GENOTYPES/


if [[ $# -lt 1 || "$1" == '-h' ]]; then
    echo "USAGE: ./download-mouse-data.sh <dest directory> [--skip ]"
    echo "Including --skip will cause destination files already downloaded to be skipped."
    exit
fi

destDir="$1"
skipExisting=0

# Check if user wants to skip existing files
if [[ $# -gt 1 && "$2" == "--skip" ]]; then
    skipExisting=1
fi

# Ensure that destination directory exists and is a directory
if [[ ! -d "$destDir" ]]; then
    echo "ERROR: $destDir is not a directory!"
    exit
fi

# Download all the files
for i in {1..20}; do
    filename="chr${i}.Build37.data"
    if [[ $skipExisting -eq 1 && -f "$destDir/$filename" ]]; then
        echo "Skipping existing file $filename ..."
        continue
    else
    echo "Downloading $filename to $destDir ..."
    curl -o "$destDir/$filename" http://mtweb.cs.ucl.ac.uk/HSMICE/GENOTYPES/$filename
    sleep .5
    fi
    done