"""
Input: A directory containing FASTA files. Each FASTA file's name has a sample ID in it.

Sample IDs 1-11 are from lane 1. Sample IDs 12-22 are from lane 2. 

Output: A single FASTA file with all the sequences from the directory. Samples are tagged with both lane ID and sample ID
"""

from Bio import SeqIO
from glob import glob

source_dir = "/home/labs/binford/Assembled_Untranslated_Transcriptomes"
output_file = f"{source_dir}/all_assembled_transcriptomes.fasta"

for file in glob(f"{source_dir}/*.fasta"):
	print(file)