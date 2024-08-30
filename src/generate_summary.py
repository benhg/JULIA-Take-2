"""
Generate a Summary CSV based on the Bowtie alignment output(s)

Summary contains the information that Bowtie produced as well as where to get the full SAM file
"""
from glob import glob
import csv
import subprocess
import sys


sample_to_taxon = {
    "s001": "Drymusa_serrana",
    "s002": "Loxo_arizonica",
    "s003": "Loxo_arizonica",
    "s004": "Loxo_arizonica",
    "s005": "Hexophthalma",
    "s006": "Hexophthalma",
    "s007": "Hexophthalma",
    "s008": "Periegops_MP_VG",
    "s009": "Periegops_MP_VG",
    "s010": "Periegops_MP_VG",
    "s011": "Periegops_MP_WB",
    "s012": "Periegops_VG_H",
    "s013": "Physocyclus",
    "s014": "Plectreurys",
    "s015": "Loxo_reclusa",
    "s016": "Zephryarchea",
    "s017": "Zephryarchea",
    "s018": "Scytodes",
    "s019": "Loxo_rufescens",
    "s020": "Loxo_spinulosa",
    "s021": "Periegops_MP_WB",
    "s022": "Periegops_MP_WB"

}


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode(sys.stdout.encoding)

headers = ["reads_sample", "reads_taxon", "index_sample", "index_taxon", "num_reads", "num_transcripts",  "num_aligned_none", "num_aligned_once", "num_aligned_multiple", "none_alignment_rate", "single_alignment_rate", "multiple_alignment_rate", "num_aligned_any" ,"alignment_rate", "reads_per_transcript_none", "reads_per_transcript_one", "reads_per_transcript_multiple", "reads_per_transcript_any", "exec_time"]

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
            try:
                # Name and metadata
                slurm_job_name = file.split("slurm-")[1].split(".out")[0]
                slurm_time_str = run_cmd(f'sacct --format="Elapsed" -j {slurm_job_name}')\
                slurm_time = slurm_time_str.split("\n")[-2].strip()


                
                # Text from stderr (which is summary info)
                data = fh2.readlines()

                #Sample IDs
                index_sample = data[0].split(" ")[0].split("_")[1].strip()
                reads_sample = data[0].split(" ")[1].split("_")[1].strip()


                # Number of transcripts
                num_transcripts = int(run_cmd(f'bowtie2-inspect --large-index /home/labs/binford/single_sample_indexes/{index_sample}_index/{index_sample}_index | grep ">" | wc -l'))


                print(f"Job {slurm_job_name} for index {index_sample} and reads {reads_sample} took {slurm_time}")
                # This is gonna be gross
                row = {
                    "index_sample": index_sample,
                    "inxex_taxon": sample_to_taxon[index_sample],
                    "reads_sample": reads_sample,
                    "reads_taxon": sample_to_taxon[reads_sample],
                    "num_reads": int(data[1].split(" ")[0]),
                    "num_transcripts": num_transcripts,
                    "num_aligned_none": int(data[3].split("(")[0].strip()),
                    "num_aligned_once": int(data[4].split("(")[0].strip()),
                    "num_aligned_multiple": int(data[5].split("(")[0].strip()),
                    "exec_time": slurm_time
                }

                # Alignment rates
                row["single_alignment_rate"] =  row["num_aligned_once"] / int(row["num_reads"])
                row["none_alignment_rate"] =  row["num_aligned_none"] / row["num_reads"]
                row["multiple_alignment_rate"] =  row["num_aligned_multiple"] / row["num_reads"]
                row["num_aligned_any"] = int(row["num_aligned_once"]) + int(row["num_aligned_multiple"])
                row["alignment_rate"] = row["num_aligned_any"] / row["num_reads"]

                # Reads/transcript scores
                row["reads_per_transcript_none"] = row["num_aligned_none"] / num_transcripts
                row["reads_per_transcript_one"] = row["num_aligned_once"] / num_transcripts
                row["reads_per_transcript_multiple"] = row["num_aligned_multiple"] / num_transcripts
                row["reads_per_transcript_any"] = row["num_aligned_any"] / num_transcripts


                writer.writerow(row)
            except Exception as e:
                print(f"failed for file {file}")     
