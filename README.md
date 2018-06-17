# Udacity-DataWrangling
Data wrangling and analysis of Norman, OK data from OpenStreetMap using python and SQL

## Purpose
The purpose of this project is to become familar with wrangling and cleaning a fairly large data set. It will also help me undersand importing that data into a database and analyzing the information. 

I used OpenStreetMap data for my hometown, Norman for this  

## File Structure

1. DataWrangling-Kopp.html - This is the project report. It contains details on the process of data wrangling and analysis.
2. Audit folder - This contains the python scripts I wrote to audit the data to determine cleanliness
    * audit_fileselectore.py - The python file to quickly switch between samples in all of the audits
    * audit_postcodes.py - The python script to find errors or inconsistencies in post codes
    * audit_state.py - The python script to determine if any state values were incorrect. They were not.
    * audit_stats.py - The python script to determine some statistics from the data set like unique users
3. Clean folder - This contains the python scripts I wrote to clean data as needed
    * clean_postcodes.py - The python function to clean incorrect postcodes
    * clean_streetnames.py - The python function to clean incorrect street names
4. export.py - This is the python script that cleans, shapes, and exports the data to CSV format. Some of the code here was borrowed from the Udacity excercises previously in the lesson 
5. norman.osm - This is my full data set
6. norman-sample.osm - This is a smaller sample of the data I used to verify my functions
7. OpenStreetMap-Sample-Project.ipynb - The Jupyter notebook I used to generate the report. 
8. sample.py - This is a file provided by Udacity to take a sample of my large dataset
9. schema.py - This is the python defined schema for converting from XML to CSV data in the correct format
 

