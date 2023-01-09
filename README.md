# Chronostratigraphy_Year_Range_Calculator
 Calculate the date ranges for a given chronostratigraphic code

Given an input Excel file (.xls, .xlsx), populate the associated year ranges for the given stratigraphic ranges.

This script requires your inputs to contain at least a System/Period column, and Series/Epoch or Stage/Age if possible.

You can set the name of the input column as an input environment variable. 

The output is a resultant .csv file with the populated ranges. Ranges that were already populated are not overwritten unless specified, which is the default setting.

An example batch file execution is as such:

-Run strat_range_calc.py -NO OVERWRITE 