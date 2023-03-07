# Chronostratigraphy Year Range Calculator <a href="url"> <img src="https://stratigraphy.org/images/logo-ics-3D-dark.png" align="center" height="48" width="48" ></a>

## User manual

January 26, 2023

paulina.marczak@gov.bc.ca

## Table of Contents

[TOC]

## What does it do?

https://datatofish.com/executable-pyinstaller/
https://www.tomshardware.com/how-to/create-python-executable-applications


This calculator determines any outstanding date ranges for a given chronostratigraphic spreadsheet. 

Given an input Excel file (.xls, .xlsx), it populates the associated year ranges for the given stratigraphic ranges based on the version 2022/02 Chronostratigraphic Chart. The associated ranges are included in the lookup table (LUT.csv), which looks like this:

            System      Max_Age_LUT   Max_Age_Range_LUT Min_Age_LUT  Min_Age_Range_LUT
            Quaternary  2.58           0                0            0

The columns are described below:

`Max_Age_LUT` 

is defined as the oldest age of the given stratigraphic unit.

`Max_Age_Range_LUT`

is defined as any year range estimates associated with the oldest age.

`Min_Age_LUT`

is defined as the most recent age of the given stratigraphic unit.

`Min_Age_Range_LUT`

is defined as any year range estimates associated with the most recent age.

For an example, refer to the Quaternary system record above. The Max_Age_LUT is 2.58, which is the oldest age that is classified under Quaternary. 

Records that are uncertain (i.e., they contain a question mark) will not be populated.

## User-Editable Parameters:

* You can edit the age values to give different ranges if you like. To do this, change them in the LUT.csv copy of the /parent folder.
* This script requires your inputs to contain at least one 'from' and one 'to' System/Period/Series/Epoch/Stage/Age column. Alternatively, you can supply one column which specifies a 'from' and 'to' in the form of:

`Mesoproterozoic to Neoproterozoic`

`Jurassic`

* You can set the name of the input column as an input environment variable. 
* The output is a resultant .csv file with the populated ranges. Ranges that were already populated are not overwritten unless specified, which is the default setting.

See Example (modifiable parameters) for more details.

## Requirements for use:

1) The file has to be an excel file. If you have a csv, save it as an Excel file.

2) The file has to be sitting in the same directory as the script. It can also be in a subdirectory of the script. The script will look for and try to process all Excel files within all subdirectories of the script location.

3) The fields that will be used for determining the age column need to be in a format that is friendly for the script. Friendly format is described in the Example (basic) section below.

4) You should have Docker installed.


### Example (basic):

Here is my input file, "stratigraphy_2023_12_08.xlsx".

        strat_age                    age_max
        Devonian (and Carboniferous) (blank cell)
        Carboniferous to Permian     (blank cell)
        Devonian?                    (blank cell)

After double-clicking the runpy.bat, my file will be converted to

        strat_age                      age_max
        Devonian (and Carboniferous)   419.2
        Carboniferous to Permian       254.14
        Devonian?                      (blank cell)

as "stratigraphy_2023_12_08_out.xlsx" in the subdirectory /out.

As you can see, strat_age values that have question marks are not calculated in the age_max column. The calculator populates empty cells inline, meaning the original age_max column is populated. The calculator does not overwrite existing values in age_max and does not calculate values for any other input strat_age format.

Users must take care to ensure their data is formatted to reflect the strat_age example above for use in the calculator or unintended errors may arise.

### Example (modifiable parameters):

An example batch file execution is as such:

        -Run strat_range_calc.py -one -



# Support:

For issues that arise that have not been documented above, contact Paulina.