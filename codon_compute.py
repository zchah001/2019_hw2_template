#!/usr/bin/env/python

import sys

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
