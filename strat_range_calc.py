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

# Get list of chronostraphigraphic cells which contain valid rows for populating year ranges

list_of_values_to_match = []

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

# Main

for r,d,f in os.walk(script_dir):
	# for file in each sub directory
	for file in f:
		# if "LUT" not in file:
		# 	print(file)
		prefixes = ['~$', 'LUT']
		if file.endswith(".xlsx") and not file.startswith(tuple(prefixes)) or file.endswith(".xls") and not file ==("LUT.csv") and not file.endswith("out.csv"):
			process_files_list.append(os.path.join(r, file))
			print(f"Appended {file} to analysis")

print (f"Processing the following files: {process_files_list}")

for filename in process_files_list:
	print("Calculating year ranges for", filename)
	file = pd.read_excel(filename)

	# Splitting input stratigraphic range into two columns for easier merging
	#Ex., 'Carbiniferous to Permian' becomes 'Carbiniferous' and 'Permian'

	# todo: change to variable input
	#todo: change to single versus multiple field inputs
	#todo: conditions for 'upper/lower'

	strat_age_list = ['strat_age_max',
						'strat_age_min']

	# make function?
	file['strat_age'] = file['strat_age'].str.replace(r"\(|\)", "") #strip all parentheses
	file[strat_age_list] = file['strat_age'].str.split(r'to|and',expand=True)
	file['strat_age_max'] = file['strat_age_max'].str.strip()
	file['strat_age_min'] = file['strat_age_min'].str.strip()

	#define export paths

	filename_no_path = filename.split(".")[0].split("\\")[-1]

	file_export = os.path.join(out_dir, filename_no_path + "_out.csv")

	# method 1
	print(file)
	print (file.columns)
	out = pd.merge(file, LUT[["System_Series_Stage","age_max_t", "age_max_t_range"]], left_on = "strat_age_max", right_on= "System_Series_Stage", how = 'left') #but only join the max dictionary values
	out = pd.merge(out, LUT[["System_Series_Stage","age_min_t", "age_min_t_range"]], left_on = "strat_age_min", right_on= "System_Series_Stage", how = 'left') #but only join the min dictionary values

	out = out.drop(columns = ['System_Series_Stage_x', 'System_Series_Stage_y'])
	
	print(out)

	out.to_csv(file_export)


	#method 2
	for User_column in file.iloc[:, [-1,-2]]: #always going to be last two indices because new columns

		columnSeriesObj_User = file[User_column]
		list_of_values_ = columnSeriesObj_User.values.tolist()

		for item in list_of_values_:
			if item is not None and item !="nan" and Find_uncertain_stratigraphy(item) == False: # Can only populate where stratigraphy has been defined
				list_of_values_to_match.append(item)
			else: 
				continue

		# match user record with a dictionary reference

		for item in list_of_values_to_match:
			#print("item", item)
			for dict_ in LUT_list:
				#print(dict_)
				full_name = f' look here {dict_["System_Series_Stage"]} {dict_["age_max_t"]}'
				# print(full_name)

				if item == dict_["System_Series_Stage"]:

					columnSeriesObj_User['age_max_t']= dict_["age_max_t"]
					columnSeriesObj_User['age_min_t']= dict_["age_min_t"]
					columnSeriesObj_User['age_max_t_range']= dict_["age_max_t_range"]
					columnSeriesObj_User['age_min_t_range']= dict_["age_min_t_range"]

					print(columnSeriesObj_User)



# # def main(productlevel_list, bandproduct_list, startyear,endyear, field_threshold):

# # if __name__ == "__main__":
# # 	main(productlevel, bandproduct, startyear, endyear, field_threshold)


print("Completed at:", (time.strftime('%a %H:%M:%S')), f", see {out_dir}")


