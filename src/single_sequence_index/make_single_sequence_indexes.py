"""
Make separate bowtie indexes for each sequence

They'll go into /home/labs/binford//home/labs/binford/taxon_confirmation_indexes/{NAME}/
"""

import subprocess
from Bio import SeqIO

base_dir = "/home/labs/binford/taxon_confirmation_indexes/"

sbatch_template = """#!/bin/bash
#SBATCH --cpus-per-task=48

mkdir -p /home/labs/binford/taxon_confirmation_indexes/{}_index
chmod 777 /home/labs/binford/taxon_confirmation_indexes/{}_index

bowtie2-build --threads 48 --small-index /home/labs/binford/taxon_confirmation_indexes/{}.fasta /home/labs/binford/taxon_confirmation_indexes/{}_index/{}_index
"""

## First, turn each sequence in the fasta file into its own fasta file
with open(file, "data/all_sequences.fasta") as old_handle:
    sequences = SeqIO.parse(old_handle, "fasta")
    for record in sequences:
        with open(f"{base_dir}/{record.id}.fasta", "w") as new_file:
            new_file.write(f">{record.id}")
            new_file.write(f"{record.sequence}")

    


## Then, submit a bunch of indexing jobs to make indexes
"""
for i in range(1, 23):
    sample_id = str(i).zfill(3)
    sbatch_text = sbatch_template.format(sample_id, sample_id, sample_id,
                                         sample_id, sample_id)
    with open(f"bowtie_cmds/gen_index_s{sample_id}.sh", "w") as fh:
        fh.write(sbatch_text)
    print(
        subprocess.check_output(
            f"sbatch /home/glick/JULIA-Take-2/src/bowtie_cmds/gen_index_s{sample_id}.sh",
            shell=True))
"""

