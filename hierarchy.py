import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import pdb

csv_file_path = r'metadata_taxonomy_only.csv'

def csv_to_hierarchy(csv_file_path):

    ranks = ['Realm', 'Kingdom', 'Phylum', 'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family', 'Subfamily', 'Genus', 'Subgenus', 'Species']

    parent_filter_options = pd.read_csv(
        csv_file_path, usecols=[ranks[0]]
        ).drop_duplicates(subset=[ranks[0]]).dropna()[ranks[0]].tolist()
    
    df = pd.read_csv(csv_file_path)

    child_list = []

    for option in parent_filter_options:
        filtered_df = df.loc[df[ranks[0]] == option]

        counter = 1

        # pdb.set_trace()
        while not filtered_df[ranks[counter]].drop_duplicates().notnull().any():
            counter = counter + 1
            print(counter)
        else:



    
            child_filter = filtered_df[ranks[counter]].drop_duplicates().dropna().tolist()
            child_list.append(child_filter)
    print(child_list)

csv_to_hierarchy(csv_file_path)

# df.loc[df[parent_level] == option]