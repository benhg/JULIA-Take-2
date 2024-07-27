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
dest_dir = "/home/labs/binford/raw_reads_fasta_tagged/"

files = {
    "sprouts0": ["lane1-s001-indexRPI1-ATCACG-Drymusa_VG_S1_L001_R1_001.fasta", "lane2-s013-indexRPI13-AGTCAA-Phol_total_RNA_S13_L002_R2_001.fasta", "lane1-s001-indexRPI1-ATCACG-Drymusa_VG_S1_L001_R2_001.fasta", "lane2-s014-indexRPI14-AGTTCC-Plect_total_RNA_S14_L002_R1_001.fasta", "lane1-s002-indexRPI2-CGATGT-LAz1_VG_S2_L001_R1_001.fasta", "lane2-s014-indexRPI14-AGTTCC-Plect_total_RNA_S14_L002_R2_001.fasta", "lane1-s002-indexRPI2-CGATGT-LAz1_VG_S2_L001_R2_001.fasta", "lane2-s015-indexRPI15-ATGTCA-LrecVA_total_RNA_S15_L002_R1_001.fasta", "lane1-s003-indexRPI3-TTAGGC-LAz2_VG_S3_L001_R1_001.fasta", "lane2-s015-indexRPI15-ATGTCA-LrecVA_total_RNA_S15_L002_R2_001.fasta", "lane1-s003-indexRPI3-TTAGGC-LAz2_VG_S3_L001_R2_001.fasta", "lane2-s016-indexRPI16-CCGTCC-Arch_total_RNA_S16_L002_R1_001.fasta", "lane1-s004-indexRPI4-TGACCA-LAz3_VG_S4_L001_R1_001.fasta", "lane2-s016-indexRPI16-CCGTCC-Arch_total_RNA_S16_L002_R2_001.fasta", "lane1-s004-indexRPI4-TGACCA-LAz3_VG_S4_L001_R2_001.fasta", "lane2-s017-indexRPI17-GTAGAG-Arch_body_RNA_S17_L002_R1_001.fasta", "lane1-s005-indexRPI5-ACAGTG-Sic1_VG_S5_L001_R1_001.fasta", "lane2-s017-indexRPI17-GTAGAG-Arch_body_RNA_S17_L002_R2_001.fasta", "lane1-s005-indexRPI5-ACAGTG-Sic1_VG_S5_L001_R2_001.fasta", "lane2-s018-indexRPI18-GTCCGC-Scy_total_RNA_S18_L002_R1_001.fasta", "lane1-s006-indexRPI6-GCCAAT-Sic2_VG_S6_L001_R1_001.fasta", "lane2-s018-indexRPI18-GTCCGC-Scy_total_RNA_S18_L002_R2_001.fasta", "lane1-s006-indexRPI6-GCCAAT-Sic2_VG_S6_L001_R2_001.fasta", "lane2-s019-indexRPI19-GTGAAA-Sagunt_RNA_S19_L002_R1_001.fasta", "lane1-s007-indexRPI7-CAGATC-Sic3_VG_S7_L001_R1_001.fasta"],
    "sprouts": ["lane2-s019-indexRPI19-GTGAAA-Sagunt_RNA_S19_L002_R2_001.fasta", "lane1-s007-indexRPI7-CAGATC-Sic3_VG_S7_L001_R2_001.fasta", "lane2-s020-indexRPI20-GTGGCC-Lgroot_total_RNA_S20_L002_R1_001.fasta", "lane1-s008-indexRPI8-ACTTGA-MP1fe_S8_L001_R1_001.fasta", "lane2-s020-indexRPI20-GTGGCC-Lgroot_total_RNA_S20_L002_R2_001.fasta", "lane1-s008-indexRPI8-ACTTGA-MP1fe_S8_L001_R2_001.fasta", "lane2-s021-indexRPI22-CGTACG-MP2_WB_S21_L002_R1_001.fasta", "lane1-s009-indexRPI9-GATCAG-MP2fe_S9_L001_R1_001.fasta", "lane2-s021-indexRPI22-CGTACG-MP2_WB_S21_L002_R2_001.fasta", "lane1-s009-indexRPI9-GATCAG-MP2fe_S9_L001_R2_001.fasta", "lane2-s022-indexRPI23-GAGTGG-MP3_WB_S22_L002_R1_001.fasta", "lane1-s010-indexRPI10-TAGCTT-MP3fe_S10_L001_R1_001.fasta", "lane2-s022-indexRPI23-GAGTGG-MP3_WB_S22_L002_R2_001.fasta", "lane1-s010-indexRPI10-TAGCTT-MP3fe_S10_L001_R2_001.fasta", "l_arizonica_R1.fasta", "lane1-s011-indexRPI11-GGCTAC-MP1fe_WB_S11_L001_R1_001.fasta", "l_arizonica_R2.fasta", "lane1-s011-indexRPI11-GGCTAC-MP1fe_WB_S11_L001_R2_001.fasta", "periegops_R1.fasta", "lane2-s012-indexRPI12-CTTGTA-Periegop_Hine_VG_S12_L002_R1_001.fasta", "periegops_R2.fasta", "lane2-s012-indexRPI12-CTTGTA-Periegop_Hine_VG_S12_L002_R2_001.fasta", "sicarius_dolichocephalus_R1.fasta", "lane2-s013-indexRPI13-AGTCAA-Phol_total_RNA_S13_L002_R1_001.fasta", "sicarius_dolichocephalus_R2.fasta"]
}

def process_file(file):

    print(file)
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
            sequence.id = f"{sequence.id} sample={sample_id} lane={lane} {special}"
            all_sequences.append(sequence)

        count = SeqIO.write(all_sequences, new_handle, "fasta")
        print(f"extracted {count} sequences from {old_handle.split('/'[-1])}")


hostname = socket.gethostname()
pool = multiprocessing.Pool(2)
work = pool.map(process_file, [f"{source_dir}/{file}" for file in files[hostname]])

