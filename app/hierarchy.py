import csv
import json
import pandas as pd

taxonomy_csv_file_path = r'virosphere-fold-v1_predicted_dataset_updated.csv'

def csv_to_taxonomy_hierarchy(taxonomy_csv_file_path, taxonomy_json_file_path):

    ranks = ['Realm', 'Subrealm', 'Kingdom', 'Subkingdom', 'Phylum', 'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family', 'Subfamily', 'Genus', 'Subgenus', 'Species', 'Virus name(s)']

    df = pd.read_csv(taxonomy_csv_file_path)

    json_result = []

    parent_rank = 0
    base_child_rank = 1

    while parent_rank < len(ranks) -1:

        parent_filter_options = pd.read_csv(
            taxonomy_csv_file_path, usecols=[ranks[parent_rank]]
            ).drop_duplicates(subset=[ranks[parent_rank]]).dropna()[ranks[parent_rank]].tolist()
        
        for option in parent_filter_options:
            
            filtered_df = df.loc[df[ranks[parent_rank]] == option]

            child_rank = base_child_rank

            while not filtered_df[ranks[child_rank]].drop_duplicates().notnull().any():
                child_rank+=1
            
            else:
                    
                child_filter = filtered_df[ranks[child_rank]].drop_duplicates().dropna().tolist()

                result = dict(
                _id = option,
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
        percentage_progress = round((parent_rank / (len(ranks) -1)) * 100, 2)
        print(f'\rProgress: {percentage_progress}%', end='', flush=True)

    with open(taxonomy_json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(json_result, indent=4))