import os
import urllib
from collections import defaultdict
from pprint import pprint

# Fetched and truncated from
# https://www.uniprot.org/uniprot/?query=database%3A%28type%3Aembl+AE017195%29&format=fasta (Aug 01, 2020)
URL = "https://bites-data.s3.us-east-2.amazonaws.com/fasta_genes.fasta"
FASTA_FILE = os.path.join(os.getenv("TMP", "/tmp"), "fasta_genes.fasta")
if not os.path.isfile(FASTA_FILE):
    urllib.request.urlretrieve(URL, FASTA_FILE)


def fasta_to_2line_fasta(fasta_file: str, fasta_2line_file: str) -> int:
    """
    :param fasta_file: Filename of multi-line FASTA file
    :param fasta_2line_file: Filename of 2-line FASTA file
    :return: Number of records
    """
    fasta = defaultdict(str)

    with open(fasta_file) as fp:
        idx = None
        for line in fp:
            if ">" in line:
                idx = line.strip()
            else:
                if not idx:
                    continue
                else:
                    fasta[idx] += line.strip()

    with open(fasta_2line_file, "w") as fp:
        for idx, sequence in fasta.items():
            fp.write(f"{idx}\n")
            fp.write(f"{sequence}\n")

    return len(fasta)


if __name__ == "__main__":
    pprint(fasta_to_2line_fasta(FASTA_FILE, f"{FASTA_FILE}_converted.fasta"))
