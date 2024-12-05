import os
from fasta import make_fasta_file
from genome_coordinates import genome_coordinates_csv_to_json
from graph_data import make_graph_data_json
from protein_structures import make_protein_structure_json

# Folder paths
input_folder = r'/home/viro-admin/projects/data/viro3d-data-import-tool/input_files'
output_folder = r'/home/viro-admin/projects/data/viro3d-data-import-tool/output_files'

# Output file paths
protein_structure_json_file_path = os.path.join(output_folder, 'protein_structures.json')
genome_coordinates_json_filepath = os.path.join(output_folder, 'genome_coordinates.json')
graph_data_json_file_path = os.path.join(output_folder, 'graph_data.json')
fasta_file_path = os.path.join(output_folder, 'viro3d_seq_db.fas')

def check_input_folder(folder_path):

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The input folder '{folder_path}' does not exist.")
    if not os.listdir(folder_path):
        raise FileNotFoundError(f"The input folder '{folder_path}' is empty.")
    print(f"Input folder '{folder_path}' is valid and contains files.")

def get_csv_file_from_user(folder_path):

    while True:
        print(f"Available files in '{folder_path}':")
        files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")
        
        try:
            choice = input("Enter the number of the file you want to process (or enter 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                exit(0)

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(files):
                return os.path.join(folder_path, files[choice_idx])
            else:
                print(f"Error: Invalid choice. Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Error: Please enter a valid number.")

def main():
    check_input_folder(input_folder)
    
    csv_file_path = get_csv_file_from_user(input_folder)
    print(f"Processing file: {csv_file_path}")
    
    make_protein_structure_json(csv_file_path, protein_structure_json_file_path)
    make_graph_data_json(csv_file_path, graph_data_json_file_path)
    genome_coordinates_csv_to_json(csv_file_path, genome_coordinates_json_filepath)
    make_fasta_file(csv_file_path, fasta_file_path)
    
    print(f"All files have been generated in the 'output_files' directory.")

if __name__ == "__main__":
    main()
