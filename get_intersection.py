#!/usr/bin/env/ python3

import pprint
import os

def get_gene_list(infile):
	genes = []
	for line in infile:
		if line[0] == ">":
			line = line.strip()
			genes.append(line[12:])
	return genes

def intersection(genes_of_all_species):
	# Initialization
	interesection = genes_of_all_species[0]

	# Iterate through rows of "genes_of_all species"; i.e. gene lists for each species
	for row in genes_of_all_species:
		interesection = [val for val in interesection if val in row and val != "hypothetical protein"]
	return interesection

def os_test(directory):
	# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
	filenames = []
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		filenames.append(filename)
	return filenames

def by_genes(intersect, directory, filenames):
	outstring = ""
	gene_counter = 0
	wrote = 0
	previous_line = ""

	for gene in intersect:
		gene_counter += 1
		for species in filenames:
			to_open = directory + "/" + species #(e.g. "./Buchnera/Aphis_CDSs/Aar.fna")
			infile = open(to_open)
			for line in infile:
				if gene in previous_line and species[:3] not in outstring:
					outstring = outstring + ">" + species[:3] + "\n" + line
					previous_line = ""
					break
				else:
					previous_line = line
			infile.close()
		# If gene length <= 200 (average across all 24 species), throw it away
		if len(outstring) < 4944: # 200*24=4800 characters from sequences; 4*24=96 characters from species name and ">"; 48 end-of-line characters
			outstring = ""
			print("Processed {} genes!".format(gene_counter))
			print("Wrote {} files!".format(wrote))
		else:
			# Error handling for the case where gene name contains "/"
			if "/" not in gene:
				outfile = open("./by_gene/" + gene + ".fasta", "w")
			else:
				index = gene.index("/")
				new_gene_name = gene[:index] + gene[index+1:]
				outfile = open("./by_gene/" + new_gene_name + ".fasta", "w")
			outfile.write(outstring)
			outfile.close()
			outstring = ""
			wrote += 1
			print("Processed {} genes!".format(gene_counter))
			print("Wrote {} files!".format(wrote))
	return

def main():
	# Set path
	directory = "./Buchnera/Aphis_CDSs"

	# Get species list
	filenames = os_test(directory)
	filenames.sort() # ['Aar.fna', ..., 'Uam.fna']
	print("Number of species:", len(filenames)) # 24

	# Get gene list for each species as a list of list
	genes_of_all_species = []
	for file in filenames:
		to_open = directory + "/" + file #(e.g. "./Buchnera/Aphis_CDSs/Aar.fna")
		infile = open(to_open)
		genes = get_gene_list(infile)
		infile.close()
		genes_of_all_species.append(genes)

	# Get intersection, i.e. the genes present in all 24 species
	intersect = intersection(genes_of_all_species)
	pprint.pprint(intersect)
	print("Number of intersecting genes:", len(intersect)) # 400

	# Create FASTA files by gene with different species
	by_genes(intersect, directory, filenames)

main()