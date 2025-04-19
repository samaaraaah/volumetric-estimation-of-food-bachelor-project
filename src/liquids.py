import csv
import pandas as pd

file1_path = '../data/cleaned/weight_data_cleaned_grouped_no_liquid.csv'
file2_path = '../data/cleaned/weight_data_cleaned_grouped.csv'
output_path = '../data/liquids.csv'
ready_path = '../data/ready/liquids_ready.csv'
removed_path = '../data/removed_logs.csv'


def load_rows_by_description(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        descriptions = set(row['description'] for row in rows)
    return rows, descriptions

# Load files
rows1, desc1 = load_rows_by_description(file1_path)
rows2, desc2 = load_rows_by_description(file2_path)
rows_del, desc_del = load_rows_by_description(removed_path)

# Find new descriptions in file2
new_descriptions = desc2 - desc1
new_descriptions = new_descriptions - desc_del

# Extract corresponding rows from file2
liquid_rows = [row for row in rows2 if row['description'] in new_descriptions]

# Write result to CSV
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=liquid_rows[0].keys())
    writer.writeheader()
    writer.writerows(liquid_rows)

# Create the new CSV with 'id', '00_MSG_00_TEXT', '00_MSG_01_IMAGE' and '00_MSG_02_TEXT'
liquid_df = pd.read_csv(output_path)
output_data = {
    'id': range(len(liquid_df)),  
    '00_MSG_00_TEXT': liquid_df['all_food_items'].str.lower(), # Retrieve all the food items present on the picture
    '00_MSG_01_IMAGE': liquid_df.apply(lambda row: f"https://www.myfoodrepo.org/api/v1/subjects/{row['key']}/dish_media/{row['image_id']}", axis=1),  # Generate the URL
    '00_MSG_02_TEXT': liquid_df['description'].str.lower() # Retrieve the description given by the user
}

output_df = pd.DataFrame(output_data)
output_df.to_csv(ready_path, index=False)

print(f"Extracted {len(liquid_rows)} new rows to {output_path}")
