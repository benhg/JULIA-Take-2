"""
Print the number of transcripts in each index
"""
import subprocess

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


for index_sample in sample_to_taxon.keys():
    # Number of transcripts
    num_transcripts = int(run_cmd(f'bowtie2-inspect --large-index /home/labs/binford/single_sample_indexes/{index_sample}_index/{index_sample}_index | grep ">" | wc -l'))
    print(index_sample, num_transcripts)