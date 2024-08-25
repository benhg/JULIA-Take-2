"""
Generate a Summary CSV based on the Bowtie alignment output(s)

Summary contains the information that Bowtie produced as well as where to get the full SAM file
"""
from glob import glob
import csv
import subprocess


headers = ["reads_sample", "index_sample", "num_reads", "num_aligned_none", "num_aligned_once", "num_aligned_multiple", "none_alignment_rate", "single_alignment_rate", "multiple_alignment_rate", "num_aligned_any" ,"alignment_rate", "exec_time"]

path = "/home/glick/JULIA-Take-2/src/slurm-*.out"
output_file = "/home/labs/binford/single_sample_indexes/summary.csv"

with open(output_file, "w") as fh:
    writer = csv.writer(fh)
    writer.writerow(headers)

with open(output_file, "a") as fh:
    writer = csv.DictWriter(fh, fieldnames=headers)
    all_files = glob(path)
    for file in all_files:
        with open(file) as fh2:
            print(file)
            slurm_job_name = file.split("slurm-")[1].split(".out")[0]
            print(slurm_job_name)
            slurm_time = subprocess.check_output(f'sacct --format="Elapsed" -j {slurm_job_name}', shell=True).decode(sys.stdout.encoding)
            print(slurm_time)
            data = fh2.readlines()
            # This is gonna be gross
            try:
                row = {
                    "index_sample": data[0].split(" ")[0].split("_")[1].strip(),
                    "reads_sample": data[0].split(" ")[1].split("_")[1].strip(),
                    "num_reads": int(data[1].split(" ")[0]),
                    "num_aligned_none": int(data[3].split("(")[0].strip()),
                    "num_aligned_once": int(data[4].split("(")[0].strip()),
                    "num_aligned_multiple": int(data[5].split("(")[0].strip()),
                    "exec_time": ""
                }

                row["single_alignment_rate"] =  row["num_aligned_once"] / int(row["num_reads"])
                row["none_alignment_rate"] =  row["num_aligned_none"] / row["num_reads"]
                row["multiple_alignment_rate"] =  row["num_aligned_multiple"] / row["num_reads"]
                row["num_aligned_any"] = int(row["num_aligned_once"]) + int(row["num_aligned_multiple"])
                row["alignment_rate"] = row["num_aligned_any"] / row["num_reads"]
                writer.writerow(row)
            except:
                print(f"failed for file {file}")     
