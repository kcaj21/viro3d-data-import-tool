import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import re
from unidecode import unidecode

csv_file_path = r'virosphere-fold-v1_predicted_dataset_updated_4.csv'
toy_csv_path = r'virosphere-fold-v1_toy_dataset_cleaned.csv'
tax_file_path = r'metadata_taxonomy_only.csv'
graph_data_csv_file_path = r'graph_data_viruses_with_realm.csv'

full_json_file_path = r'proteinstructures.json'
graph_data_json_file_path = r'graph_data_decoded.json'

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

        
# def make_graph_data_json(csv_path, json_file_path):
#     data = []
    
#     df = pd.read_csv(csv_path, skipinitialspace=True, usecols=['id', 'x', 'y', 'Realm'])
    
#     # Convert numeric columns to float
#     for col in ['x', 'y']:
#         df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
#     # Convert DataFrame to list of dictionaries
#     for _, row in df.iterrows():
#         data.append({
#             # 'id': row['id'],
#             'id':row['id'],
#             'x': float(row['x']),
#             'y': float(row['y']),
#             'Realm': row['Realm'],
#         })
    
#     # Open a json writer, and use the json.dumps() 
#     # function to dump data
#     with open(json_file_path, 'w', encoding='utf-8') as jsonf:
#         json.dump(data, jsonf, indent=4, ensure_ascii=False)

def make_graph_data_json(csv_path, json_file_path):
    data = []
    
    df = pd.read_csv(csv_path, skipinitialspace=True, usecols=['Virus name(s)', 'PC1', 'PC2', 'Realm']).iloc[:,[1,0,2,3]]
    # df = df.iloc[:,[1,0,2,3]]
    df = df.drop_duplicates()
    df = df.fillna("Unclassified")
    #Unclassified

    # print(df)
    
    # # Convert numeric columns to float
    for col in ['PC1', 'PC2']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    # # Convert DataFrame to list of dictionaries
    for _, row in df.iterrows():
        data.append({
            # 'id': row['id'],
            'id': unidecode(row['Virus name(s)']),
            'x': float(row['PC1']),
            'y': float(row['PC2']),
            'Realm': row['Realm'],
        })
    
    # # Open a json writer, and use the json.dumps() 
    # # function to dump data
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, indent=4, ensure_ascii=False)
         

make_protein_structure_json(csv_file_path, full_json_file_path)

# make_graph_data_json(csv_file_path, graph_data_json_file_path)


# Virus name is col 15

# child_level = 15
# parent_level = child_level - 1

# 39 COLS

# filter parent column by each unique value and add children values to array
# if child column is empty, move child column index +1 until a non null value is found and add those to array
# dataframe as entire csv and if null, move one column up
