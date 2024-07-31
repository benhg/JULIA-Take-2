#!/bin/bash
#SBATCH --cpus-per-task=48

bowtie2-build --large-index Assembled_Untranslated_Transcriptomes/all_assembled_transcriptomes.fasta all_untranslated_transcriptomes_index