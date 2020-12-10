#!/usr/bin/env python3


# Download the required files using curl

gff="Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.37.gff3.gz"
fasta="Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.dna.chromosome.Chromosome.fa.gz"

import os,gzip,itertools,csv,re

# To parse FASTA files
# define what a header looks like in FASTA format
def isheader(line):
    return line[0] == '>'

def aspairs(f):
    seq_id = ''
    sequence = ''
    for header,group in itertools.groupby(f, isheader):
        if header:
            line = next(group)
            seq_id = line[1:].split()[0]
        else:
            sequence = ''.join(line.strip() for line in group)
            yield seq_id, sequence
            
if not os.path.exists(gff):
    os.system("curl -O ftp://ftp.ensemblgenomes.org/pub/bacteria/release-45/gff3/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.37.gff3.gz")

if not os.path.exists(fasta):
    os.system("curl -O ftp://ftp.ensemblgenomes.org/pub/bacteria/release-45/fasta/bacteria_0_collection/escherichia_coli_str_k_12_substr_mg1655/dna/Escherichia_coli_str_k_12_substr_mg1655.ASM584v2.dna.chromosome.Chromosome.fa.gz")
    

# Process gff to get gene count, total gene length and coding length

with gzip.open(gff, "rt") as fh:

# now add code to process this

    gff = csv.reader(fh, delimiter="\t")
    Num_of_Genes = 0
    Total_Gene_Length = 0
    Total_Exon_Length = 0
    for row in gff:
        if row[0].startswith("#"):
                continue

        if row[2] == 'gene':
            Num_of_Genes += 1
            Total_Gene_Length += int(row[4]) - int(row[3])

        if row[2] == 'CDS':
            Total_Exon_Length += int(row[4]) - int(row[3])


# Process fasta to get total genome length

with gzip.open(fasta, "rt") as fh:
     pairs = aspairs(fh)
     seqs = dict(pairs)
     Total_Genome_Length = len(seqs['Chromosome'])


# Print results
print('Number of genes: {}'.format(Num_of_Genes))
print('Total length of the genes is: {}'.format(Total_Gene_Length))
print('Total length of genome is: {}'.format(Total_Genome_Length))
print('percentage of the genome which is coding: {:.2f}%'.format(100 * (Total_Exon_Length/Total_Genome_Length)))
