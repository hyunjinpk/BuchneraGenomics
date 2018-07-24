#!/usr/bin/env/ python3

import os

def os_test(directory):
	# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
	filenames = []
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		filenames.append(filename)
	return filenames

def convert(file, directory):
	infile = open(directory + file, "r")
	outstring = "  24   "

	lines = infile.readlines()
	infile.close()

	outstring = outstring + str(len(lines[1].strip())) + "\n" + "\n"

	for line in lines:
		if line[0] == ">":
			outstring += line[1:]
		else:
			outstring = outstring + line + "\n"

	outfile = open("./PHYLIP/" + file[:-13] + ".phy", "w")
	outfile.write(outstring)
	outfile.close()
	return

def main():
	# Set path
	directory = "/Users/ochmanlab/Desktop/Hyunjin3/by_gene/aligned/nt_ali/"

	# Get file name
	filenames = os_test(directory)
	filenames.sort()

	# Convert each FASTA file to PHYLIP format
	for file in filenames:
		convert(file, directory)

main()