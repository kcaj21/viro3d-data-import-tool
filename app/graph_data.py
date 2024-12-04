import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import re
from unidecode import unidecode

csv_path = r'/home/viro-admin/projects/data/phylo-data-script/input_files/virosphere-fold-v1_predicted_dataset_updated_4.csv'

json_file_path = r'/home/viro-admin/projects/data/phylo-data-script/output_files/graph_data.json'

def make_graph_data_json(csv_path, json_file_path):
    
    print(f"Processing: graph_data.json")
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