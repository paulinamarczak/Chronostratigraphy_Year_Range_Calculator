# Conditional field population
# Author: Paulina Marczak

# iteratively grab excel files to process

# convert to pandas.df

# identify columns for which stratigraphy code exists

# identify by column name not by index, also name can differ, maybe add a variable in batch file for column name

# does only the age column matter? 

# add new empty field for min range, max age, and age +/- range

# populate empty fields using data dictionary

# data dictionary can be text file included with script?

# ask george what the accepted inputs should be, whether the code should be flexible for multiple columns or just one coded column, or preferrably just the Stage/Age column

import os

import time

print ("Starting at:", (time.strftime('%a %H:%M:%S')))
print ("Importing modules..")

import shutil

import pandas as pd

import csv

# Paths

script_dir = os.path.dirname(os.path.realpath(__file__))
out_dir= os.path.join(script_dir, "out_dir")

# Make output path
if not os.path.exists(out_dir):
	os.makedirs(out_dir)


# Stratigraphic units Look-up dictionary
# import from csv?
LUT = pd.read_csv("LUT.csv",  sep=",", encoding='cp1252')
print(LUT)

# Format as dictionary

LUT_dict = {}

# LUT_dict = {name: (i, parks_merge) for name,i,parks_merge in zip(intersect_list_names, intersect_list, park_merge_list)}


#how do i want it to look

LUT_dict = {
  "System": "Quaternary",
  "Epoch": "Holocene",
  "Stage": "Meghalayan",
  "age_max_t":0.0042,
  "age_max_t_range": 0
}


# Get all tifs in subdirectories

process_files_list = []


print ("Gathering input files..")

for r,d,f in os.walk(script_dir):
	# for file in each sub directory
	for file in f:
		if file.endswith(".xlsx") and not file.startswith('~$') or file.endswith(".xls") and not file ==("LUT.csv") and not file.endswith("out.csv"):
			process_files_list.append(os.path.join(r, file))
			print(f"Appended {file} to analysis")

print (f"Processing the following files: {process_files_list}")


for filename in process_files_list:
	print("Calculating year ranges for", filename)
	file = pd.read_excel(filename)

	file[strat_age].split()...
	
	Left_join = pd.merge(file, 
	                     LUT, 
	                     left_on=['era','period', 'strat_age'],
	                     right_on=['System', 'Epoch', 'Stage'],
	                     how ='left')

	#Left_join.drop('System', 'Epoch', 'Stage')
	#split the column to identify ranges
	print(Left_join)


# # def main(productlevel_list, bandproduct_list, startyear,endyear, field_threshold):

# # if __name__ == "__main__":
# # 	main(productlevel, bandproduct, startyear, endyear, field_threshold)


# print("Completed at:", (time.strftime('%a %H:%M:%S')), f", see {out_dir}")


