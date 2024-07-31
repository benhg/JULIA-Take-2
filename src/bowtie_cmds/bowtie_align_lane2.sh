#!/bin/bash
#SBATCH --cpus-per-task=48

bowtie2 -f --threads 48 -x /home/labs/binford/all_untranslated_transcriptomes_index_lane_2/all_untranslated_transcriptomes_index_lane_2 -1 /home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane2_R1.fasta -2 /home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane2_R2.fasta