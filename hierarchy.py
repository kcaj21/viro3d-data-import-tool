import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import pdb

csv_file_path = r'metadata_taxonomy_only.csv'

def csv_to_hierarchy(csv_file_path):

    ranks = ['Realm', 'Subrealm', 'Kingdom', 'Subkingdom', 'Phylum', 'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family', 'Subfamily', 'Genus', 'Subgenus', 'Species']

    df = pd.read_csv(csv_file_path)

    json_result = []

    parent_rank = 0

    base_child_rank = 1

    while parent_rank < len(ranks) -1:
    # while parent_rank < 4:



        parent_filter_options = pd.read_csv(
            csv_file_path, usecols=[ranks[parent_rank]]
            ).drop_duplicates(subset=[ranks[parent_rank]]).dropna()[ranks[parent_rank]].tolist()
        
        for option in parent_filter_options:
            filtered_df = df.loc[df[ranks[parent_rank]] == option]

            child_rank = base_child_rank

            # pdb.set_trace()
            while not filtered_df[ranks[child_rank]].drop_duplicates().notnull().any():
                child_rank+=1
            else:
                    
                child_filter = filtered_df[ranks[child_rank]].drop_duplicates().dropna().tolist()
                # print(child_filter)
                result = dict(
                id = option,
                level = ranks[parent_rank],
                children_taxa = []
                )
                
                for child in child_filter:
                
                    child_result = dict(
                    name = child,
                    level = ranks[child_rank]
                    )
                
                    result['children_taxa'].append(child_result)

                json_result.append(result)
                child_rank = base_child_rank
        parent_rank+=1
        base_child_rank+=1
    # print(json_result)
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(json_result, indent=4))

json_file_path = r'/home/viro-admin/projects/data/phylo-data-script/phylogeny.json'


csv_to_hierarchy(csv_file_path)

# df.loc[df[parent_level] == option]