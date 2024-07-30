import csv
import json
import pandas as pd
import math
from typing import List, Optional
from pydantic import BaseModel, Field
 
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_protein_structure_json(csv_file_path, json_file_path):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csv_file_path, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        #  Convert each row into a dictionary 
        # and add it to data
        # for rows in csvReader:
             
        #     Assuming a column named 'record_id' to
        #     be the primary key
        #     key = rows['record_id']
        #     data[key] = rows

        data = [row for row in csvReader]
 
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(json_file_path, 'r', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

parent = 'Realm'
child = 'Kingdom'

levels = ['Realm', 'Kingdom', 'Phylum', 'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family', 'Subfamily', 'Genus', 'Subgenus', 'Species']


def make_phylogenetic_tree_json(tax_file_path):

    # reading csv to take parent column, remove the duplicates and blank values and create a list from them

    parent_level = levels[0]

    parent_filter_options = pd.read_csv(
        tax_file_path, usecols=[parent_level]
        ).drop_duplicates(subset=[parent_level]).dropna()[parent_level].tolist()
    

    
    # instantiating empty list to append each result to
    
    tax_list = []

    # looping over each unique value from the parent column in order to filter the parent column
    
    for option in parent_filter_options:

        # removing duplicate values from the child column

        # instantiating dataframe object that is just the parent and child columns, unaltered

        df = pd.read_csv(
            tax_file_path
            )

        filtered_df = df.loc[
            df[parent_level] == option
            ]
        
        counter = 1

        child_level = levels[counter]
        
        if not filtered_df[child_level].drop_duplicates().isnull().any():
        
            filtered_df = filtered_df.drop_duplicates(subset=[child_level]
                )
                    
            # turning the unique values from the children column into a list
            
            children = filtered_df[child_level].dropna().tolist()

            # creating a result variable - a dictionary with the parent taxon name, parent level and an empty list of children taxa

            result = dict(
                id = option,
                level = parent_level,
                children_taxa = []
            )

            # looping over each child taxon and adding it to the children_taxa list in the result variable

            for child in children:
                if type(child) == float:
                    pass
                else:
                    child_result = dict(
                        name = child,
                        level = child_level
                    )
                    result['children_taxa'].append(child_result)
                
            # appending the full result to the tax_list variable

            tax_list.append(result)
        
        else:
            while counter <= len(levels) -1:
                counter+1
                

            print('found null')

    print(tax_list)
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(tax_list, indent=4))

# class Child(BaseModel):
#     name: str
#     level: str

# class Taxon(BaseModel):
#     id: str 
#     level: str 
#     children_taxa: Optional[List[Child]] = None

    # result = Taxon(
    #     id = parent_filter_options[0],
    #     level = parent_level,
    #     children_taxa = []
    # )

    # for child in children:
    #     child_result = Child(
    #         name = child,
    #         level = child_level
    #     )
    #     result.children_taxa.append(child_result)
         
csv_file_path = r'virosphere-fold-v1_predicted_dataset_updated.csv'
tax_file_path = r'metadata_taxonomy_only.csv'
json_file_path = r'/home/viro-admin/projects/data/phylo-data-script/phylogeny.json'
 
make_phylogenetic_tree_json(tax_file_path)

# Virus name is col 15

# child_level = 15
# parent_level = child_level - 1

# 39 COLS

# filter parent column by each unique value and add children values to array
# if child column is empty, move child column index +1 until a non null value is found and add those to array
# dataframe as entire csv and if null, move one column up
