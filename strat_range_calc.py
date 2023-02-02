# Chronostratigraphy Year Range Calculator
# Author: Paulina Marczak

# identify by column name not by index, also name can differ, maybe add a variable in batch file for column name

import os
import time

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

## Main


# @click.command()
# @click.argument("input_range_columns") # Value fields (max, max range, min, min range) in user data
# @click.argument("strat_age_list") # Category fields to classify chronostratigraphy in user data


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



## GUI - manual

class App(customtkinter.CTk):
	def __init__(self):
		super().__init__()

		self.title("Chronostratigraphy Year Range Calculator v 1.0")
		self.geometry("500x500")
		self.wm_attributes('-toolwindow', 'True')
		self.wm_iconbitmap('img/test.ico') # needs to be updated in future version of customtkinter to work here
		customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
		customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

		 # configure grid layout (4x4)
		# self.grid_columnconfigure(1, weight=1)
		# self.grid_columnconfigure((2, 3), weight=0)
		# self.grid_rowconfigure((0, 1, 2), weight=1)


		def optionmenu_callback(choice):
			print("optionmenu dropdown clicked:", choice)

		def select_file_path():
			self.filename = customtkinter.filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")))
			df = pd.read_excel(self.filename)
			columns = df.columns
			tkvar.set(columns[0]) # set default value

			column_menu = customtkinter.CTkOptionMenu(self, values = columns,  command=optionmenu_callback)
			column_menu.pack()
			column_menu.set(columns[0])  # set initial value

			return file_path

			#Make 3 more for the other input variables?

		def get_columns(file_path):
			df = pd.read_excel(file_path)
			columns = df.columns.tolist()
			return columns

		def update_dropdown(*args):
			file_path = select_file_path()
			columns = get_columns(file_path)
			column_var.set(columns[0])
			column_dropdown['values'] = columns
		

		# create textbox
		self.textbox = customtkinter.CTkTextbox(self, width=250)
		#self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
		self.textbox.insert("0.0", "Chronostratigraphy Age Range Calculator\n\n" + "The chronostratigraphy year range calculator takes in a.xlsx or .xls files.\n\n")
		self.textbox.pack()

		file_path = customtkinter.StringVar()
		column_var = customtkinter.StringVar()

		self.select_file_button = customtkinter.CTkButton(master=self, text = "Select the column where your max year is", command = select_file_path)
		self.select_file_button1 = customtkinter.CTkButton(master=self, text = "Select the column where your max year range is", command = select_file_path)
		self.select_file_button2 = customtkinter.CTkButton(master=self, text = "Select the column where your min year is", command = select_file_path)
		self.select_file_button3 = customtkinter.CTkButton(master=self, text = "Select the column where your min year range is", command = select_file_path)
		self.select_file_button4 = customtkinter.CTkButton(master=self, text = "Select just one column which describes the chronostratigraphy", command = select_file_path)
		self.select_file_button5 = customtkinter.CTkButton(master=self, text = "OR Select two columns which describe the chronostratigraphy", command = select_file_path)


		# self.select_file_button.pack()
		#self.select_file_button.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

		self.select_file_button1.pack()
		self.select_file_button2.pack()
		self.select_file_button3.pack()
		self.select_file_button4.pack()
		self.select_file_button5.pack()

		self.progressbar = customtkinter.CTkProgressBar(master=self)
		#self.progressbar.pack(padx=20, pady=10)

		


		# column_dropdown = ttk.Combobox(self, textvariable=column_var)
		# column_dropdown.pack()
		# column_dropdown1 = ttk.Combobox(self, textvariable=column_var)
		# column_dropdown1.pack()
		# column_dropdown2 = ttk.Combobox(self, textvariable=column_var)
		# column_dropdown2.pack()
		# column_dropdown3 = ttk.Combobox(self, textvariable=column_var)
		# column_dropdown3.pack()


		# tkvar = customtkinter.StringVar(self)
		# tkvar1 = customtkinter.StringVar(self)
		# tkvar2 = customtkinter.StringVar(self)

# if __name__ == '__main__':
# 	#main(input_range_columns, strat_age_list)
# 	app = App()
# 	app.mainloop()
# 	main(input_range_columns, strat_age_list)


## GUI - testing

