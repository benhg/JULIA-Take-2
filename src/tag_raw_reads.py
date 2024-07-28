"""
This file aggregates and tags the known assembled transcriptomes.

Input: A directory containing FASTA files. Each FASTA file's name has a sample ID in it.

Sample IDs 1-11 are from lane 1. Sample IDs 12-22 are from lane 2. 

Output 1: A directory containing tagged fasta files 

Output 2: A single FASTA file with all the sequences from the directory. Samples are tagged with both lane ID and sample ID
"""

from Bio import SeqIO
from glob import glob
import multiprocessing
import socket

source_dir = "/home/labs/binford/raw_reads_fasta/"
dest_dir = "/home/labs/binford/raw_reads_fasta_tagged_batched/"


def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.Align.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    batch = []
    for entry in iterator:
        batch.append(entry)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def process_file(file):
    """
    Operate on batches of 10k lines at a time to avoid memory exhaustion
    """
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

    with open(file, "r") as old_handle:
        record_iter = SeqIO.parse(old_handle, "fasta")

        for i, batch in enumerate(batch_iterator(record_iter, 100000)):
            all_sequences = []
            batch_filename = f"{new_filename}_%i.fasta" % (i + 1)
            new_handle = open(batch_filename, "w")

            for sequence in batch:
                sequence.id = f"{sequence.id} sample={sample_id} lane={lane} {special}"
                all_sequences.append(sequence)

            count = SeqIO.write(all_sequences, new_handle, "fasta")
            print(f"extracted {count} sequences from {file.split('/')[-1]} into batch {i}")
            new_handle.close()


pool = multiprocessing.Pool(48)
work = pool.map(process_file, [f"{file}" for file in glob(f"{source_dir}/*.fasta")])

