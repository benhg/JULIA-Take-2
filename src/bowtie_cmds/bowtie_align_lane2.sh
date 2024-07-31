#!/bin/bash
#SBATCH --cpus-per-task=48

# NOTE: Job 1730 on Lettuce is lane2

bowtie2 --time --un /home/labs/binford/lane2_collateral/unpaired_unaligned.txt --al /home/labs/binford/lane2_collateral/unpaired_aligned.txt --un-conc /home/labs/binford/lane2_collateral/paired_conc_unaligned.txt --al-conc /home/labs/binford/lane2_collateral/paired_conc_aligned.txt  --met-file /home/labs/binford/lane2_collateral/lane1_bt_metrics.txt -f --threads 48 -x /home/labs/binford/all_untranslated_transcriptomes_index_lane_2/all_untranslated_transcriptomes_index_lane_2 -1 /home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane2_R1.fasta -2 /home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane2_R2.fasta