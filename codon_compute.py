#!/usr/bin/env/python

#!/usr/bin/env python3

import os, gzip, itertools
from collections import Counter
# this is code which will parse FASTA files
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

def returnSum(myDict):

    sum = 0
    for i in myDict:
        sum = sum + myDict[i]

    return sum
url1="ftp://ftp.ensemblgenomes.org/pub/bacteria/release-45/fasta/bacteria_0_collection/salmonella_enterica_subsp_enterica_serovar_typhimurium_str_lt2/cds/Salmonella_enterica_subsp_enterica_serovar_typhimurium_str_lt2.ASM694v2.cds.all.fa.gz"
url2="ftp://ftp.ensemblgenomes.org/pub/bacteria/release-45/fasta/bacteria_0_collection/mycobacterium_tuberculosis_h37rv/cds/Mycobacterium_tuberculosis_h37rv.ASM19595v2.cds.all.fa.gz"
file1="Salmonella_enterica_subsp_enterica_serovar_typhimurium_str_lt2.ASM694v2.cds.all.fa.gz"
file2="Mycobacterium_tuberculosis_h37rv.ASM19595v2.cds.all.fa.gz"

if not os.path.exists(file1):
    os.system("curl -O %s"%(url1))

if not os.path.exists(file2):
    os.system("curl -O %s"%(url2))

n_gene1 = 0 #number of gene in file 1
n_gene2 = 0 #number of gene in file 2
L_gene1 = 0 #length of gene in file 1
L_gene2 = 0 #length of gene in file 2
G_number1 = 0 #numer of G in file 1
C_number1 = 0 #numer of C in file 1
G_number2 = 0 #numer of G in file 2
C_number2 = 0 #numer of C in file 2

codon1 = {}
# creating a dictionary for codon.
for first in {'A','T','C','G'}:
    for second in {'A','T','C','G'}:
        for third in {'A','T','C','G'}:
            new_codon = first+second+third
            new_dict = {new_codon:0}
            codon1.update(new_dict)


codon2 = {}
# creating a dictionary for codon.
for first in {'A','T','C','G'}:
    for second in {'A','T','C','G'}:
        for third in {'A','T','C','G'}:
            new_codon = first+second+third           
            new_dict = {new_codon:0}
            codon2.update(new_dict)
codonF = {}
# creating a dictionary for codon.
for first in {'A','T','C','G'}:
    for second in {'A','T','C','G'}:
        for third in {'A','T','C','G'}:
            new_codon = first+second+third
            new_dict = {new_codon:0}
            codonF.update(new_dict)

with gzip.open(file1,"rt") as fh:
    seqs1 = aspairs(fh)
    for seq1 in seqs1:
        seqname1  = seq1[0]
        seqstring1= seq1[1]
        n_gene1 = n_gene1 + 1
        L_gene1 = L_gene1 + len(seqstring1)
        base = Counter(seqstring1)
        g_number1 = G_number1 + base['G']
        c_number1 = C_number1 + base['C']
        for i in range(0,len(seqstring1)-1,3):
            if seqstring1[i:i+3] in codon1:
                codon1[seqstring1[i:i+3]] += 1
            else:
                codon1[seqstring1[i:i+3]] = 1

with gzip.open(file2,"rt") as fj:
    seqs2 = aspairs(fj)
    for seq2 in seqs2:
        seqname2  = seq2[0]
        seqstring2= seq2[1]
        n_gene2 = n_gene2 + 1
        L_gene2 = L_gene2 + len(seqstring2)
        base = Counter(seqstring2)
        g_number2 = G_number2 + base['G']
        c_number2 = C_number2 + base['C']
        for i in range(0,len(seqstring2)-1,3):
            if seqstring2[i:i+3] in codon2:
                codon2[seqstring2[i:i+3]] += 1
            else:
                codon2[seqstring2[i:i+3]] = 1
       # print(seqname, " first 10 bases are ", seqstring[0:10])
for key in codonF:
    codonF[key] = str(round(codon1[key]/returnSum(codon1),3)) +  str(round(codon2[key]/returnSum(codon2),3))
print("The Number of genes in species 1 is:",n_gene1)
print("The Length of genes in Species 1 is:",L_gene1)
print("The Number of genes in species 2 is:",n_gene2)
print("The Length of genes in Species 2 is:",L_gene2)



print("The G+C percentage of species 1 is:",(g_number1 + c_number1)/L_gene1)
print("The G+C percentage of species 2 is:",(g_number2 + c_number2)/L_gene2)
print("The G+C percentage of total dataset is:",(g_number2 + c_number2 + g_number1 + c_number1 )/(L_gene2 + L_gene1))
print("The Codon numbers in species  1 are ",returnSum(codon1))
print("The Codon numbers in species  2 are ",returnSum(codon2))
print("The Codon frequency is", str(codonF))



def process_fasta(fasta):
	with open(fasta, 'r') as f:
		genes = 0
		seq = []
		for i in f:
			if i.startswith(">"):
				genes += 1
			else:
				i = i.rstrip("\n")
				seq.append(i)

		seq = ''.join(seq)
		l = sum(len(i) for i in (seq))

		GC = 0
		for i in seq:
			if i == 'G' or i == 'C':
				GC += 1
		GCpercent = [str(round(GC/l*100, 2)),"%"]
		GCpercent = ''.join(GCpercent)
		TotalCodons = round(l/3)

		return genes, l, GCpercent, TotalCodons

genes, l, GCpercent, TotalCodons = process_fasta(sys.argv[1])
print("\n","Number of genes = %s"%genes,"\n","Total nucleotides = %s"%l,"\n","GC content = %s"%GCpercent,"\n","Total codons = %s"%TotalCodons,"\n")
