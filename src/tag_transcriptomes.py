"""
This file aggregates and tags the known assembled transcriptomes.

Input: A directory containing FASTA files. Each FASTA file's name has a sample ID in it.

Sample IDs 1-11 are from lane 1. Sample IDs 12-22 are from lane 2. 

Output: A single FASTA file with all the sequences from the directory. Samples are tagged with both lane ID and sample ID
"""

from Bio import SeqIO
from glob import glob
import multiprocessing
import resource

source_dir = "/home/labs/binford/raw_reads_fasta"
dest_dir = "/home/labs/binford/raw_reads_fasta_tagged"


def process_file(file):

    # Set the limit to (500 GiB/48 processes)
    all_sequences = []
    new_filename = file.replace(source_dir, dest_dir)
    lane = "N/A"
    sample_id = "N/A"
    special = ""
    if "lane1" in file:
        lane = "1"
    elif "lane2" in file:
        lane = "2"
    else:
        special += file.split(".fasta")[0].split("/")[-1]

    # All files with "laneX" have a sample ID
    if "lane" in new_filename:
        sample_id = f"{new_filename.split('-')[1]}_Trinity"

    #print(lane, sample_id, special)

    with open(file, "r") as old_handle, open(new_filename, "w") as new_handle:
        sequences = list(SeqIO.parse(old_handle, "fasta"))
        for sequence in sequences:
            print(sequence.id)
            sequence.id = f"{sequence.id} sample={sample_id} lane={lane} {special}"
            print(sequence.id)
            all_sequences.append(sequence)

        count = SeqIO.write(all_sequences, new_handle, "fasta")
        print(f"extracted {count} sequences from {old_handle.split('/'[-1])}")
    
pool = multiprocessing.Pool(1)
work = pool.map(process_file, [file for file in glob(f"{source_dir}/*.fasta")])

