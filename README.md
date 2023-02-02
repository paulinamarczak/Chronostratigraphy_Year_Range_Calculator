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


---------
## Notes on Dockerfile

To deploy an app using a Dockerfile, you'll need to have Docker installed on the machine you're using for deployment. Once you have Docker set up, you can use the following steps to deploy your app:

1. Write a Dockerfile for your app. The Dockerfile should specify the base image to use, any additional software that needs to be installed, and how to configure your app to run within the container.

2. Build the Docker image using the Dockerfile. This is done by running the command docker build -t <image_name> . in the directory where the Dockerfile is located. The -t flag specifies the name you want to give the image, and the . specifies the current directory as the build context.

3. Run the Docker image to start a container. This is done by running the command docker run -p <host_port>:<container_port> <image_name>. The -p flag maps the specified host port to the specified container port. The <image_name> should be the same as the name specified in step 2.

4. Your application is now running in a container and it's accessible through the host port you specified.

Here's an example of a Dockerfile for a simple Python app:


                # Use an official Python runtime as the base image
                FROM python:3.8-alpine
                
                # Set the working directory in the container
                WORKDIR /app
                
                # Copy the requirements file into the container
                COPY requirements.txt .
                
                # Install the required packages
                RUN pip install --no-cache-dir -r requirements.txt
                
                # Copy the application code into the container
                COPY . .
                
                # Expose the port on which the app will run
                EXPOSE 8000
                
                # Run the command to start the app
                CMD ["python", "app.py"]

You can build this Dockerfile by running


                docker build -t my_app .

then run the container by

                docker run -p 8000:8000 my_app


This will run the container and map the host's port 8000 to the container's port 8000 so you can access the app on http://localhost:8000

Please note that this is just an example and you may need to adjust the commands, ports, and file paths based on your specific application and environment.



# Support:

For issues that arise that have not been documented above, contact Paulina.