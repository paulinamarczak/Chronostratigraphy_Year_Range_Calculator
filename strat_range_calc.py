# Chronostratigraphy Year Range Calculator
# Author: Paulina Marczak

# identify by column name not by index, also name can differ, maybe add a variable in batch file for column name

import os
import time
import sys

print ('Starting at:', (time.strftime('%a %H:%M:%S')))
print ('Importing modules..')

import shutil
import pandas as pd
import csv
import re
import click
import tkinter as tk
import customtkinter

# import tkinterweb
from tkinter import filedialog, ttk
import tkinter.messagebox
from PIL import Image, ImageTk

#streamlit
import numpy as np
import streamlit as st
from streamlit.web import cli as stcli


## Paths

script_dir = os.path.dirname(os.path.realpath(__file__))
out_dir= os.path.join(script_dir, 'out_dir')
filename = "strat_range_calc.py"

# Make output path
if not os.path.exists(out_dir):
	os.makedirs(out_dir)

## Lists

# Build LUT dictionaries

LUT_list = []

# Get all files for processing in subdirectories

process_files_list = []

# Get list of chronostraphigraphic cells which contain valid rows for populating year ranges

list_of_values_to_match = []

# Eventually these will be user-selected

# input_range_columns = ['age_max_t',
# 						'age_max_t_range',
# 						'age_min_t',
# 						'age_min_t_range']

# Split incoming single-column range to two

# Possibly user input if already split into two, otherwise they are split from 1 input and renamed as this

# strat_age_list_split = ['strat_age_max',
# 				'strat_age_min']

# Values columns from LUT - static

strat_age_Range_list = ['Max_Age_LUT',
						'Max_Age_Range_LUT',
						'Min_Age_LUT',
						'Min_Age_Range_LUT']


# Title

st.set_page_config(page_title = "Chronostratigraphy Year Range Calculator")
st.title("Chronostratigraphy Year Range Calculator")
st.write("Contact Information: Paulina Marczak, MSc | paulina.marczak@gov.bc.ca")

st.write("-------------")
st.write("Read the documentation at https://htmlpreview.github.io/?https://github.com/paulinamarczak/Chronostratigraphy_Year_Range_Calculator/blob/main/README.html")


# Load user data section

st.subheader("Upload your data as an Excel file")

types = ["xls", "xlsx"]

uploaded_file = st.file_uploader(label = "", type = types)


## Functions

def Find_uncertain_stratigraphy(item): # Makes a rule for which records should be populated, which excludes uncertain classifications, as marked by '?'

	search_ = bool(re.search(r'.*?([a-z_]*\?+[a-z_]*).*?',str(item)))
	return search_


## Define inputs

# Get dataset of all stratigraphic units and their ranges, as well as user-inputted excel files

print ('Gathering input files..')

LUT = pd.read_csv('LUT.csv',  sep=',', encoding='cp1252')

# Make this one a user input - possible to have two columns for this

strat_age_list = 'strat_age'

# Need dictionary structure for matching LUT with user data

for index,row in LUT.iterrows():
	d=row.to_dict()
	LUT_list.append(d)

## Main

def main(input_range_columns, strat_age_list):

	# Dict for comparing LUT field values with user values 

	strat_population_dict = dict(zip(input_range_columns,strat_age_Range_list))

	for r,d,f in os.walk(script_dir):
		
		for file in f:
			prefixes = ['~$', 'LUT']
			if file.endswith('.xlsx') and not file.startswith(tuple(prefixes)) or file.endswith('.xls') and not file.endswith('out.csv'):
				process_files_list.append(os.path.join(r, file))
				print(f'Appended {file} to analysis')

	print (f'Processing the following files: {process_files_list}')

	for filename in process_files_list:

		print('Calculating year ranges for', filename)
		file = pd.read_excel(filename)

		input_strat_list = strat_age_list.split(" ")

		# Splitting input stratigraphic range into two columns for easier merging
		#Ex., 'Carbiniferous to Permian' becomes 'Carbiniferous' and 'Permian'

		for input_strat_field in input_strat_list: #input_strat_field is 'strat_FIELD_x'

			file[input_strat_field] = file[input_strat_field].str.replace(r'\(|\)', '', regex = True) #strip all parentheses

			file[strat_age_list_split] = file[input_strat_field].str.split(r'to|and',expand=True) #split into two fields based on to or and in cell value
			
			# Populate strat_age_max and strat_age_min with single range strat_age entries (E.g., "Jurassic")

			for item in strat_age_list_split:

				file[item] = file[item].fillna(file[input_strat_field])

				file[item] = file[item].str.strip()
				file[item] = file[item].str.strip()

			filename_no_path = filename.split('.')[0].split('\\')[-1]

			file_export = os.path.join(out_dir, filename_no_path + '_out.csv')

			#merge file with LUT if exact match found for system, epoch, or stage
			out = pd.merge(file, LUT[['System_Series_Stage_LUT','Max_Age_LUT', 'Max_Age_Range_LUT']], left_on = 'strat_age_max', right_on= 'System_Series_Stage_LUT', how = 'left') #but only join the max dictionary values
			out = pd.merge(out, LUT[['System_Series_Stage_LUT','Min_Age_LUT', 'Min_Age_Range_LUT']], left_on = 'strat_age_min', right_on= 'System_Series_Stage_LUT', how = 'left') #but only join the min dictionary values

			# Populate only empty range values in origin dataset since we don't want to overwrite entries that are manually entered
			for key,val in strat_population_dict.items():
					out[key] = out[key].fillna(out[val])

			print(out.columns)

			# Don't want to keep intermediary joined columns
			out.drop(columns=out.columns[-8:], axis=1,  inplace=True)

			print(out.columns)

			return out



# Chronostratigraphy-added data section

if uploaded_file is not None:
	st.write("")
	st.subheader("Chronostratigraphy added data")
	st.write("")

	data = pd.read_excel(uploaded_file)
	
	#get file field options
	strat_age_list_split=st.multiselect("Select up to two chronostratigraphy descriptor columns (e.g., Mesoproterozoic to Neoproterozoic)",data.columns.unique())
	input_range_columns=st.multiselect("Select four chronostratigraphy year and year range columns (e.g., age_max_t	age_max_t_range	age_min_t age_min_t_range)",data.columns.unique())


	main(input_range_columns, strat_age_list)

	st.dataframe(out)

	st.write("")

	# Download button for RFC model results

	file_name = st.text_input(label = "Input file name (incude .csv)")

	

	@st.cache
	def convert_df(df):
		return df.to_csv(index = False).encode("utf-8")

	corrected_data_download = convert_df(out)
	st.download_button(label = "Download corrected data", data = corrected_data_download, file_name = file_name, mime = "text/csv")


if __name__ == '__main__':
	sys.argv = ["streamlit", "run", "strat_range_calc.py"]
	sys.exit(stcli.main())
	# main(input_range_columns, strat_age_list)

print('Completed at:', (time.strftime('%a %H:%M:%S')), f', see output file at {out_dir}')

# todo: change to variable input
#todo: change to single versus multiple field inputs
#todo: conditions for 'upper/lower'
# Raise error class to make sure the inputs all have a matching output?