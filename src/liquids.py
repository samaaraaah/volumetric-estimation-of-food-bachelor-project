import csv

# Customize these
file1_path = '../data/cleaned/weight_data_cleaned_grouped_no_liquid.csv'
file2_path = '../data/cleaned/weight_data_cleaned_grouped.csv'
output_path = '../data/liquids.csv'


def load_rows_by_description(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        descriptions = set(row['description'] for row in rows)
    return rows, descriptions

# Load both files
rows1, desc1 = load_rows_by_description(file1_path)
rows2, desc2 = load_rows_by_description(file2_path)

# Find new descriptions in file2
new_descriptions = desc2 - desc1

# Extract corresponding rows from file2
liquid_rows = [row for row in rows2 if row['description'] in new_descriptions]

# Write result to CSV
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=liquid_rows[0].keys())
    writer.writeheader()
    writer.writerows(liquid_rows)

print(f"✅ Extracted {len(liquid_rows)} new rows to {output_path}")
