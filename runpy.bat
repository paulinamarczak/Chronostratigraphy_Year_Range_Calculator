@echo off

rem Please make sure you have a working install of python first.

rem Find an appropriate gdal installation wheel here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
rem Then install gdal using pip and the full file path of the .whl in commandline: pip install path-to-wheel-file.whl

rem pip install rasterio
rem pip install numpy
rem pip install click
rem pip install rasterio
rem pip install multiprocessing.Pool
rem pip install pandas

rem Set your gdal paths to your own install folder

rem Set your python\scripts path, rasterio\gdal_data path, and osgeo\data\proj path.
rem If these are not yet installed, run the batch file once, then locate the paths once the packages are installed.
rem Update the path with your local installs.
rem Now you may rerun the batch file.

set "PATH= %PATH%, %ProgramFiles%\ArcGIS\Pro\bin\Python\Scripts\%"
echo %PATH%

rem Set your python exe to your own install folder

set python_exe= "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

rem Configure the field name in the script

%python_exe% ".\strat_range_calc.py"


pause