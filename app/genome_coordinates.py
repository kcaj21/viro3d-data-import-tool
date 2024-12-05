# Imports
import pandas as pd
import csv
import json
import operator
from collections import OrderedDict
from unidecode import unidecode

# File Paths
data_csv_filepath = r'/home/viro-admin/projects/data/viro3d-data-import-tool/input_files/virosphere-fold-v1_predicted_dataset_updated_4.csv'
genome_coordinates_json_filepath = r'/home/viro-admin/projects/data/viro3d-data-import-tool/output_files/genome_coordinates.json'

# Main Conversion Function
def genome_coordinates_csv_to_json(data_csv_filepath, genome_coordinates_json_filepath):
    print(f"Processing: genome_coordinates.json")
    
    df = pd.read_csv(
        data_csv_filepath, 
        usecols=[
            'record_id', 'pept_cat', 'genbank_genome_coordinates', 'nt_acc', 
            'seg', 'Virus name(s)', 'genbank_name_curated', 'Virus isolate designation', 'genome_length_bp'
        ]
    )
    df.sort_values(by=['record_id'])

    # Extract Columns into Lists
    record_id_column = df['record_id'].tolist()
    genome_coordinate_column = df['genbank_genome_coordinates'].tolist()
    pept_cat_column = df['pept_cat'].tolist()
    nt_acc_column = df['nt_acc'].tolist()
    segment_column = df['seg'].tolist()
    virus_name_column = df['Virus name(s)'].tolist()
    gene_name_column = df['genbank_name_curated'].tolist()
    isolate_designation_column = df['Virus isolate designation'].tolist()
    genome_length_bp_column = df['genome_length_bp'].tolist()

    # Create Dictionary for Coordinates
    coords_dictionary = [
        {
            "id": id,
            "nt_acc": nt_acc,
            "virus_name": unidecode(virus_name),
            "gene_name": gene_name,
            "segment": segment,
            "coordinates": coords,
            "pept_cat": pept_cat,
            "isolate_designation": isolate_designation,
            "genome_length_bp": genome_length_bp
        }
        for id, nt_acc, virus_name, gene_name, segment, coords, pept_cat, isolate_designation, genome_length_bp in zip(
            record_id_column, 
            nt_acc_column, 
            virus_name_column, 
            gene_name_column, 
            segment_column, 
            genome_coordinate_column, 
            pept_cat_column, 
            isolate_designation_column,
            genome_length_bp_column
        )
    ]
    
    json_result = {}

    for item in coords_dictionary:
        # Handle missing values for 'segment' and 'isolate_designation'
        if type(item['segment']) == float:
            item['segment'] = 'Non-segmented'
        if type(item['isolate_designation']) == float:
            item['isolate_designation'] = 'N/A'

        # Process genome coordinates
        if 'join' in item['coordinates']:
            coords_list = genome_with_joins_converter(
                item['coordinates'], item['id'], item['pept_cat'], 
                item['nt_acc'], item['segment'], item['virus_name'], 
                item['gene_name'], item['isolate_designation'], item["genome_length_bp"]
            )
        else:
            coords_list = genome_with_no_joins_converter(
                item['coordinates'], item['id'], item['pept_cat'], 
                item['nt_acc'], item['segment'], item['virus_name'], 
                item['gene_name'], item['isolate_designation'], item["genome_length_bp"]
            )

        # Append to JSON result
        for coord in coords_list:
            if coord['nt_acc'] not in json_result:
                json_result[coord['nt_acc']] = []
            json_result[coord['nt_acc']].append(coord)

    # Create MongoDB-style documents
    mongo_documents = [
    {
        "_id": nt_acc,
        "isolate_designation": coords[0].pop('isolate_designation', None),
        "segment": coords[0].get('segment'),
        "genome_length_bp": coords[0].pop('genome_length_bp', None),
        "coordinates": coords
    }
        for nt_acc, coords in json_result.items()
    ]

    # Write to JSON
    with open(genome_coordinates_json_filepath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(mongo_documents, indent=4, ensure_ascii=False))

