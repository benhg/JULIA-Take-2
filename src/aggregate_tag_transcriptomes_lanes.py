"""
Input: A directory containing FASTA files. Each FASTA file's name has a sample ID in it.

Sample IDs 1-11 are from lane 1. Sample IDs 12-22 are from lane 2. 

Output1: Two files, each with the reads from one lane.
"""

from Bio import SeqIO
from glob import glob

source_dir = "/home/labs/binford/Assembled_Untranslated_Transcriptomes"

global_file_lane_1 = []
global_file_lane_2 = []

# Merge everything into one big dict
for file in glob(f"{source_dir}/*.fasta"):
    if "all_assembled_transcriptomes" in file:
        pass
    sample_id = file.split("/")[-1].split(".fasta")[0]
    s_num = sample_id.split("s")[-1].split("_")[0]
    lane = 1 if int(s_num) < 12 else 2
    print(sample_id, lane)
    records = list(SeqIO.parse(file, "fasta"))
    for record in records:
        # edit ID
        record.id = f"{record.id} sample={sample_id} lane={lane}"
        if lane == 1:
            global_file_lane_1.append(record)
        elif lane == 2:
            global_file_lane_2.append(record)
        else:
            print("Unknown lane.......")

# Output to new files
with open(f"{source_dir}/all_assembled_transcriptomes_lane_1.fasta", "w") as output_handle:
    SeqIO.write(global_file_lane_1, output_handle, "fasta")

with open(f"{source_dir}/all_assembled_transcriptomes_lane_2.fasta", "w") as output_handle:
    SeqIO.write(global_file_lane_2, output_handle, "fasta")

