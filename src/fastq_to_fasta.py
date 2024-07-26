"""
The raw reads are in fastq format, but it'll be easier to deal with them in fasta format 
"""
from Bio import SeqIO
from glob import glob
import multiprocessing

source_dir = "/home/labs/binford/raw_reads"
out_dir = "/home/labs/binford/raw_reads_fasta"


def process_file(file):
    new_filename = file.replace("fastq", "fasta").replace(source_dir, out_dir)
    with open(file, "r") as old_handle, open(new_filename, "w") as new_handle:
        sequences = SeqIO.parse(old_handle, "fastq")
        count = SeqIO.write(sequences, new_handle, "fasta")
        print(f"extracted {count} sequences from {old_handle.split('/'[-1])}")

pool = multiprocessing.Pool()

work = pool.map(process_file, [file for file in glob(f"{source_dir}/*.fastq")])
