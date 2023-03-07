# import tkinter as tk
# import pandas as pd
# import tkinter.filedialog as fd
# from tkinter import messagebox

# class MainApp:
# 	def __init__(self, root):
# 		self.root = root
# 		self.root.title("Chronostratigraphy Year Range Calculator")

# 		def optionmenu_callback(choice):
# 			print("optionmenu dropdown clicked:", choice)

# 		def populate_options():
# 			# Open a file dialog to select the Excel file
# 			self.file_path = fd.askopenfilename(initialdir = "/", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
# 			# Load the selected Excel file into a pandas dataframe
# 			df = pd.read_excel(self.file_path)
# 			# Get a list of column names in the dataframe
# 			options = df.columns.tolist()
# 			# Clear any existing options in the option menu
# 			self.option_field_chrono["menu"].delete(0, "end")
# 			self.option_field_max_year["menu"].delete(0, "end")
# 			self.option_field_max_range["menu"].delete(0, "end")
# 			self.option_field_min_year["menu"].delete(0, "end")
# 			self.option_field_min_range["menu"].delete(0, "end")
# 			# Insert the new options into the option menu
# 			for option in options:
# 				self.option_field_chrono["menu"].add_command(label=option, command=tk._setit(self.var_chrono, option))
# 				self.option_field_max_year["menu"].add_command(label=option, command=tk._setit(self.var_max_year, option))
# 				self.option_field_max_range["menu"].add_command(label=option, command=tk._setit(self.var_max_range, option))
# 				self.option_field_min_year["menu"].add_command(label=option, command=tk._setit(self.var_min_year, option))
# 				self.option_field_min_range["menu"].add_command(label=option, command=tk._setit(self.var_min_range, option))

# 		# Create the Tkinter window

# 		# Create a button to populate the options
# 		self.label1 = tk.Label(self.root, text="Input path:")
# 		var = tk.StringVar(self.root)
# 		self.label1.pack()

# 		self.populate_button = tk.Button(self.root, text=" ", command=populate_options)
# 		self.populate_button.pack()

# 		# Create a button to show what the default file for the template is
# 		self.populate_button = tk.Button(self.root, text="Input Excel file for setting up fields", command=populate_options)
# 		self.populate_button.pack()

# 		# Create a dropdown to select Chronostratigraphy
# 		self.label2 = tk.Label(self.root, text="Chronostratigraphy Field (Existing):")
# 		self.var_chrono = tk.StringVar(self.root)
# 		self.var_chrono.set(" ")
# 		self.option_field_chrono = tk.OptionMenu(self.root, var, [])
# 		self.label2.pack()
# 		self.option_field_chrono.pack()

# 		# Create a dropdown to select Max Year Field Name
# 		self.label3 = tk.Label(self.root, text="Max Year Field Name (Existing):")
# 		self.var_max_year = tk.StringVar(self.root)
# 		self.var_max_year.set(" ")
# 		self.option_field_max_year = tk.OptionMenu(self.root, var, [])
# 		self.label3.pack()
# 		self.option_field_max_year.pack()

# 		# Create a dropdown to select Max Year Range Field Name
# 		self.label4 = tk.Label(self.root, text="Max Year Range Field Name (Existing):")
# 		self.option_field_max_range  = tk.StringVar(self.root)
# 		self.option_field_max_range.set(" ")
# 		self.option_field = tk.OptionMenu(self.root, var, [])
# 		self.label4.pack()
# 		self.option_field.pack()

# 		# Create a dropdown to select Min Year Field Name

# 		self.label5 = tk.Label(self.root, text="Min Year Field Name (Existing):")
# 		self.var_min_year = tk.StringVar(self.root)
# 		self.var_min_year.set(" ")
# 		self.option_field_min_year = tk.OptionMenu(self.root, var, [])
# 		self.label5.pack()
# 		self.option_field_min_year.pack()

