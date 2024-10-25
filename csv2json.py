import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import re

csv_file_path = r'virosphere-fold-v1_predicted_dataset_updated_3.csv'
toy_csv_path = r'virosphere-fold-v1_toy_dataset_cleaned.csv'
tax_file_path = r'metadata_taxonomy_only.csv'
graph_data_csv_file_path = r'graph_data.csv'

toy_json_file_path = r'proteinstructures_toy.json'
full_json_file_path = r'proteinstructures.json'
graph_data_json_file_path = r'graph_data.json'

def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]', '', text)
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_protein_structure_json(csv_file_path, json_file_path):
     
    # create a dictionary
    data = {}
    
    #if the \ufeff error occurs, switch encoding from 'utf-8' to 'utf-8-sig'
    with open(csv_file_path, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
         
        #  Convert each row into a dictionary 
        # and add it to data
        # for rows in csvReader:

        data = [row for row in csvReader]

        for x in data:
            x['Virus name(s)'] = remove_non_ascii(x['Virus name(s)'])
        
 
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
        
def make_graph_data_json(csv_path, json_file_path):
    data = []
    
    df = pd.read_csv(csv_path, skipinitialspace=True, usecols=['id', 'Virus name(s)', 'x', 'y'])
    
    # Convert numeric columns to float
    for col in ['x', 'y']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    # Convert DataFrame to list of dictionaries
    for _, row in df.iterrows():
        data.append({
            'id': row['id'],
            'Virus name(s)': remove_non_ascii(row['Virus name(s)']),
            'x': float(row['x']),
            'y': float(row['y'])
        })
    
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, indent=4, ensure_ascii=False)
         
# make_graph_data_json(graph_data_csv_file_path, graph_data_json_file_path)


# Virus name is col 15

# child_level = 15
# parent_level = child_level - 1

# 39 COLS

# filter parent column by each unique value and add children values to array
# if child column is empty, move child column index +1 until a non null value is found and add those to array
# dataframe as entire csv and if null, move one column up
