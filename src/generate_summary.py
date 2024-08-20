"""
Generate a Summary CSV based on the Bowtie alignment output(s)

Summary contains the information that Bowtie produced as well as where to get the full SAM file
"""
from glob import glob
import csv

headers = ["reads_sample", "index_sample", "num_reads", "num_aligned_none", "aligned_once", "aligned_multiple", "alignment_rate"]

path = "/home/glick/JULIA-Take-2/src/slurm-*.out"
output_file = "/home/labs/binford/single_sample_indexes/summary.csv"

with open(output_file, "w") as fh:
	writer = csv.DictWriter(fieldnames=headers)
	all_files = glob(path)
	for file in all_files:
		with open(file) as fh2:
			data = fh2.readlines()
			print(data)
