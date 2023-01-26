# Chronostratigraphy Year Range Calculator
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
import re

# Define paths

script_dir = os.path.dirname(os.path.realpath(__file__))
out_dir= os.path.join(script_dir, "out_dir")

# Make output path
if not os.path.exists(out_dir):
	os.makedirs(out_dir)

# Lists

LUT_list = []

# Get all files for processing in subdirectories

process_files_list = []

## Get list of columns used for classifying chronostratigraphy

LUT_chrono_columns = ["System", "Epoch", "Stage"]

# Functions

## Make a rule for which records should be populated, which excludes uncertain classifications, as marked by '?'

def Find_uncertain_stratigraphy(item):

	search_ = bool(re.search(r'.*?([a-z_]*\?+[a-z_]*).*?',str(item)))
	return search_

# Define inputs

# Get dataset of all stratigraphic units and their ranges, as well as user-inputted excel files

print ("Gathering input files..")

LUT = pd.read_csv("LUT.csv",  sep=",", encoding='cp1252')

# Format as list of dictionaries

for index,row in LUT.iterrows():
	d=row.to_dict()
	LUT_list.append(d)

print(LUT_list)

for r,d,f in os.walk(script_dir):
	# for file in each sub directory
	for file in f:
		if file.endswith(".xlsx") and not file.startswith('~$') or file.endswith(".xls") and not file ==("LUT.csv") and not file.endswith("out.csv"):
			process_files_list.append(os.path.join(r, file))
			print(f"Appended {file} to analysis")

print (f"Processing the following files: {process_files_list}")

# Main

for filename in process_files_list:
	print("Calculating year ranges for", filename)
	file = pd.read_excel(filename)

	# Splitting input stratigraphic range into two columns for easier merging
	#Ex., 'Carbiniferous to Permian' becomes 'Carbiniferous' and 'Permian'

	strat_age_list = ['strat_age_max',
						'strat_age_min']

	#todo: change to variable input
	#todo: change to single versus multiple field inputs

	file[strat_age_list] = file['strat_age'].str.split('to',expand=True) 
	
	# Cleanup extra whitespace
	file['strat_age_max'] = file['strat_age_max'].str.strip()
	file['strat_age_min'] = file['strat_age_min'].str.strip()

	# print(file.columns)
	# print(file)

	# LUT_dict = {}

	for User_column in file.iloc[:, [-1,-2]]: #always going to be last two indices because new columns

		list_of_values_to_match = []

		columnSeriesObj_User = file[User_column]
		list_of_values_ = columnSeriesObj_User.values.tolist()

		for item in list_of_values_:
			if item is not None and item !="nan" and Find_uncertain_stratigraphy(item) == False:
				print("Found user record for populating", item)
				list_of_values_to_match.append(item)
			else: 
				continue
		for item in list_of_values_to_match:
			for dict_ in LUT_list:
				if item == dict_["System"]:
					print (f"Match found between dictionary {dict_['System']} and stratigraphy {item}")


	# for LUT_column in LUT.iloc[:, [0,1,2]]: # Compare each dataset column with possible stratigraphy phase
	# 	columnSeriesObj = LUT[LUT_column]
	# 	print("columnSeriesObj", columnSeriesObj.values)
	# 	LUT_dict = dict(zip(lakes.id, lakes.value))

	# 	list_a = columnSeriesObj.values.tolist()
	# 	LUT_dict.append(list_a)
	# 	print('LUT_dict', LUT_dict)
		
	# 	for User_column in file.iloc[:, [-1,-2]]:
	# 		# print(User_column)
	# 		columnSeriesObj_User = file[User_column]
	# 		# print(columnSeriesObj_User.values)
	# 		list_b = columnSeriesObj_User.values.tolist()
	# 		print(list_a, dict_b)
	# 		if list_a == dict_b:
	# 			print("match found", list_a, dict_b)


	# df1 = pd.merge(file, LUT, on='strat_age_max', how='outer', suffixes=('','_key'))
	

	# df1 = df1[(df1.start <= df1.start_key) & (df1.end <= df1.end_key)]
	# df1 = pd.merge(df, df1, on=['order','start','end', 'value'], how='left')

	# print(file)

	# print("Joining year ranges from lookup table")



	# Left_join = pd.merge(file, LUT, how='inner', left_on = 'strat_age_max', right_on = 'Epoch')

	# print(Left_join)

	# Left_join = file.merge(LUT, 
	# 					 left_on=['strat_age_max'],
	# 					 right_on=['Epoch'],
	# 					 how ='left')
	file= file.drop(file.index[0])

	#Left_join = file.assign(new_age_max=file['period'].map(LUT.set_index('Epoch')['strat_age_max']))


	# print("leftjoin", Left_join)
	# # Left_join.index = Left_join[colName]
	# list(Left_join.columns)
	# #Left_join = Left_join.drop(['System', 'Epoch', 'Stage', Left_join.columns[-1], Left_join.columns[-2]], axis= 1)
	# #split the column to identify ranges
	# print(Left_join)

	# filename_no_path = filename.split(".")[0].split("\\")[-1]

	# file_export = os.path.join(out_dir, filename_no_path + "_out.csv")
	# Left_join.to_csv(file_export)


# # def main(productlevel_list, bandproduct_list, startyear,endyear, field_threshold):

# # if __name__ == "__main__":
# # 	main(productlevel, bandproduct, startyear, endyear, field_threshold)


# print("Completed at:", (time.strftime('%a %H:%M:%S')), f", see {out_dir}")


