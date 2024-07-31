#!/bin/bash
#SBATCH --cpus-per-task=48

bowtie2-build -p 48 --large-index /home/labs/binford/Assembled_Untranslated_Transcriptomes/all_assembled_transcriptomes_lane_2.fasta /home/labs/binford/all_untranslated_transcriptomes_index_lane_2