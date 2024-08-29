import csv



def remove_ufeff_from_first_cell(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the first row
        try:
            first_row = next(reader)
        except StopIteration:
            print("The input file is empty.")
            return
        
        # Check and modify the first cell if necessary
        if len(first_row) > 0 and first_row[0].startswith('/ufeff'):
            first_row[0] = first_row[0].replace('/ufeff', '', 1)
        
        # Write the modified first row
        writer.writerow(first_row)
        
        # Write the rest of the rows unchanged
        for row in reader:
            writer.writerow(row)

# Usage
input_file = r'virosphere-fold-v1_toy_dataset_edit.csv'
output_file = r'virosphere-fold-v1_toy_dataset_cleaned.csv'

remove_ufeff_from_first_cell(input_file, output_file)

print(f"'/ufeff' removed from the first cell successfully. Output saved to {output_file}")
