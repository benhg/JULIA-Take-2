"""
Make separate bowtie indexes for each sample

They'll go into /home/labs/binford/single_sample_indexes/s_{XYZ}/
"""

import subprocess

sbatch_template = """
#!/bin/bash
#SBATCH --cpus-per-task=48

mkdir -p /home/labs/binford/single_sample_indexes/s{}

bowtie2-build --threads 48 --large-index /home/labs/binford/Assembled_Untranslated_Transcriptomes/s{}_Trinity.fasta /home/labs/binford/single_sample_indexes/s{}_index/s{}_index
"""

for i in range(1,23):
    sample_id = str(i).zfill(3)
    sbatch_text = sbatch_template.format(sample_id, sample_id, sample_id, sample_id)
    with open(f"bowtie_cmds/gen_index_s{sample_id}.sh", "w") as fh:
        fh.write(sbatch_text)
    print(subprocess.check_output(f"sbatch /home/glick/JULIA-Take-2/src/bowtie_cmds/gen_index_s{sample_id}.sh"))