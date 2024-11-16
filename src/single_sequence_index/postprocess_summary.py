"""
Postprocess the summary to extract and apply the thresholding we talked about
"""
from glob import glob
import csv
import subprocess
import sys

sample_to_taxon = {
    "s001": "Drymusa_serrana",
    "s002": "Loxo_arizonica",
    "s003": "Loxo_arizonica",
    "s004": "Loxo_arizonica",
    "s005": "Hexophthalma",
    "s006": "Hexophthalma",
    "s007": "Hexophthalma",
    "s008": "Periegops_MP_VG",
    "s009": "Periegops_MP_VG",
    "s010": "Periegops_MP_VG",
    "s011": "Periegops_MP_WB",
    "s012": "Periegops_VG_H",
    "s013": "Physocyclus",
    "s014": "Plectreurys",
    "s015": "Loxo_reclusa",
    "s016": "Zephryarchea",
    "s017": "Zephryarchea",
    "s018": "Scytodes",
    "s019": "Loxo_rufescens",
    "s020": "Loxo_spinulosa",
    "s021": "Periegops_MP_WB",
    "s022": "Periegops_MP_WB",
    "c74742": "Loxo_spinulosa",
    "c49446": "Scytodes"
}

# Handles variations like WB vs VG
sample_to_taxon_short = {
    "s001": "Drymusa_serrana",
    "s002": "Loxo_arizonica",
    "s003": "Loxo_arizonica",
    "s004": "Loxo_arizonica",
    "s005": "Hexophthalma",
    "s006": "Hexophthalma",
    "s007": "Hexophthalma",
    "s008": "Periegops",
    "s009": "Periegops",
    "s010": "Periegops",
    "s011": "Periegops",
    "s012": "Periegops",
    "s013": "Physocyclus",
    "s014": "Plectreurys",
    "s015": "Loxo_reclusa",
    "s016": "Zephryarchea",
    "s017": "Zephryarchea",
    "s018": "Scytodes",
    "s019": "Loxo_rufescens",
    "s020": "Loxo_spinulosa",
    "s021": "Periegops",
    "s022": "Periegops",
    "c74742": "Loxo_spinulosa",
    "c49446": "Scytodes"
}

# Collected from
# f'bowtie2-inspect --large-index /home/labs/binford/single_sample_indexes/{index_sample}_index/{index_sample}_index
# see get_sizes.py
sample_to_transcript_count = {
    "s001": 146829,
    "s002": 165083,
    "s003": 176396,
    "s004": 177026,
    "s005": 178906,
    "s006": 136577,
    "s007": 157499,
    "s008": 143469,
    "s009": 167627,
    "s010": 183810,
    "s011": 191292,
    "s012": 167942,
    "s013": 223989,
    "s014": 229674,
    "s015": 196020,
    "s016": 161846,
    "s017": 292600,
    "s018": 148310,
    "s019": 191686,
    "s020": 167585,
    "s021": 245515,
    "s022": 170940,
    "c74742": 167585,
    "c49446": 148310
}


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode(sys.stdout.encoding)


headers = [
    "reads_sample", "reads_taxon", "index_sample", "index_taxon", "num_reads",
    "num_transcripts", "pairtype", "num_aligned_none", "num_aligned_once",
    "num_aligned_multiple", "none_alignment_rate", "single_alignment_rate",
    "multiple_alignment_rate", "num_aligned_any", "alignment_rate",
    "reads_per_transcript_none", "reads_per_transcript_one",
    "reads_per_transcript_multiple", "reads_per_transcript_any", "exec_time"
]

input_file = "/home/labs/binford/taxon_confirmation_indexes/summary.csv"
output_file = "/home/labs/binford/taxon_confirmation_indexes/summary.csv"

def hopper_threshold(value):
    """
    Take a value, and return the "hopperness" associated with this value
    """
    if value <= 1:
        return "LIKELY_HOPPER"
    elif value < 10:
        return "MAYBE_HOPPER"
    else:
        return "NOT_HOPPER"

index_to_rows = {}

with open(input_file, 'r') as f:
    reader = csv.DictReader(f, fieldnames =headers)

for row in reader:
    existing_entry = index_to_rows.get(row["index_sample"], {})
    existing_entry[row["index_sample"]] = row


for group in index_to_rows.values():
    print(group)
    for row in group:
        pass