#This converter is envoked for viruses that DON'T have spliced genomes (no joins)
def genome_with_no_joins_converter(genomic_coordinates, id, pept_cat, nt_acc, segment, virus_name, gene_name, isolate_designation, genome_length_bp):
    
    # Clean and parse the coordinates property
    genomic_coordinates = genomic_coordinates.replace(">", "").replace("<", "")
    coordinates_cleaned = genomic_coordinates[1:-1]

    start, end_and_sense = coordinates_cleaned.split(':')
    start = float(start)

    end, sense = end_and_sense.split(']')
    end = float(end)
    sense = sense.strip()[1]

    # Create annotations
    annotations = [{
        "id": id,
        "nt_acc": nt_acc,
        "virus_name": virus_name,
        "gene_name": gene_name,
        "isolate_designation": isolate_designation,
        "pept_cat": pept_cat,
        "segment": segment,
        "start": start,
        "end": end,
        "strand": sense,
        "family": id,
        "genome_length_bp": genome_length_bp,
        "join": "none",
    }]
    return annotations

#This converter is envoked for viruses that DO have spliced genomes (with joins)
def genome_with_joins_converter(join_coordinates, id, pept_cat, nt_acc, segment, virus_name, gene_name, isolate_designation, genome_length_bp):
    
    # Clean and parse the coordinates property
    join_coordinates = join_coordinates.replace(">", "").replace("<", "")[5:-1]
    joins_list = join_coordinates.split(',')

    final_joins_list = []
    for i, join in enumerate(joins_list, 1):
        new_join = join.replace(" ", "").replace("[", "")
        start, end_and_sense = new_join.split(':')
        end, sense = end_and_sense.split("]")

        coords = {
            "id": f"{id}_{i}",
            "nt_acc": nt_acc,
            "virus_name": virus_name,
            "gene_name": gene_name,
            "isolate_designation": isolate_designation,
            "pept_cat": pept_cat,
            "segment": segment,
            "start": float(start),
            "end": float(end),
            "strand": sense.strip("()"),
            "family": id,
            "genome_length_bp": genome_length_bp,
            "join": "none"
        }
        final_joins_list.append(coords)

    # Sort and add join annotations
    final_joins_list.sort(key=operator.itemgetter('start'))
    
    #The distance between the annotations being joined must be calculated (the difference variable)
    #Then, 0.01 will be added to the coordinate of the "end" annotation (where the join begins) and 0.01 subtracted from the "start" annotation (where the jonin ends)
    for i in range(len(final_joins_list) - 1):
        difference = final_joins_list[i + 1]["start"] - final_joins_list[i]["end"]
        left_join_start = final_joins_list[i]["end"] + 0.01
        left_join_end = final_joins_list[i]["end"] + (difference / 2) #The difference is divided by 2 and ADDED to the left join end. Therefore, a line of a length half that of the distance is drawn
        #The left join end and right join start lines will meet in the middle of the distance between the annotations
        right_join_start = final_joins_list[i + 1]["start"] - (difference / 2) + 0.01 #The difference is divided by 2 and SUBTRACTED from the right join start. Therefore, a line of a length half that of the distance is drawn
        right_join_end = final_joins_list[i + 1]["start"] - 0.01

        final_joins_list.insert(i + 1, {
            "id": f"{final_joins_list[i]['id']}_end",
            "nt_acc": nt_acc,
            "virus_name": virus_name,
            "gene_name": gene_name,
            "isolate_designation": isolate_designation,
            "pept_cat": pept_cat,
            "segment": segment,
            "start": left_join_start,
            "end": left_join_end,
            "strand": sense,
            "family": id,
            "genome_length_bp": genome_length_bp,
            "join": "left-join"
        })

        final_joins_list.insert(i + 2, {
            "id": f"{final_joins_list[i + 2]['id']}_start",
            "nt_acc": nt_acc,
            "virus_name": virus_name,
            "gene_name": gene_name,
            "isolate_designation": isolate_designation,
            "pept_cat": pept_cat,
            "segment": segment,
            "start": right_join_start,
            "end": right_join_end,
            "strand": sense,
            "family": id,
            "genome_length_bp": genome_length_bp,
            "join": "right-join"
        })

    return final_joins_list

# Type Testing Function to check for any NaN values in pandas dataframe
def type_test(coords_dictionary):
    for item in coords_dictionary:
        print(type(item['nt_acc']))


