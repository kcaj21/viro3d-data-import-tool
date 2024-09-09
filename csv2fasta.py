import csv
import pandas as pd

# Define the paths to your input CSV file and the output FASTA file

# Main Data
# in_path = "/home/viro-admin/projects/data/phylo-data-script/sequences.csv"
# out_path = "/home/viro-admin/projects/data/phylo-data-script/viro3d_seq_db.fasta"

#Toy Data
in_path = "/home/viro-admin/projects/data/phylo-data-script/toy_sequences.csv"
out_path = "/home/viro-admin/projects/data/phylo-data-script/toy_viro3d_seq_db.fasta"

# Open the input CSV file for reading and the output FASTA file for writing
with open(in_path, "r") as in_handle, open(out_path, "w") as out_handle:
    # Iterate over each line in the CSV file
    for line in in_handle:
        # Strip newline characters and split the line into parts using comma as the delimiter
        parts = line.strip("\n").split(',')
        
        # Assuming the first part is the sequence identifier and the second part is the sequence itself
        header = parts[0]  # Sequence identifier
        seq = parts[1]     # Sequence
        
        # Write the FASTA formatted line to the output file
        out_handle.write(f">{header}\n{seq}\n")