class MainApp:
	def __init__(self, master):
		self.master = master
		self.master.title("Chronostratigraphy Year Range Calculator")

		def optionmenu_callback(choice):
			print("optionmenu dropdown clicked:", choice)

		def select_file_path():
			self.filename = customtkinter.filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes = (("Excel files", "*.xlsx"), ("all files", "*.*")))
			df = pd.read_excel(self.filename)
			columns = df.columns
			tkvar.set(columns[0]) # set default value

			column_menu = customtkinter.CTkOptionMenu(self, values = columns,  command=optionmenu_callback)
			column_menu.pack()
			column_menu.set(columns[0])  # set initial value

			return file_path

			#Make 3 more for the other input variables?

		def get_columns(file_path):
			df = pd.read_excel(file_path)
			columns = df.columns.tolist()
			return columns

		def update_dropdown(*args):
			file_path = select_file_path()
			columns = get_columns(file_path)
			column_var.set(columns[0])
			column_dropdown['values'] = columns


		# create textbox
		self.texty = tk.Text(self.master, height = 5, width = 52)
		self.texty.pack()
		#self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
		self.intro_spiel = tk.Label(self.master, text = "Chronostratigraphy Age Range Calculator\n\n" + "The chronostratigraphy year range calculator takes in a.xlsx or .xls files.\n\n")
		self.intro_spiel.pack()


		# create dropdown menu for selecting chrono category columns
		self.strat_age_list_label = tk.Label(self.master, text="Select the first chronostratigraphy category column")
		self.strat_age_list_label.pack()
		self.strat_age_list_var = tk.StringVar(self.master)
		self.strat_age_list_var.set("strat_age")
		self.strat_age_list_dropdown = tk.OptionMenu(self.master, self.strat_age_list_var, "strat_age")
		self.strat_age_list_dropdown.pack()

		# create dropdown menu for selecting chrono category columns
		self.strat_age_list_label = tk.Label(self.master, text="Select the second chronostratigraphy category column (Optional)")
		self.strat_age_list_label.pack()
		self.strat_age_list_var = tk.StringVar(self.master)
		self.strat_age_list_var.set("strat_age")
		self.strat_age_list_dropdown = tk.OptionMenu(self.master, self.strat_age_list_var, "strat_age")
		self.strat_age_list_dropdown.pack()


		# create dropdown menu for input_range_columns
		self.input_range_columns_label = tk.Label(self.master, text="Select input range columns:")
		self.input_range_columns_label.pack()
		self.input_range_columns_var = tk.StringVar(self.master)
		self.input_range_columns_var.set("age_max_t")
		self.input_range_columns_dropdown = tk.OptionMenu(self.master, self.input_range_columns_var,
														   "age_max_t", "age_max_t_range", "age_min_t", "age_min_t_range")
		self.input_range_columns_dropdown.pack()

		# create dropdown menu for input_range_columns
		self.input_range_columns_label = tk.Label(self.master, text="Select input range columns:")
		self.input_range_columns_label.pack()
		self.input_range_columns_var = tk.StringVar(self.master)
		self.input_range_columns_var.set("age_max_t")
		self.input_range_columns_dropdown = tk.OptionMenu(self.master, self.input_range_columns_var,
														   "age_max_t", "age_max_t_range", "age_min_t", "age_min_t_range")
		self.input_range_columns_dropdown.pack()

		# create dropdown menu for input_range_columns
		self.input_range_columns_label = tk.Label(self.master, text="Select input range columns:")
		self.input_range_columns_label.pack()
		self.input_range_columns_var = tk.StringVar(self.master)
		self.input_range_columns_var.set("age_max_t")
		self.input_range_columns_dropdown = tk.OptionMenu(self.master, self.input_range_columns_var,
														   "age_max_t", "age_max_t_range", "age_min_t", "age_min_t_range")
		self.input_range_columns_dropdown.pack()

		# create dropdown menu for input_range_columns
		self.input_range_columns_label = tk.Label(self.master, text="Select input range columns:")
		self.input_range_columns_label.pack()
		self.input_range_columns_var = tk.StringVar(self.master)
		self.input_range_columns_var.set("age_max_t")
		self.input_range_columns_dropdown = tk.OptionMenu(self.master, self.input_range_columns_var,
														   "age_max_t", "age_max_t_range", "age_min_t", "age_min_t_range")
		self.input_range_columns_dropdown.pack()


		# create button to execute main()
		self.execute_button = tk.Button(self.master, text="Execute", command=self.execute_main)
		self.execute_button.pack()

	def execute_main(self):
		input_range_columns = self.input_range_columns_var.get()
		strat_age_list = self.strat_age_list_var.get()
		main(input_range_columns, strat_age_list)

if __name__ == '__main__':
	root = tk.Tk()
	app = MainApp(root)
	root.mainloop()



print('Completed at:', (time.strftime('%a %H:%M:%S')), f', see output file at {out_dir}')

# todo: change to variable input
#todo: change to single versus multiple field inputs
#todo: conditions for 'upper/lower'
# Raise error class to make sure the inputs all have a matching output?