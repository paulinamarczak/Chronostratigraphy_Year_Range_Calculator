import tkinter as tk
import pandas as pd

def populate_options():
	# Load the Excel file into a pandas dataframe
	df = pd.read_excel("sampleData_AgeUpdate.xlsx")
	# Get a list of unique values in the specified column
	options = df.columns.tolist()
	# Clear any existing options in the option menu
	option_field["menu"].delete(0, "end")
	# Insert the new options into the option menu
	for option in options:
		option_field["menu"].add_command(label=option, command=tk._setit(var, option))

# Create the Tkinter window
root = tk.Tk()
root.title("Option Field Example")

# Create a label and option field
label = tk.Label(root, text="Select an option:")
var = tk.StringVar(root)
var.set("Select an option")
option_field = tk.OptionMenu(root, var, [])
label.pack()
option_field.pack()

# Create a button to populate the options
populate_button = tk.Button(root, text="Populate Options", command=populate_options)
populate_button.pack()

# Start the Tkinter event loop
root.mainloop()