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


LUT_dict = {
  "System": "Quaternary",
  "Epoch": "Holocene",
  "Stage": "Meghalayan",
  "strat_age_max":0.0042,
  "strat_age_max_range": 0
}

#Get list of columns used for classifying chronostratigraphy

LUT_chrono_columns = ["System", "Epoch", "Stage"]

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

	# Splitting input stratigraphic range into two columns for easier merging
	#Ex., 'Carbiniferous to Permian' becomes 'Carbiniferous' and 'Permian'

	strat_age_list = ['strat_age_max',
						'strat_age_min']

	file[strat_age_list] = file['strat_age'].str.split('to',expand=True) 
	
	# Cleanup extra whitespace
	file['strat_age_max'] = file['strat_age_max'].str.strip()
	file['strat_age_min'] = file['strat_age_min'].str.strip()

	print(file)
	# print(LUT.loc[:, [LUT_chrono_columns]])
	for LUT_column in LUT.iloc[:, [0,1,2]]: # Compare each dataset column with possible stratigraphy
		columnSeriesObj = LUT[LUT_column]
		print(columnSeriesObj.values)

		for User_column in file.loc[:, [strat_age_list]]:
			columnSeriesObj_User = LUT[User_column]
			print(columnSeriesObj_User.values)

	df1 = pd.merge(file, LUT, on='strat_age_max', how='outer', suffixes=('','_key'))
	

	df1 = df1[(df1.start <= df1.start_key) & (df1.end <= df1.end_key)]
	df1 = pd.merge(df, df1, on=['order','start','end', 'value'], how='left')

	print(file)

	print("Joining year ranges from lookup table")



	Left_join = pd.merge(file, LUT, how='inner', left_on = 'strat_age_max', right_on = 'Epoch')

	print(Left_join)

	# Left_join = file.merge(LUT, 
	# 					 left_on=['strat_age_max'],
	# 					 right_on=['Epoch'],
	# 					 how ='left')
	file= file.drop(file.index[0])

	#Left_join = file.assign(new_age_max=file['period'].map(LUT.set_index('Epoch')['strat_age_max']))


	print("leftjoin", Left_join)
	# Left_join.index = Left_join[colName]
	list(Left_join.columns)
	#Left_join = Left_join.drop(['System', 'Epoch', 'Stage', Left_join.columns[-1], Left_join.columns[-2]], axis= 1)
	#split the column to identify ranges
	print(Left_join)

	filename_no_path = filename.split(".")[0].split("\\")[-1]

	file_export = os.path.join(out_dir, filename_no_path + "_out.csv")
	Left_join.to_csv(file_export)


# # def main(productlevel_list, bandproduct_list, startyear,endyear, field_threshold):

# # if __name__ == "__main__":
# # 	main(productlevel, bandproduct, startyear, endyear, field_threshold)


# print("Completed at:", (time.strftime('%a %H:%M:%S')), f", see {out_dir}")


