import csv
import json
import pandas as pd

taxonomy_csv_file_path = r'virosphere-fold-v1_predicted_dataset_updated.csv'
taxonomy_json_file_path = r'/home/viro-admin/projects/data/phylo-data-script/phylogeny.json'

clusters_csv = r'foldseekCluster_cluster_meta.csv'
clusters_json_file_path = r'/home/viro-admin/projects/data/phylo-data-script/clusters.json'



def csv_to_taxonomy_hierarchy(taxonomy_csv_file_path, taxonomy_json_file_path):

    ranks = ['Realm', 'Subrealm', 'Kingdom', 'Subkingdom', 'Phylum', 'Subphylum', 'Class', 'Subclass', 'Order', 'Suborder', 'Family', 'Subfamily', 'Genus', 'Subgenus', 'Species']

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

    with open(taxonomy_json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(json_result, indent=4))



# csv_to_taxonomy_hierarchy(taxonomy_csv_file_path, taxonomy_json_file_path)

def csv_to_clusters(clusters_csv, clusters_json_file_path):

    df = pd.read_csv(clusters_csv)

    json_result = []

    cluster_representatives = df['cluster_representative'].drop_duplicates().tolist()

    length = len(cluster_representatives) - 1

    progress = 0

    for cluster_rep in cluster_representatives:


        result = dict(
            _id = cluster_rep,
            cluster_members = []
        )

        filtered_df = df.loc[df['cluster_representative'] == cluster_rep]

        children = filtered_df.iloc[:, 1:9]

        for index, row in children.iterrows():
            
            child_result = dict(
                cluster_rep_id = cluster_rep,
                member_record_id = row['member_record_id'],
                protein_length = row['protlen'],
                tax_id = row['taxid'],
                species = row['Species'],
                plDDT_score = row['plddd']
                )

            result['cluster_members'].append(child_result)

        json_result.append(result)
        progress+=1
        percentage_progress = round((progress / length) * 100, 2)
        print(f'\rProgress: {percentage_progress}%', end='', flush=True)

    with open(clusters_json_file_path, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(json_result, indent=4))

csv_to_clusters(clusters_csv, clusters_json_file_path)

