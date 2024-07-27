"""
This file aggregates and tags the known assembled transcriptomes.

Input: A directory containing FASTA files. Each FASTA file's name has a sample ID in it.

Sample IDs 1-11 are from lane 1. Sample IDs 12-22 are from lane 2. 

Output: A single FASTA file with all the sequences from the directory. Samples are tagged with both lane ID and sample ID
"""

from Bio import SeqIO
from glob import glob
import multiprocessing

source_dir = "/home/labs/binford/raw_reads_fasta"


def process_file(file):
    new_filename = file
    lane = "N/A"
    sample_id = "N/A"
    if "lane1" in file:
        lane = "1"
    elif "lane2" in file:
        lane = "2"

    # All files with "laneX" have a sample ID
    if "lane" in new_filename:
        sample_id = f"{new_filename.split('-')[1]}_Trinity"

    with open(file, "r") as old_handle, open(new_filename, "w") as new_handle:
        sequences = SeqIO.parse(old_handle, "fastq")
        for sequence in sequences:
            sequence.id = f"{record.id} sample={sample_id} lane={lane}"

        count = SeqIO.write(sequences, new_handle, "fasta")
        print(f"extracted {count} sequences from {old_handle.split('/'[-1])}")

pool = multiprocessing.Pool()
work = pool.map(process_file, [file for file in glob(f"{source_dir}/*.fasta")])

