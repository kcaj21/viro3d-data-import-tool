import json
import pandas as pd

clusters_csv = r'/home/viro-admin/projects/data/viro3d-data-import-tool/input_files/foldseekCluster_cluster_meta.csv'
output_path = r'/home/viro-admin/projects/data/viro3d-data-import-tool/output_files/clusters.json'

#This will convert the CSV of clusters of similar proteins to JSON
#This will be needed for the intended extension feature of the app to allow the user to browse a table of proteins in similar clusters to the one they are currently viewing

import pandas as pd
import json

def csv_to_clusters(clusters_csv, clusters_json_file_path):

    df = pd.read_csv(clusters_csv)

    #using groupby to group the unique member records by their cluster represntstive
    grouped = df.groupby('cluster_representative')

    json_result = []
    total_clusters = len(grouped)
    progress = 0

    #for each cluster rep and their group, we create an object with an id = to the cluster rep and then add a nested list of the members and their properties
    for cluster_rep, group in grouped:
        cluster_data = {
            "_id": cluster_rep,
            "cluster_members": group.apply( #apply is another way of iterating over each member and performing some operation - in this case a lambda function to form each row that represents a cluster member
                lambda row: {
                    "cluster_rep_id": cluster_rep,
                    "member_record_id": row['member_record_id'],
                    "protein_length": row['protlen'],
                    "tax_id": row['taxid'],
                    "species": row['Species'],
                    "plDDT_score": row['plddd']
                },
                axis=1 # axis can either be 0 or 1. 0 for iterating column-wise and 1 for row-wise
            ).tolist()
        }

        json_result.append(cluster_data)

        progress += 1
        if progress % 10 == 0 or progress == total_clusters:
            percentage_progress = round((progress / total_clusters) * 100, 2)
            print(f'\rProgress: {percentage_progress}%', end='', flush=True)

    with open(clusters_json_file_path, 'w', encoding='utf-8') as jsonf:
        json.dump(json_result, jsonf, indent=4)

def find_duplciates(clusters_csv):

    df = pd.read_csv(clusters_csv)

    cluster_members = df[df['member_record_id'].duplicated() == True]

    print(cluster_members)