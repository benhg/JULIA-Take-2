#!/bin/bash
#SBATCH --cpus-per-task=48

# NOTE: Job 1729 on Bacon is lane1

bowtie2 -f --threads 48 -x /home/labs/binford/all_untranslated_transcriptomes_index_lane_1/all_untranslated_transcriptomes_index_lane_1 -1 /home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane1_R1.fasta -2 /home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane1_R2.fasta