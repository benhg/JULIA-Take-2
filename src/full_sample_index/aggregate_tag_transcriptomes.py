"""
Input: A directory containing FASTA files. Each FASTA file's name has a sample ID in it.

Sample IDs 1-11 are from lane 1. Sample IDs 12-22 are from lane 2. 

Output1: A file of all the transcripts with tags added.
"""

from Bio import SeqIO
from glob import glob

source_dir = "/home/labs/binford/Assembled_Untranslated_Transcriptomes"
output_file = f"{source_dir}/all_assembled_transcriptomes.fasta"

global_file = []

# Merge everything into one big dict
for file in glob(f"{source_dir}/*.fasta"):
    if "all_assembled_transcriptomes" in file:
        continue
    sample_id = file.split("/")[-1].split(".fasta")[0]
    s_num = sample_id.split("s")[-1].split("_")[0]
    lane = 1 if int(s_num) < 12 else 2
    print(sample_id, lane)
    records = list(SeqIO.parse(file, "fasta"))
    for record in records:
        # edit ID
        record.id = f"{record.id} sample={sample_id} lane={lane}"
        global_file.append(record)

# Output to a new file
with open(output_file, "w") as output_handle:
    SeqIO.write(global_file, output_handle, "fasta")
