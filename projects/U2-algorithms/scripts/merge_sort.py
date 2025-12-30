"""
Merge Sort Implementation
Based on Ch. 7.1 of "An Introduction of Bioinformatics Algorithms"

This script implements merge sort to sort lines from an input file,
following the MERGE and MERGESORT algorithms from the textbook.

Author: Collin McNeil
Course: BIN602 - Data Mining for Bioinformatics
Date: 12-30-2024

Usage:
    python3 merge_sort.py input.txt output.txt # Save to file
    python3 merge_sort.py input.txt            # Print to stdout
"""

import sys


def merge(a, b):
    """
    MERGE algorithm from textbook (Ch. 7.1)
    Merges two sorted lists into a single sorted list.

    Parameters:
        a (list): First sorted list of length n1.
        b (list): Second sorted list of length n2.

    Returns:
        list: Merged sorted list of length n1 + n2.
    """
    n1 = len(a)
    n2 = len(b)

    # Create output list c
    c = [None] * (n1 + n2)

    # Add sentinel values (use None as sentinel for strings)
    # Handle this with explicit boundary checks
    i = 0 # Index for list a (1-indexed in textbook, 0-indexed here)
    j = 0 # Index for list b

    # Merge elements from a and b into c
    for k in range(n1 + n2):
        # Handle boundary conditions
        if i >= n1:
            # All elements from a have been used
            c[k] = b[j]
            j += 1
        elif j >= n2:
            # All elements from b have been used
            c[k] = a[i]
            i += 1
        elif a[i] <= b[j]:
            # Element from a is smaller
            c[k] = a[i]
            i += 1
        else:
            # Element from b is smaller
            c[k] = b[j]
            j += 1

    return c


def mergesort(c):
    """
    MERGESORT algorithm from textbook (Ch 7.1)
    Recursively sorts a list using divide-and-conquer.

    Parameters:
        c (list): The list to sort

    Returns:
        list: A new sorted list
    """
    n = len(c)

    # Base case: a list of size 1 is already sorted
    if n == 1:
        return c
    
    # Divide phase: split list into two halves
    mid = n // 2
    left = c[:mid]  # First n/2 elements
    right = c[mid:] # Last n/2 elements

    # Recursively sort each half
    sorted_left = mergesort(left)
    sorted_right = mergesort(right)

    # Conquer phase: merge the two sorted halves
    sorted_list = merge(sorted_left, sorted_right)

    return sorted_list


def main():
    """
    Main function to handle command line arguments and file I/O.
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 merge_sort.py input.txt [output.txt]", file=sys.stderr)
        print("  input.txt  - file containing lines to sort", file=sys.stderr)
        print("  output.txt - (optional) file to write sorted lines to", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Read input file
    try:
        with open(input_file, 'r') as f:
                lines = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle empty file or single line (base case)
    if len(lines) == 0:
        sorted_lines = []
    elif len(lines) == 1:
        sorted_lines = lines
    else:
        # Sort lines using MERGESORT
        sorted_lines = mergesort(lines)

    # Output results
    if output_file:
        # Write to output file
        try:
            with open(output_file, 'w') as f:
                for line in sorted_lines:
                    f.write(line + '\n')
            print(f"Sorted output written to '{output_file}'")
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to stdout
        for line in sorted_lines:
            print(line)


if __name__ == "__main__":
    main()