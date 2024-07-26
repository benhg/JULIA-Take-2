# Barcode Hopping

## Introduction

We have a dataset of a bunch of genome sequences from various spiders. We are concerned that some index hopping (https://www.illumina.com/techniques/sequencing/ngs-library-prep/multiplexing/index-hopping.html) has occurred. A few years ago, we did some experiemental work to try and figure out where that occurred, but we want to run it again for more confidence.

We're going to align sequences using [STAR](https://github.com/alexdobin/STAR).

## Plan of Action

Currently, we have a set of known transcripts in FASTA format, and a set of raw reads in FASTQ format. We will align the raw reads against the known transcripts using STAR. The specific plan of action is:

1. Add metadata to the sequences in the known transcripts (lane and sample ID)
2. Convert the FASTQ raw reads to FASTA, and add metadata to the FASTA tags
3. Build a genome index from all the transcripts
4. Run the STAR mapping step from that output

After we see the output from step 4, we'll decide next steps
