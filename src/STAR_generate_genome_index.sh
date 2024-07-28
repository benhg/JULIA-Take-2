#!/bin/bash
#SBATCH --cpus-per-task=48

/home/glick/STAR/bin/Linux_x86_64/STAR --runThreadN 48 --runMode genomeGenerate \
--genomeDir /home/labs/binford/all_transcriptomes_genome_dir \
--genomeFastaFiles /home/labs/binford/Assembled_Untranslated_Transcriptomes/all_assembled_transcriptomes.fasta \
--limitGenomeGenerateRAM=322122547200