import pandas as pd

cluster_csv = r'/home/viro-admin/projects/data/viro3d-data-import-tool/input_files/foldseekCluster_cluster_meta.csv'
metadata_csv = r'/home/viro-admin/projects/data/viro3d-data-import-tool/input_files/virosphere-fold-v1_predicted_dataset_updated_4.csv'

# Load the first CSV
clusters = pd.read_csv(cluster_csv)

# Load the second CSV
metadata = pd.read_csv(metadata_csv)

# Perform the mapping
merged_df = pd.merge(
    clusters,
    metadata[['record_id', 'Virus name(s)', 'Family', 'host', 'genbank_name_curated', 'uniprot_id', 'nt_acc']],  # Select columns to map from df2
    left_on='member_record_id',                  # Unique ID column in df1
    right_on='record_id',                 # Unique ID column in df2
    how='left'                           # Keep all rows from df1
)

# Optionally drop the duplicate ID column from df2 if not needed
merged_df = merged_df.drop(columns=['record_id'])

# Save or use the result
merged_df.to_csv('/home/viro-admin/projects/data/viro3d-data-import-tool/input_files/merged_cluster_file.csv', index=False)

# record_id	protein_name	virus_name	species	family	host	protein_length (No. of Residues)	uniprot_id	genbank_id	taxid	nucleotide_accession_number

