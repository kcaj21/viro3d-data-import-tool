import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import re
from unidecode import unidecode

csv_file_path = r'/home/viro-admin/projects/data/phylo-data-script/input_files/virosphere-fold-v1_predicted_dataset_updated_4.csv'

json_file_path = r'/home/viro-admin/projects/data/phylo-data-script/output_files/protein_structures.json'
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_protein_structure_json(csv_file_path, json_file_path):
    
    print(f"Processing: protein_structures.json")
     
    # create a dictionary
    data = {}
    
    #if the \ufeff error occurs, switch encoding from 'utf-8' to 'utf-8-sig'
    with open(csv_file_path, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        
        fieldnames = csvReader.fieldnames
        fieldnames = ['_id' if name == 'record_id' else name for name in fieldnames]
        
        csvReader = csv.DictReader(csvf, fieldnames=fieldnames)
        next(csvReader)
         
        #  Convert each row into a dictionary 
        # and add it to data
        # for rows in csvReader:

        data = []
        for row in csvReader:
            row['Virus name(s)'] = unidecode(row['Virus name(s)'])
            data.append(row)
        
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)
