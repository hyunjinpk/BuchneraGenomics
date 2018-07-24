#!/usr/bin/env/ python3

import os

def os_test(directory):
	# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
	filenames = []
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		filenames.append(filename)
	return filenames

def translatorx(file, directory):
	command = "perl " + directory + "/aligned/translatorx.pl -i " + directory + "/" + file + " -o " + directory + "/aligned/" + file[:-6]
	print(command)
	os.system(command)
	return

def main():
	# Set path
	directory = "/Users/ochmanlab/Desktop/Hyunjin3/by_gene"

	# Get file list
	filenames = os_test(directory)
	filenames.sort()

	# Align each gene using TranslatorX
	for file in filenames:
		translatorx(file, directory)

main()