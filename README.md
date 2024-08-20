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

Currently, we are at step 4, and not having memory problems yet.

The next step we have is to create a summary. Ultimately, we want something that predicts which sequences (not samples, but sequences within the samples) are having index hopping. But first, we will create some summary statistics. See `generate_summary.py` for details.

## Notes

To execute one of the python scripts on slurm, use "slurm_run.sh" script:

`sbatch --cpus-per-task=48 slurm_run.sh <name of the python script to run>`

This is kind of a hack, to be honest, but whatever. It works.

## Dataset Descriptions

This section describes all the datasets, specifies where they are stored, and states what we're using them for.

### Assembled Translated Transcriptomes

**Location:** `/home/labs/binford/Assembled_Untranslated_Transcriptomes`

This dataset is a bunch of untranslated RNA transcriptomes of various things including the 22 samples originally sequenced. We are confident about the origin of this data, and we use it as a "golden reference". We build our indices from it and will query against it with other data.

**Files of note:** `all_assembled_transcriptomes.fasta` contains the whole dataset with sequence, lane, and sample IDs attached to each sequence ID as a tag, to make life easier

### Raw Reads

**Location:** `/home/labs/binford/raw_reads`

This data is the raw reads, straight out of the sequencer. It's in FASTQ format, and it has 1 FASTQ file for each sample. There's also some extra FASTQ files that have concatenated data from each sample. 

### Converted/Tagged Raw Reads

**Location:** `/home/labs/binford/raw_reads_fasta_tagged_batched`

This data is the same data as the raw reads, but it's transformed slightly. It's converted to FASTA format, and it has tags added to each sequence ID (lane, sample, species, etc.). We use these as the data for our Bowtie runs.

It's divided into two sections: batched files and combined files. The batched files are sets of 2,000,000 sequences each which have tags added. The combined files have been re-combined from batches.

**Files of note:**

`/home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane1_R1.fasta` contains all of the sequences from lane 1 (samples 1-11) in the R1 direction.

`/home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane1_R2.fasta` contains all of the sequences from lane 1 (samples 1-11) in the R2 direction.

`/home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane2_R1.fasta` contains all of the sequences from lane 2 (samples 12-22) in the R1 direction.

`/home/labs/binford/raw_reads_fasta_tagged_batched/combined_files/lane2_R2.fasta` contains all of the sequences from lane 2 (samples 12-22) in the R2 direction.

### Bowtie Indices

We created bowtie indices from each of the "lanes" (groups of 11 samples that were created with the same lane of the sequencer), as well as one index of all 22 samples. They are in the directories `all_untranslated_transcriptomes_index_lane_1`, `all_untranslated_transcriptomes_index_lane_2`, and `all_untranslated_transcriptomes_index`. In the `single_sample_indexes` directory, each sample has an index made just from its known transcripts.

### Bowtie output directories

The bowtie output files underneath `single_sample_index/s<0XX>/` contain an index for each sample. Each set of reads is run against every sample from the same lane, and the .SAM output files are stored in the same directory as the index. For example, the .SAM file for reads from sample 2 run against the index for sample 1 is stored in the directory `/home/labs/binford/single_sample_indexes/s001_index/` with filename `index_001_read_s002.sam`.

