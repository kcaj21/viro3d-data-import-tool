import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import re

csv_file_path = r'virosphere-fold-v1_predicted_dataset_updated.csv'
toy_csv_path = r'virosphere-fold-v1_toy_dataset_cleaned.csv'
tax_file_path = r'metadata_taxonomy_only.csv'
toy_json_file_path = r'proteinstructures_toy.json'

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_protein_structure_json(toy_csv_path, toy_json_file_path):
     
    # create a dictionary
    data = {}
    
    #if the \ufeff error occurs, switch encoding from 'utf-8' to 'utf-8-sig'
    with open(toy_csv_path, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
         
        #  Convert each row into a dictionary 
        # and add it to data
        # for rows in csvReader:

        data = [row for row in csvReader]

        for x in data:
            x['Virus name(s)'] = remove_non_ascii(x['Virus name(s)'])
        
 
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(toy_json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
         
make_protein_structure_json(toy_csv_path, toy_json_file_path)


# Virus name is col 15

# child_level = 15
# parent_level = child_level - 1

# 39 COLS

# filter parent column by each unique value and add children values to array
# if child column is empty, move child column index +1 until a non null value is found and add those to array
# dataframe as entire csv and if null, move one column up
