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
                index_id = str().zfill(3)
                reads_sample_id = str(j).zfill(3)

            print(reads_sample_id, index_id)
            q += 1 


            #print(f"{combined_files_dir}/lane{lane}-s{index_id}*R1*")
            dir_1_filename = glob(f"{combined_files_dir}/lane{lane}-s{reads_sample_id}*R1*")[0]
            #print(dir_1_filename)
            dir_2_filename = dir_1_filename.replace("R1", "R2")

            sbatch_text = sbatch_template.format(index_id, index_id, dir_1_filename, dir_2_filename, index_id, index_id, reads_sample_id)
            #print(dir_1_filename, dir_2_filename, index_id)
            with open(f"bowtie_cmds/gen_index_{index_id}_s{reads_sample_id}.sh", "w") as fh:
                fh.write(sbatch_text)
            print(subprocess.check_output(f"sbatch bowtie_cmds/gen_index_{reads_sample_id}_s{reads_sample_id}.sh", shell=True))

## Special Cases
## Please run s001 raw reads against s012 transcripts, and s021 raw reads against s005

## S001 against s012
dir_1_filename = glob(f"{combined_files_dir}/lane1-s001*R1*")[0]
dir_2_filename = dir_1_filename.replace("R1", "R2")

sbatch_text = sbatch_template.format("012", "012", dir_1_filename, dir_2_filename, "012", "012", "001")
with open(f"bowtie_cmds/gen_index_012_001s.sh", "w") as fh:
    fh.write(sbatch_text)
    print(subprocess.check_output(f"sbatch bowtie_cmds/gen_index_012_001s.sh", shell=True))


## S021 against s005 
dir_1_filename = glob(f"{combined_files_dir}/lane2-s021*R1*")[0]
dir_2_filename = dir_1_filename.replace("R1", "R2")

sbatch_text = sbatch_template.format("005", "005", dir_1_filename, dir_2_filename, "005", "005", "021")
with open(f"bowtie_cmds/gen_index_012_001s.sh", "w") as fh:
    fh.write(sbatch_text)
    print(subprocess.check_output(f"sbatch bowtie_cmds/gen_index_012_001s.sh", shell=True))
