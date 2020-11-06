from sys import argv

if len(argv) != 3:
	print("Run with 2 arguments: input_GFF.gff3 output_FASTA.fasta")
	exit(0)
else:
	pass

script, input_gff, input_fasta = argv

gff_file = open(codon_compute_gff)
gff2_file = open(codon2_compute_gff)


# Go through lines in GFF.

for line in gff_file:
	count = 0
	if ">" in gff_file:
	
    	count += 1
		else:
		pass
		
print(f"The total number of genes in species 1 is {count}.")

for line in gff2_file:
	count = 0
	if ">" in gff2_file:
	
    	count2 += 1
		else:
		pass
		
print(f"The total number of genes in species 2 is {count2}.")



line_length_total_species1 = 0	
line_length_total_species2 = 0	
for line in gff_file:
	if ">" in line:
		continue
		
	line_length = len(line)
	line_length_total += line_length
