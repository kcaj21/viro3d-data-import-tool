import json
import pandas as pd

clusters_csv = r'foldseekCluster_cluster_meta.csv'

#This will convert the CSV of clusters of similar proteins to JSON
#This will be needed for the intended extension feature of the app to allow the user to browse a table of proteins in similar clusters to the one they are currently viewing

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

def find_duplciates(clusters_csv):

    df = pd.read_csv(clusters_csv)

    cluster_members = df[df['member_record_id'].duplicated() == True]

    print(cluster_members)