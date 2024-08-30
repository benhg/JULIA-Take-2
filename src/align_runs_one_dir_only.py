"""
Make separate bowtie indexes for each sample

They'll go into /home/labs/binford/single_sample_indexes/s_{XYZ}/
"""

import subprocess
from glob import glob
import time

combined_files_dir = "/home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/"

sbatch_template = """#!/bin/bash
#SBATCH --cpus-per-task=48

echo "index_s{} read_s{}"

bowtie2 -f --threads 48 -x /home/labs/binford/single_sample_indexes/s{}_index/s{}_index -U {} > /home/labs/binford/single_sample_indexes/s{}_index/index_{}_read_s{}.sam
"""

def run_alignment(reads_sample_id, index_id):
    if int(reads_sample_id.split("s")[1]) <= 11:
        lane = 1
    else:
        lane = 2

    print(lane)

    #print(f"{combined_files_dir}/lane{lane}-s{index_id}*R1*")
    dir_1_filename = glob(f"{combined_files_dir}/lane{lane}-s{reads_sample_id}*R1*")[0]
    #print(dir_1_filename)
    dir_2_filename = dir_1_filename.replace("R1", "R2")
    job_filename = f"bowtie_cmds/unpaired_align_{index_id}_s{reads_sample_id}.sh"
    print(dir_1_filename)

    sbatch_text = sbatch_template.format(index_id, reads_sample_id, index_id, index_id, dir_1_filename, index_id, index_id, reads_sample_id)
    print(dir_1_filename, dir_2_filename, index_id, reads_sample_id)
    with open(job_filename, "w") as fh:
        fh.write(sbatch_text)
    time.sleep(0.1)
    print(subprocess.check_output(f"sbatch {job_filename}", shell=True))


def run_all_intra_lane_samples():
    # For each lane
    q = 0
    for lane in range(1,3):
        # For each sample in lane
        for i in range(1,12):
            # For each set of raw reads
            for j in range(1, 12):


                if lane == 2:
                    index_id = str(i + 11).zfill(3)
                    reads_sample_id = str(j + 11).zfill(3)
                else:
                    index_id = str(i).zfill(3)
                    reads_sample_id = str(j).zfill(3)

                print(reads_sample_id, index_id)
                q += 1

                run_alignment(reads_sample_id, index_id)


pairs_to_run = [["s016", "s005"], ["s005", "s016"], ["s022", "s008"], ["s008", "s022"], 
["s011", "s021"],
["s021", "s011"],
["s016", "s001"],
["s001", "s016"],
["s016", "s004"],
["s004", "s016"],
["s018", "s004"],
["s004", "s018"],
["s012", "s008"],
["s008", "s012"],
["s019", "s008"],
["s008", "s019"]
]

for pair in pairs_to_run:
    run_alignment(pair[0], pair[1])