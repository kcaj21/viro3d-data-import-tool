import pandas as pd

# Define the paths to your input CSV file and the output FASTA file

# Main Data
in_path = r'/home/viro-admin/projects/data/phylo-data-script/input_files/virosphere-fold-v1_predicted_dataset_updated_4.csv'
out_path = r"/home/viro-admin/projects/data/phylo-data-script/output_files/viro3d_seq_db.fas"

def make_fasta_file(in_path, out_path):
    print(f"Processing: viro3d_seq_db.fas")
    
    df = pd.read_csv(in_path, usecols=['record_id', 'structure_seq'])

    # Open the output file and write in FASTA format
    with open(out_path, "w") as out_handle:
        for _, row in df.iterrows():
            header = row['record_id']  # Sequence identifier
            seq = row['structure_seq']  # Sequence
            out_handle.write(f">{header}\n{seq}\n")