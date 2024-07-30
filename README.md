# Barcode Hopping

## Introduction

We have a dataset of a bunch of genome sequences from various spiders. We are concerned that some index hopping (https://www.illumina.com/techniques/sequencing/ngs-library-prep/multiplexing/index-hopping.html) has occurred. A few years ago, we did some experiemental work to try and figure out where that occurred, but we want to run it again for more confidence.

We're going to align sequences using [STAR](https://github.com/alexdobin/STAR).

## Plan of Action

Currently, we have a set of known transcripts in FASTA format, and a set of raw reads in FASTQ format. We will align the raw reads against the known transcripts using STAR. The specific plan of action is:

1. Add metadata to the sequences in the known transcripts (lane and sample ID)
    a. This is done with `aggregate_tag_transcriptomes.py`
2. Convert the FASTQ raw reads to FASTA, and 
    a. This is done with `fastq_to_fasta.py`
3. Add metadata to the FASTA tags
    a. This is done with `tag_raw_reads.py`. It does it in lots of batches for memory consumption purposes
    b. This can be assembled into one file with `cat`
4. Build a genome index from all the transcripts
    a. There is an SBATCH script for this: `star_generate_genome_index.sh`
5. Run the STAR mapping step from that output

After we see the output from step 4, we'll decide next steps

After getting through step 3, step 4 turned out to be problematic. STAR consumes way more memory than it should. Therefore, we're going to proceed with Bowtie2 instead of STAR. After consulting some experts and ourselves, we decided to do this:

1. Create bowtie indexes for:
    a. The whole set of assembled transcripts
    b. Just lane 1 transcripts
    c. Just lane 2 transcripts.
2. Use Bowtie to run every raw read from lane 1 against lane 1 and every raw read from lane 2 against lane 2
3. If we run out of memory trying to do step 2, repeat it but only using one sample at a time, to create 22 sets of outputs
4. Examine the results and decide next steps.

## Notes

To execute one of the python scripts on slurm, use "slurm_run.sh" script:

`sbatch --cpus-per-task=48 slurm_run.sh <name of the python script to run>`

This is kind of a hack, to be honest, but whatever. It works.
