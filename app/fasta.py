import pandas as pd

in_path = r'/home/viro-admin/projects/data/viro3d-data-import-tool/input_files/virosphere-fold-v1_predicted_dataset_updated_4.csv'
out_path = r"/home/viro-admin/projects/data/viro3d-data-import-tool/output_files/viro3d_seq_db.fas"

def make_fasta_file(in_path, out_path):
    print(f"Processing: viro3d_seq_db.fas")
    
    df = pd.read_csv(in_path, usecols=['record_id', 'structure_seq'])

    # Write the data to a .fas file
    with open(out_path, "w") as out_handle:
        for _, row in df.iterrows():
            header = row['record_id']  # Sequence identifier
            seq = row['structure_seq']  # Sequence
            out_handle.write(f">{header}\n{seq}\n")