# 		# Create a dropdown to select Min Year Range Field Name
# 		self.label6 = tk.Label(self.root, text="Min Year Range Field Name (Existing):")
# 		self.var_min_range = tk.StringVar(self.root)
# 		self.var_min_range.set(" ")
# 		self.option_field_min_range = tk.OptionMenu(root, var, [])
# 		self.label6.pack()
# 		self.option_field_min_range.pack()

# 		# create button to execute main()
# 		self.execute_button = tk.Button(self.root, text="Run", command= self.execute_main)
# 		self.execute_button.pack()

# 	def execute_main(self):
# 		input_range_columns = self.label1.get()
# 		main(input_range_columns)

# # Start the Tkinter event loop
# if __name__ == '__main__':
# 	root = tk.Tk()
# 	app = MainApp(root)
# 	root.mainloop()

import os
import time

print ('Starting at:', (time.strftime('%a %H:%M:%S')))
print ('Importing modules..')

import shutil
import pandas as pd
import csv
import re
import click
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

import tkinter as tk
import pandas as pd
from tkinter import messagebox


## Paths

script_dir = os.path.dirname(os.path.realpath(__file__))
out_dir= os.path.join(script_dir, 'out_dir')

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

input_range_columns = ['age_max_t',
						'age_max_t_range',
						'age_min_t',
						'age_min_t_range']

# Split incoming single-column range to two

# Possibly user input if already split into two, otherwise they are split from 1 input and renamed as this

strat_age_list_split = ['strat_age_max',
				'strat_age_min']

# Values columns from LUT - static

strat_age_Range_list = ['Max_Age_LUT',
						'Max_Age_Range_LUT',
						'Min_Age_LUT',
						'Min_Age_Range_LUT']

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

			out.to_csv(file_export)


class ExcelDropdownMenus(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("Chronostratigraphy Year Range Calculator")
		self.geometry("400x500")
		self.resizable(False, False)
		
		self.load_button = tk.Button(self, text="Load Excel File", command=self.load_excel)
		self.load_button.pack(pady=10)


		self.file_path = tk.StringVar()
		self.file_path_entry = tk.Entry(self, textvariable=self.file_path)
		self.file_path_entry.pack(pady=10)


		self.menus = []

		# creat list of option menus

		for i in range(5):
			menu = tk.OptionMenu(self, tk.StringVar(), [])
			menu.pack(pady=10)
			self.menus.append(menu)

		# create button to execute main()
		self.execute_button = tk.Button(self, text="Execute", command = ...)
		self.execute_button.pack()
	
	# create function to load excel file

	def load_excel(self):
		file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")))
		if file_path:
			self.file_path.set(file_path)
			try:
				df = pd.read_excel(file_path, sheet_name=0)
				columns = df.columns.tolist()
				for i, menu in enumerate(self.menus):
					menu["menu"].delete(0, "end")
					for column in columns:
						menu["menu"].add_command(label=column, command=lambda value=column: menu["variable"].set(value))
			except Exception as e:
				messagebox.showerror("Error", str(e))


	# ok so i need to add two more function to get columns adn update dropdown? 
	# but its already updating dropdown just need to grab items from list
	def get_columns(file_path):
		df = pd.read_excel(file_path)
		columns = df.columns.tolist()
		return columns

	def update_dropdown(*args):
		file_path = select_file_path()
		columns = get_columns(file_path)
		column_var.set(columns[0])
		column_dropdown['values'] = columns

	file_path = customtkinter.StringVar()
	column_var = customtkinter.StringVar()


if __name__ == "__main__":
	app = ExcelDropdownMenus()
	app.mainloop()
	main(input_range_columns, strat_age_list)

print('Completed at:', (time.strftime('%a %H:%M:%S')), f', see output file at {out_dir}')

#app needs to somehow connect each output to an empty list and then feed that list into the main()
#it needs the first menu item to append input_range_columns empty list
# it needs the next 4 menu items to append to  strat_age_list empty list