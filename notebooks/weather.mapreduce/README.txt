Eigen-by-Station.sh	The master shell script for running the map-reduce job
map-year-temp.py	The map script
reduce-year-temp.py	The reduce script

Statistics.py		A module for computing first and second order statistics
coding.py		A module for writing and reading key,value lines where the value is a pickled, encoded object

process-days.py		A script for generating Dates.pkl a table that related dates 
			of the form mm/dd to numbers in the range 0:365
Dates.pkl

process-stations.py	A script which generates Stat2Lat.pkl: a table that relates station names to their Latitude.
Stat2Lat.pkl

randomize.py		A script for efficiently randomizing the order of lines in a file. 

README.txt		This file

