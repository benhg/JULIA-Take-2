"""
Make separate bowtie indexes for each sample

They'll go into /home/labs/binford/single_sample_indexes/s_{XYZ}/
"""

import subprocess
from glob import glob

combined_files_dir = "/home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/"

sbatch_template = """#!/bin/bash
#SBATCH --cpus-per-task=48


bowtie2 -f --threads 48 -x /home/labs/binford/single_sample_indexes/s{}_index/s{}_index -1 {} -2 {} > /home/labs/binford/single_sample_indexes/s{}_index/index_{}_read_s{}.sam
"""

# For each lane
for lane in range(1,3):
    # For each sample in lane
    for i in range(1,12):
        # For each set of raw reads
        for j in range(1, 12):

            if lane == 2:
                index_id = str(i + 11).zfill(3)
                reads_sample_id = str(j).zfill(3)
            else:
                index_id = str(i + 11).zfill(3)
                reads_sample_id = str(j).zfill(3)

            print(reads_sample_id, index_id)


            print(f"{combined_files_dir}/lane{lane}-s{index_id}*R1*")
            dir_1_filename = glob(f"{combined_files_dir}/lane{lane}-s{reads_sample_id}*R1*")
            print(dir_1_filename)
            dir_1_filename = glob(f"{combined_files_dir}/lane{lane}-s{reads_sample_id}*R1*")[0]
            dir_2_filename = dir_1_filename.replace("R1", "R2")

            sbatch_text = sbatch_template.format(index_id, index_id, dir_1_filename, dir_2_filename, index_id, index_id, reads_sample_id)
            print(dir_1_filename, dir_2_filename, index_id)
            # with open(f"bowtie_cmds/gen_index_{reads_sample_id}_s{reads_sample_id}.sh", "w") as fh:
            #     fh.write(sbatch_text)
            # print(subprocess.check_output(f"sbatch bowtie_cmds/gen_index_{reads_sample_id}_s{reads_sample_id}.sh", shell=True))

## Special Cases