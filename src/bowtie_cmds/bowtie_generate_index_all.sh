#!/bin/bash
#SBATCH --cpus-per-task=48

bowtie2-build --large-index /home/labs/binford/Assembled_Untranslated_Transcriptomes/all_assembled_transcriptomes.fasta /home/labs/binford/all_untranslated_transcriptomes_index_lane_1